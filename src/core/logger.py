import os
from datetime import datetime

class ChatLogManager:
    """Manages real-time markdown logging of all workspace interactions including User, AI, Shell, and System events."""
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def _get_log_file_path(self) -> str:
        date_str = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.log_dir, f"chat_log_{date_str}.md")

    def start_session(self) -> None:
        """Marks the beginning of a new session in the log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"\n--- Session Started at [{timestamp}] ---\n"
        self._write_to_file(log_entry)

    def log_event(self, category: str, role: str, message: str) -> None:
        """
        Logs an event based on category.
        category: 'user', 'ai', 'shell', 'system'
        role: The display name (e.g., '나', 'AI', 'Shell', '[System]')
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        # category is used for internal tagging, role is for display
        log_entry = f"[{timestamp}] [{category.upper()}] {role}: {message}\n"
        self._write_to_file(log_entry)

    def _write_to_file(self, entry: str) -> None:
        try:
            with open(self._get_log_file_path(), "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            print(f"Logging error: {e}")
