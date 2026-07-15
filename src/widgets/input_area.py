# ponytail: Custom InputArea with interactive QuickSettings overlay

from textual.widgets import Input, Button, Static
from textual.containers import Container
from textual.message import Message
from src.core.state import ConnectionMode

class InputArea(Container):
    """The unified input container featuring the status indicator."""
    
    class ModeChanged(Message):
        """Fired when user changes the active connection mode."""
        def __init__(self, mode: str):
            super().__init__()
            self.mode = mode

    def __init__(self, initial_mode: str = ConnectionMode.LOCAL, **kwargs):
        super().__init__(**kwargs)
        self.current_mode = initial_mode

    def compose(self):
        self.id = "input-container"
        yield Input(placeholder="메시지를 입력하세요...", id="input-field")
        yield Static("현재 연결: 로컬 AI 연결", id="status-bar")

    def on_mount(self):
        # Setup initial design states based on default mode
        self.apply_mode_style(self.current_mode)

    def apply_mode_style(self, mode: str):
        """Updates the style classes, placeholder texts, and indicators of the input area."""
        # Clean current styling classes
        for m in [ConnectionMode.LOCAL, ConnectionMode.NETWORK, ConnectionMode.GEMINI, ConnectionMode.OPENCODE]:
            self.remove_class(f"input-mode-{m}")
            
        # Add new styling class corresponding to active mode
        self.add_class(f"input-mode-{mode}")
        
        # Retrieve display visual traits
        display_name = ConnectionMode.get_display_name(mode)
        _, _, symbol = ConnectionMode.get_theme_color(mode)
        
        # Apply placeholder transformation
        input_field = self.query_one("#input-field", Input)
        input_field.placeholder = f"{symbol} [{display_name}] 메시지를 입력해 보세요..."
        
        # Apply info text transformation
        status_bar = self.query_one("#status-bar", Static)
        status_bar.update(f"현재 연결: {symbol} {display_name} | 대화 전송: Enter")
