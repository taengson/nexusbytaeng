import asyncio
import shlex
import sys
import os

class AgentProcessManager:
    def __init__(self, command: str, callback):
        self.command = command
        self.callback = callback
        self.process = None

    async def start(self):
        env = {**os.environ, "PYTHONUNBUFFERED": "1"}
        # Avoid create_subprocess_shell to prevent command injection when the
        # command originates from external configuration. Split safely with shlex.
        command_parts = shlex.split(self.command)
        if not command_parts:
            raise ValueError("Agent command is empty")
        self.process = await asyncio.create_subprocess_exec(
            *command_parts,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )
        asyncio.create_task(self._read_stream(self.process.stdout))
        asyncio.create_task(self._read_stream(self.process.stderr))

    async def _read_stream(self, stream):
        while True:
            try:
                chunk = await stream.read(1024)
                if not chunk:
                    break
                text = chunk.decode()
                self.callback(text)
            except Exception:
                break

    async def send(self, text: str):
        if self.process and self.process.stdin:
            self.process.stdin.write(text.encode() + b"\n")
            await self.process.stdin.drain()

    async def stop(self):
        if self.process:
            self.process.terminate()
            await self.process.wait()
