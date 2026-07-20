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

    def compose(self):
        if self.sender == "system":
            # System messages: No prefix, No bubble
            self.add_class("msg-container")
            self.add_class("sys-msg")
            # Shell output is left-aligned, system notifications are center-aligned
            bubble_class = "shell-text" if self.is_shell else "sys-text"
            yield Static(self.text, classes=bubble_class)
        elif self.sender == "user":
            self.add_class("msg-container")
            self.add_class("user-msg")
            yield Static(f"User ❯ {self.text}", classes="user-text")
        elif self.sender == "ai":
            self.add_class("msg-container")
            self.add_class("ai-msg")
            yield Static(f"AI ❯ {self.text}", classes="ai-text")
        else:
            # Fallback for unknown sender
            self.add_class("msg-container")
            yield Static(self.text)
