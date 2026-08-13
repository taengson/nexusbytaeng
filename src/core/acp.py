from typing import Any, Callable, Dict, List, NotRequired, Optional, TypedDict, Union
import asyncio
import json
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# --- ACP Types ---

class ACPRequest(TypedDict):
    jsonrpc: str
    method: str
    params: Dict[str, Any]
    id: int

class ACPResponse(TypedDict):
    jsonrpc: str
    result: NotRequired[Any]
    error: NotRequired[Dict[str, Any]]
    id: int

class ACPNotification(TypedDict):
    jsonrpc: str
    method: str
    params: Dict[str, Any]

# --- ACP Client ---

class ACPClient:
    """
    ACPClient handles JSON-RPC 2.0 communication with an Agent Server.
    Implements handshake, session management, and background listening for notifications.
    """
    def __init__(
        self, 
        command: List[str], 
        on_message: Callable[[Dict[str, Any]], None],
        app_context: Any = None
    ):
        self.command = command
        self.on_message = on_message
        self.app = app_context # Textual App for thread-safe UI updates
        
        self.process: Optional[asyncio.subprocess.Process] = None
        self.session_id: Optional[str] = None
        self.request_id = 0
        self._listen_task: Optional[asyncio.Task] = None
        self._is_active = False
        self._pending: Dict[int, asyncio.Future] = {}

    async def start(self):
        """Starts the agent process and the background listener loop."""
        self.process = await asyncio.create_subprocess_exec(
            *self.command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        self._is_active = True
        self._listen_task = asyncio.create_task(self._listen_loop())
        logger.info(f"ACP process started: {' '.join(self.command)}")

    async def stop(self):
        """Stops the agent process and listener loop."""
        self._is_active = False
        if self._listen_task:
            self._listen_task.cancel()
        if self.process:
            try:
                self.process.terminate()
                try:
                    await asyncio.wait_for(self.process.wait(), timeout=5)
                except asyncio.TimeoutError:
                    logger.warning("ACP process did not terminate in time; forcing kill")
                    self.process.kill()
                    await self.process.wait()
            except Exception as e:
                logger.error(f"Error stopping ACP process: {e}")

    async def _listen_loop(self):
        """Reads stdout line by line and parses JSON-RPC messages."""
        try:
            while self._is_active and self.process and self.process.stdout:
                line = await self.process.stdout.readline()
                if not line:
                    break
                
                try:
                    data = json.loads(line.decode().strip())
                    # Notification (no id) or Response (has id)
                    if "id" not in data:
                        # It's a notification (e.g., session/update)
                        await self._handle_notification(data)
                    else:
                        # It's a response to a request.
                        await self._handle_response(data)
                except json.JSONDecodeError:
                    logger.debug(f"Non-JSON output received: {line.decode().strip()}")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in ACP listen loop: {e}")

    def _route_to_ui(self, data: Dict[str, Any]):
        """Thread-safe helper to schedule the UI callback on the Textual app loop."""
        if self.app and hasattr(self.app, "call_next"):
            # Textual's call_next expects a callable with no arguments;
            # wrap the callback and its data in a closure.
            self.app.call_next(lambda: self.on_message(data))
        else:
            # Fallback for non-Textual or simple async usage
            if asyncio.iscoroutinefunction(self.on_message):
                asyncio.create_task(self.on_message(data))
            else:
                self.on_message(data)

    async def _handle_notification(self, data: Dict[str, Any]):
        """Routes notifications to the UI callback."""
        self._route_to_ui(data)

    async def _handle_response(self, data: Dict[str, Any]):
        """Resolves the pending future for the matching request ID.

        Responses are delivered only to the original requester via the pending
        Future. Notifications (messages without an id) are routed to on_message.
        This avoids duplicate UI updates while still making response errors
        visible when there is no waiter.
        """
        req_id = data.get("id")
        if req_id in self._pending:
            future = self._pending.pop(req_id)
            if not future.done():
                future.set_result(data)
            return

        # No pending waiter: surface the response (usually an error or stray
        # message) to the UI so it is not silently dropped.
        self._route_to_ui({"type": "response", "data": data})

    async def send_request(self, method: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Sends a JSON-RPC request and waits for the matching response."""
        self.request_id += 1
        rid = self.request_id
        request: ACPRequest = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": rid
        }
        
        if not self.process or not self.process.stdin:
            return None

        # Create future to wait for response
        future = asyncio.get_event_loop().create_future()
        self._pending[rid] = future

        self.process.stdin.write(json.dumps(request).encode() + b"\n")
        await self.process.stdin.drain()
        
        try:
            return await asyncio.wait_for(future, timeout=10)
        except asyncio.TimeoutError:
            self._pending.pop(rid, None)
            logger.error(f"ACP request {method} timed out (id={rid})")
            return None

    async def initialize(self, protocol_version: int = 1):
        """Performs the ACP handshake: initialize."""
        return await self.send_request("initialize", {
            "protocolVersion": protocol_version,
            "clientInfo": {"name": "NexusByTaeng", "version": "0.1.0"}
        })

    async def create_session(self, cwd: str):
        """Performs the ACP handshake: session/new."""
        return await self.send_request("session/new", {"cwd": cwd, "mcpServers": []})

    async def prompt(self, text: str):
        """Sends a prompt to the agent."""
        if not self.session_id:
            raise RuntimeError("Session not initialized")
        
        return await self.send_request("session/prompt", {
            "sessionId": self.session_id,
            "prompt": [{"type": "text", "text": text}]
        })

    def set_session_id(self, session_id: str):
        self.session_id = session_id
