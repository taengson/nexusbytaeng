# ponytail: Independent SessionWorkspace widget for TabbedContent

import asyncio
from textual.widgets import Input, Static
from textual.containers import Container, VerticalScroll
from textual.message import Message
from src.widgets.project_tree import ProjectTreePanel
from src.widgets.chat_elements import MessageWidget
from src.widgets.input_area import InputArea, InputResult
from src.core.state import ConnectionMode
from typing import Dict, Any
from src.core.acp import ACPClient
from src.core.logger import ChatLogManager

class SessionWorkspace(Container):
    """The workspace session widget, intended for mounting in tabs."""
    
    def __init__(self, initial_mode: str = ConnectionMode.LOCAL, **kwargs):
        super().__init__(**kwargs)
        self.current_mode = initial_mode
        self.agent_manager = None
        self.acp_client = None
        self.logger = ChatLogManager()
        self._active_ai_widget = None
        self._current_response_buffer = ""
        self._logging_timer = None
        self._logging_token = 0

    def update_last_ai_message(self, text: str, sender: str = "ai"):
        """Appends text to the active AI message widget to support streaming."""
        if self._active_ai_widget and self._active_ai_widget.sender == sender:
            self._active_ai_widget.append_text(text + " ")
        else:
            # Create a new message widget and track it
            self.add_message(sender, text)
            # Find the widget we just added to set as active
            message_list = self.query_one("#message-list", VerticalScroll)
            for w in reversed(message_list.children):
                if isinstance(w, MessageWidget) and w.sender == sender:
                    self._active_ai_widget = w
                    break

    def compose(self):
        # Right side: Chat workspace & Settings Input
        with Container(id="chat-panel"):
            yield VerticalScroll(id="message-list")
            # Status bar for ACP connection state
            yield Static(" ", id="acp-status-bar", classes="status-bar")
            yield InputArea(initial_mode=self.current_mode)

    async def on_mount(self):
        # Emit session initial status logs
        display_name = ConnectionMode.get_display_name(self.current_mode)
        self.logger.start_session(display_name)
        _, _, symbol = ConnectionMode.get_theme_color(self.current_mode)
        
        self.add_system_message(f"--- {symbol} {display_name} 워크스페이스 세션이 시작되었습니다 ---")
        self.add_system_message(
            "왼쪽의 파일 트리를 통해 실제 폴더 구조를 탐색할 수 있습니다. "
        )
        
        if self.current_mode == ConnectionMode.HERMES_ACP:
            # Use ACPClient for structured JSON-RPC communication
            self.input_area = self.query_one(InputArea)
            self.input_area.can_focus = False
            self.set_acp_status("⚡ ACP 핸드셰이크 진행 중... (잠시만 기다려 주세요)", "#94a3b8")
            self.add_system_message("🔄 ACP 연결 중...")
            
            try:
                self.acp_client = ACPClient(
                    command=["hermes", "acp"], 
                    on_message=self._handle_acp_message,
                    app_context=self.app
                )
                await self._connect_acp()
            except Exception as e:
                self.set_acp_status(f"❌ ACP 연결 실패: {e}", "#ef4444")
                self.add_system_message(f"❌ ACP 연결 실패: {e}\n홈 화면으로 돌아가거나 앱을 종료하십시오.")

        elif self.current_mode == ConnectionMode.GEMINI_ACP:
            # Use ACPClient for Gemini
            self.input_area = self.query_one(InputArea)
            self.input_area.can_focus = False
            self.set_acp_status("✨ Gemini 연결 중...", "#94a3b8")
            self.add_system_message("🔄 Gemini 연결 중...")
            
            try:
                self.acp_client = ACPClient(
                    command=["gemini", "--acp"], 
                    on_message=self._handle_acp_message,
                    app_context=self.app
                )
                await self._connect_acp()
            except Exception as e:
                self.set_acp_status(f"❌ Gemini 연결 실패: {e}", "#ef4444")
                self.add_system_message(f"❌ Gemini 연결 실패: {e}\n홈 화면으로 돌아가거나 앱을 종료하십시오.")

        elif self.current_mode == ConnectionMode.OPENCODE_ACP:
            # Use ACPClient for OpenCode
            self.input_area = self.query_one(InputArea)
            self.input_area.can_focus = False
            self.set_acp_status("💻 OpenCode 연결 중...", "#94a3b8")
            self.add_system_message("🔄 OpenCode 연결 중...")
            
            try:
                self.acp_client = ACPClient(
                    command=["opencode", "acp"], 
                    on_message=self._handle_acp_message,
                    app_context=self.app
                )
                await self._connect_acp()
            except Exception as e:
                self.set_acp_status(f"❌ OpenCode 연결 실패: {e}", "#ef4444")
                self.add_system_message(f"❌ OpenCode 연결 실패: {e}\n홈 화면으로 돌아가거나 앱을 종료하십시오.")

    async def _connect_acp(self):
        """Common ACP connection logic for Hermes and Gemini."""
        await self.acp_client.start()
        await self.acp_client.initialize()
        resp = await self.acp_client.create_session(cwd=".")
        
        if resp and "result" in resp:
            session_id = resp["result"].get("sessionId") or resp["result"].get("session_id")
            if session_id:
                self.acp_client.set_session_id(session_id)
                self.logger.log_event("system", "ACP", f"Session ID: {session_id}")
                mode_symbol = "✨" if self.current_mode == ConnectionMode.GEMINI_ACP else "⚡"
                self.set_acp_status(f"✅ ACP 연결됨 (ID: {session_id})", "#10b981")
                self.add_system_message(f"✅ ACP 연결됨 (session: {session_id})")
                self.input_area.can_focus = True
            else:
                self.set_acp_status("⚠️ ACP 세션 ID를 찾을 수 없습니다.", "#ef4444")
                self.add_system_message("⚠️ ACP 세션 ID를 찾을 수 없습니다.")
        else:
            self.set_acp_status("⚠️ ACP 응답 비정상", "#ef4444")
            self.add_system_message("⚠️ ACP 세션 생성 응답이 비정상적입니다.")

    def _finalize_ai_logging(self, token: int):
        """Logs the accumulated response buffer to the chat log.
        Uses token-based validation to ensure only the latest timer triggers logging."""
        if token != self._logging_token:
            return  # This timer was invalidated by a newer one
        if self._current_response_buffer:
            self.logger.log_event("ai", "AI", self._current_response_buffer)
            self._current_response_buffer = ""
        self._logging_timer = None

    def _handle_acp_message(self, data: Dict[str, Any]):
        """Handles JSON-RPC messages from ACPClient."""
        # 1. Handle Responses (Requests with ID)
        if data.get("type") == "response":
            resp = data.get("data", {})
            if resp.get("result") and "sessionId" in resp["result"]:
                self.acp_client.set_session_id(resp["result"]["sessionId"])
                self.add_system_message(f"✅ ACP 세션 활성화됨 (ID: {resp['result']['sessionId']})")
            elif resp.get("error"):
                self.add_system_message(f"⚠️ ACP 에러: {resp['error'].get('message', 'Unknown error')}")
            return
        
        # 2. Handle Notifications (e.g., session/update)
        method = data.get("method")
        params = data.get("params", {})

        if method == "session/update":
            # hermes acp는 sessionUpdate가 params["update"] 안에 둠
            update = params.get("update") or params
            update_type = update.get("sessionUpdate")
            content = update.get("content", {})
            
            if update_type == "agent_message_chunk":
                text = content.get("text", "")
                self.update_last_ai_message(text, sender="ai")
                self._current_response_buffer += text
                # Token-based timer invalidation: increment token, capture in lambda
                self._logging_token += 1
                token = self._logging_token
                self._logging_timer = self.set_timer(
                    2.0, 
                    lambda t=token: self._finalize_ai_logging(t)
                )
            elif update_type == "agent_thought_chunk":
                thought = content.get("text", "")
                # Only reset if current active widget is not a thought widget
                if not self._active_ai_widget or self._active_ai_widget.sender != "thought":
                    self._active_ai_widget = None
                self.update_last_ai_message(thought, sender="thought")
            elif update_type == "tool_call":
                tool_name = update.get('name') or update.get('toolName') or "Unknown Tool"
                self.add_system_message(f"🛠 Tool: {tool_name}")
            elif update_type == "tool_call_update":
                self.add_system_message(f"🛠 Result: {update.get('result')}")
        else:
            # Generic log for other notifications
            self.logger.log_event("system", "ACP", f"Notification {method}: {params}")


    def on_input_result(self, message: InputResult):
        """Handles results from shell, commands, and suggestions routed via InputArea."""
        if self.current_mode in (ConnectionMode.HERMES_ACP, ConnectionMode.GEMINI_ACP, ConnectionMode.OPENCODE_ACP) and message.sender == "user" and not message.is_shell:
            # Flush remaining AI response buffer before starting new exchange
            if self._current_response_buffer:
                self.logger.log_event("ai", "AI", self._current_response_buffer)
                self._current_response_buffer = ""
            
            # Clear buffer and active widget for a new exchange
            self._active_ai_widget = None
            
            self.add_message(message.sender, message.text)
            self.logger.log_event("user", "나", message.text)
            if self.acp_client:
                asyncio.create_task(self.acp_client.prompt(message.text))
        else:
            if message.is_shell and message.sender == "user":
                # Shell command input — display and log the command
                self.add_message("user", f"🐚 > {message.text}")
                self.logger.log_event("shell", "나", message.text)
            else:
                self.add_message(message.sender, message.text, is_shell=message.is_shell)
                category = "shell" if message.is_shell else "user"
                role = "Shell" if message.is_shell else "나"
                self.logger.log_event(category, role, message.text)

    def on_remove(self) -> None:
        """Flush remaining response buffer when session is closing."""
        if self._current_response_buffer:
            self.logger.log_event("ai", "AI", self._current_response_buffer)
            self._current_response_buffer = ""

    def on_input_area_mode_changed(self, message: InputArea.ModeChanged):
        """Reacts to connection switches from the InputArea settings."""
        self.current_mode = message.mode
        display_name = ConnectionMode.get_display_name(self.current_mode)
        _, _, symbol = ConnectionMode.get_theme_color(self.current_mode)
        
        # Log system event
        self.add_system_message(f"🔔 연결 인스턴스가 {symbol} {display_name}(으)로 조절되었습니다.")


    def on_input_submitted(self, event: Input.Submitted):
        """Triggers upon pressing Enter inside the message input."""
        # This is now fully handled by InputArea via global InputResult messages
        # to ensure consistent ordering and prevent duplicate messages.
        pass

        
        # Note: InputArea will handle the logic and post an InputResult message
        # if it's a command or shell execution.

    async def generate_mock_response(self, user_text: str):
        """Asynchronously triggers simulated response cards."""
        await asyncio.sleep(0.3)
        
        mock_responses = {
            ConnectionMode.LOCAL: f"🤖 [로컬 AI 응답]\n입력하신 쿼리 '{user_text}' 분석 완료.",
            ConnectionMode.NETWORK: f"🌐 [네트워크 응답]\n에코 패킷 수신 성공: '{user_text}'",
            ConnectionMode.GEMINI_ACP: f"✨ [Gemini 응답]\n구문 해석 성공.",
            ConnectionMode.OPENCODE_ACP: f"💻 [OpenCode 응답]\n프로젝트 컨텍스트 주입 완료."
        }
        
        response_text = mock_responses.get(self.current_mode, "시뮬레이션 데이터 수신 오류.")
        self.add_message("ai", response_text)

    def add_message(self, sender: str, text: str, is_shell: bool = False):
        """Mounts a message card and scrolls the viewport."""
        message_list = self.query_one("#message-list", VerticalScroll)
        message_list.mount(MessageWidget(sender, text, is_shell=is_shell))
        message_list.scroll_end(animate=False)

    def set_acp_status(self, text: str, color: str = "white"):
        """Updates the ACP connection status bar."""
        status_bar = self.query_one("#acp-status-bar", Static)
        status_bar.update(text)
        status_bar.styles.color = color

    def add_system_message(self, text: str):
        """Displays a system-level notification message in the chat list."""
        self.add_message("system", text)

