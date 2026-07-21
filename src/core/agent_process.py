import asyncio
import sys

class AgentProcessManager:
    def __init__(self, command: str, callback):
        self.command = command
        self.callback = callback
        self.process = None

    async def start(self):
        self.process = await asyncio.create_subprocess_shell(
            self.command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        asyncio.create_task(self._read_stream(self.process.stdout))
        asyncio.create_task(self._read_stream(self.process.stderr))

    async def _read_stream(self, stream):
        while True:
            try:
                chunk = await stream.read(1024)
                if not chunk:
                    break
                text = chunk.decode().strip()
                print(f"[DEBUG] AgentProcessManager: Raw chunk received, decoded text: {text}")
                self.callback(text)
            except Exception as e:
                print(f"[DEBUG] AgentProcessManager: Error reading stream: {e}")
                break

    async def send(self, text: str):
        if self.process and self.process.stdin:
            self.process.stdin.write(text.encode() + b"\n")
            await self.process.stdin.drain()

    async def stop(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()
