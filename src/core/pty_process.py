import asyncio
import os
import pty
import select
import subprocess
from typing import Callable, Optional

class TtyProcessManager:
    """
    Manages a subprocess with a pseudo-terminal (PTY) to fool interactive CLI tools
    into thinking they are running in a real terminal.
    """
    def __init__(self, command: str, callback: Callable[[str], None]):
        self.command = command
        self.callback = callback
        self.process: Optional[subprocess.Popen] = None
        self.master_fd: Optional[int] = None
        self._read_task: Optional[asyncio.Task] = None

    async def start(self):
        """Starts the process with a PTY and begins reading the output stream."""
        # Create PTY
        self.master_fd, slave_fd = pty.openpty()
        
        # Start process with the slave end of PTY as stdin/stdout/stderr
        self.process = subprocess.Popen(
            self.command,
            shell=True,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            close_fds=True,
            text=False # Handle as bytes for PTY
        )
        
        # Close slave_fd in parent as it's now owned by the process
        os.close(slave_fd)
        
        # Start the async read loop
        self._read_task = asyncio.create_task(self._read_loop())

    async def _read_loop(self):
        """Asynchronously reads from the PTY master fd and triggers the callback."""
        loop = asyncio.get_running_loop()
        
        try:
            while True:
                # Use loop.run_in_executor or select to avoid blocking the event loop
                # Since PTY reads can be blocking, we use a small read with a timeout check
                # or leverage the fact that read(n) on a PTY is generally efficient.
                
                # For maximum stability in async, we can use a separate thread or 
                # a non-blocking read wrapper.
                data = await loop.run_in_executor(None, self._read_from_pty)
                if not data:
                    break
                
                # Decode and trigger callback
                self.callback(data.decode(errors='replace'))
                
        except Exception as e:
            print(f"[DEBUG] TtyProcessManager read loop error: {e}")
        finally:
            if self.master_fd:
                os.close(self.master_fd)

    def _read_from_pty(self) -> bytes:
        """Synchronous read from the PTY master fd."""
        try:
            # Read a chunk of data. PTY reads usually return what's available.
            return os.read(self.master_fd, 1024)
        except (OSError, IOError):
            return b""

    async def send(self, text: str):
        """Writes text to the PTY master fd."""
        if self.master_fd is not None:
            # PTY requires bytes. Ensure newline is present for CLI tools.
            full_text = text + "\n"
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, os.write, self.master_fd, full_text.encode())

    async def stop(self):
        """Terminates the process and cleans up PTY resources."""
        if self._read_task:
            self._read_task.cancel()
            
        if self.process:
            self.process.terminate()
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self.process.wait)
            
        if self.master_fd:
            os.close(self.master_fd)
            self.master_fd = None
