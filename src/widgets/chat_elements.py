# ponytail: Simple design for chat message bubbles

from textual.widgets import Static
from textual.containers import Container

class MessageWidget(Container):
    """A card-style message bubble representing a chat turn."""
    
    def __init__(self, sender: str, text: str, is_shell: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.sender = sender  # 'user', 'ai', 'system'
        self.text = text
        self.is_shell = is_shell

    def compose(self):
        if self.sender == "user":
            self.add_class("msg-container")
            self.add_class("user-msg")
            yield Static(self.text, classes="message-bubble user-bubble")
        elif self.sender == "ai":
            self.add_class("msg-container")
            self.add_class("ai-msg")
            yield Static(self.text, classes="message-bubble ai-bubble")
        else:
            # System messages: No bubble
            self.add_class("msg-container")
            self.add_class("sys-msg")
            # Shell output is left-aligned, system notifications are center-aligned
            bubble_class = "shell-text" if self.is_shell else "sys-text"
            yield Static(self.text, classes=bubble_class)
