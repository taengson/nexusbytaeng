from enum import Enum, auto
from typing import List, Callable, Dict, Any, Optional
import subprocess
import os
from pathlib import Path

class InputMode(Enum):
    NORMAL = auto()
    SHELL = auto()

class ShellExecutor:
    def execute(self, command: str) -> str:
        try:
            result = subprocess.run(
                command, 
                shell=True, 
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
            res = self.shell.execute(text)
            if text.strip() == "exit":
                self.mode = InputMode.NORMAL
                return InputMode.NORMAL, "Exited shell mode."
            return InputMode.SHELL, res

        if text.startswith("!"):
            return InputMode.SHELL, "SHELL_CONFIRMATION_REQUIRED"
        
        self.mode = InputMode.NORMAL
        return InputMode.NORMAL, text

    def get_suggestions(self, text: str) -> tuple[Optional[str], List[str]]:
        return None, []

