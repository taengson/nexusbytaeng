from enum import Enum, auto
from typing import List, Callable, Dict, Any, Optional
import subprocess
import os
from pathlib import Path

class InputMode(Enum):
    NORMAL = auto()
    SHELL = auto()
    COMMAND = auto()
    SUGGESTION = auto()

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

class CommandHandler:
    def __init__(self):
        self.commands: Dict[str, Callable[[str], Any]] = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register("help", lambda _: "Available commands:\n/help  - Show this help menu\n/clear - Clear the chat history\n/exit  - Close the application")
        self.register("clear", lambda _: "Chat history cleared.")
        self.register("exit", lambda _: "Exiting...")

    def register(self, name: str, callback: Callable[[str], Any]):
        self.commands[name] = callback

    def handle(self, command_text: str) -> str:
        parts = command_text.strip().split(maxsplit=1)
        cmd_name = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd_name in self.commands:
            return str(self.commands[cmd_name](args))
        return f"Unknown command: {cmd_name}"

    def get_suggestions(self, partial: str) -> List[str]:
        return [f"/{name}" for name in self.commands.keys() if name.startswith(partial)]

class PathSuggester:
    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir

    def suggest(self, partial: str) -> List[str]:
        # ponytail: simple glob search for path suggestions
        try:
            search_path = os.path.join(self.root_dir, partial + "*")
            matches = Path(search_path).glob("*")
            return [str(p).replace(self.root_dir, "") for p in matches]
        except Exception:
            return []

class InputDispatcher:
    def __init__(self):
        self.mode = InputMode.NORMAL
        self.shell = ShellExecutor()
        self.commands = CommandHandler()
        self.paths = PathSuggester()

    def dispatch(self, text: str) -> tuple[InputMode, str]:
        if self.mode == InputMode.SHELL:
            res = self.shell.execute(text)
            if text.strip() == "exit":
                self.mode = InputMode.NORMAL
                return InputMode.NORMAL, "Exited shell mode."
            return InputMode.SHELL, res

        if text.startswith("!"):
            return InputMode.SHELL, "SHELL_CONFIRMATION_REQUIRED"
        
        if text.startswith("/"):
            self.mode = InputMode.COMMAND
            res = self.commands.handle(text[1:])
            self.mode = InputMode.NORMAL
            return InputMode.NORMAL, res
        
        if text.startswith("@"):
            self.mode = InputMode.SUGGESTION
            suggestions = self.paths.suggest(text[1:])
            return InputMode.SUGGESTION, ",".join(suggestions)
        
        self.mode = InputMode.NORMAL
        return InputMode.NORMAL, text

    def get_suggestions(self, text: str) -> tuple[Optional[str], List[str]]:
        """Returns (guide_text, suggestion_list) based on current input."""
        if text.startswith("/"):
            partial = text[1:]
            return "Available Commands:", self.commands.get_suggestions(partial)
        elif text.startswith("@"):
            partial = text[1:]
            return "Suggested Paths:", self.paths.suggest(partial)
        return None, []

