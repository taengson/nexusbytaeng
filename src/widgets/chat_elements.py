# ponytail: Minimal text-based chat layout (no bubbles)

from textual.widgets import Static
from textual.containers import Container

class MessageWidget(Container):
    """A minimal text-based message representation."""
    
    def __init__(self, sender: str, text: str, is_shell: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.sender = sender  # 'user', 'ai', 'system'
        self.text = text
        self.is_shell = is_shell
        self._text_static = None

    def append_text(self, text: str):
        """Appends text to the internal static widget for streaming."""
        if self._text_static:
            self._text_static.update(self._get_formatted_text(self.text + text))
            self.text += text
        else:
            # If for some reason it's called before compose, just update the variable
            self.text += text

    def _get_formatted_text(self, text: str) -> str:
        if self.sender == "user":
            return f"User ❯ {text}"
        if self.sender == "ai":
            return f"AI ❯ {text}"
        return text

    def compose(self):
        if self.sender == "system":
            self.add_class("msg-container")
            self.add_class("sys-msg")
            bubble_class = "shell-text" if self.is_shell else "sys-text"
            self._text_static = Static(self.text, classes=bubble_class)
            yield self._text_static
        elif self.sender == "user":
            self.add_class("msg-container")
            self.add_class("user-msg")
            self._text_static = Static(self._get_formatted_text(self.text), classes="user-text")
            yield self._text_static
        elif self.sender == "ai":
            self.add_class("msg-container")
            self.add_class("ai-msg")
            self._text_static = Static(self._get_formatted_text(self.text), classes="ai-text")
            yield self._text_static
        else:
            self.add_class("msg-container")
            self._text_static = Static(self.text)
            yield self._text_static

