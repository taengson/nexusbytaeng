from enum import Enum, auto
from typing import List, Callable, Dict, Any, Optional
import subprocess
import shlex
import os
from pathlib import Path

class InputMode(Enum):
    NORMAL = auto()
    SHELL = auto()

class ShellExecutor:
    def execute(self, command: str) -> str:
        try:
            # Avoid shell=True to prevent command injection; parse with shlex.
            parts = shlex.split(command)
            if not parts:
                return ""
            result = subprocess.run(
                parts,
                shell=False,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error executing command: {str(e)}"

class InputDispatcher:
    def __init__(self):
        self.mode = InputMode.NORMAL
        self.shell = ShellExecutor()

    def dispatch(self, text: str) -> tuple[InputMode, str]:
        if self.mode == InputMode.SHELL:
            # Handle exit command before executing it in the shell.
            if text.strip().lower() == "exit":
                self.mode = InputMode.NORMAL
                return InputMode.NORMAL, "Exited shell mode."
            res = self.shell.execute(text)
            return InputMode.SHELL, res

        if text.startswith("!"):
            return InputMode.SHELL, "SHELL_CONFIRMATION_REQUIRED"

        self.mode = InputMode.NORMAL
        return InputMode.NORMAL, text

    def get_suggestions(self, text: str) -> tuple[Optional[str], List[str]]:
        """Return a guide label and a list of suggestions for the current input.

        - @ prefix suggests files/directories from the current working directory.
        - Other prefixes return no suggestions for now.
        """
        stripped = text.strip()
        if stripped.startswith("@"):
            query = stripped[1:].strip()
            directory = "."
            prefix = ""
            if "/" in query:
                directory = os.path.dirname(query) or "."
                prefix = os.path.basename(query)
            try:
                entries = sorted(os.listdir(directory))
                suggestions = [e for e in entries if e.startswith(prefix)] if prefix else entries
                return "파일/경로 제안", suggestions[:10]
            except Exception:
                return "파일/경로 제안", []
        return None, []

