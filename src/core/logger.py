import os
from datetime import datetime
from typing import List

class ChatLogManager:
    """Manages real-time markdown logging of all workspace interactions including User, AI, Shell, and System events.

    Writes are buffered in memory and flushed to disk periodically or on session end
    to reduce I/O overhead during high-frequency streaming events.
    """
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self._buffer: List[str] = []

    def _get_log_file_path(self) -> str:
        date_str = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.log_dir, f"chat_log_{date_str}.md")

    def start_session(self, mode_name: str = "Unknown") -> None:
        """Marks the beginning of a new session in the log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"\n--- Session Started at [{timestamp}] (Mode: {mode_name}) ---\n"
        self._buffer.append(log_entry)
        self.flush()

    def log_event(self, category: str, role: str, message: str) -> None:
        """
        Logs an event based on category.
        category: 'user', 'ai', 'shell', 'system'
        role: The display name (e.g., '나', 'AI', 'Shell', '[System]')
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        # category is used for internal tagging, role is for display
        log_entry = f"[{timestamp}] [{category.upper()}] {role}: {message}\n"
        self._buffer.append(log_entry)

    def flush(self) -> None:
        """Flushes the in-memory log buffer to disk."""
        if not self._buffer:
            return
        try:
            with open(self._get_log_file_path(), "a", encoding="utf-8") as f:
                f.write("".join(self._buffer))
            self._buffer.clear()
        except Exception as e:
            print(f"Logging error: {e}")

    def _write_to_file(self, entry: str) -> None:
        """Deprecated: kept for compatibility; prefer log_event + flush."""
        self._buffer.append(entry)
