# ponytail: Custom InputArea with interactive QuickSettings overlay

from textual.widgets import Input, Button, Static
from textual.containers import Container
from textual.message import Message
from src.core.state import ConnectionMode
from src.core.input_engine import InputDispatcher, InputMode
from src.widgets.modals import ConfirmationModal
from src.widgets.suggestions import SuggestionPanel

class InputResult(Message):
    """Fired when an input action (Shell, Command, etc.) produces a result to be displayed."""
    def __init__(self, text: str, sender: str = "ai", is_shell: bool = False):
        super().__init__()
        self.text = text
        self.sender = sender  # 'user', 'ai', 'system'
        self.is_shell = is_shell

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
        self.dispatcher = InputDispatcher()

    def update_input_mode_style(self, mode: InputMode):
        """Updates the CSS classes of the input container based on the active input mode."""
        for m in InputMode:
            self.remove_class(f"input-engine-mode-{m.name.lower()}")
        self.add_class(f"input-engine-mode-{mode.name.lower()}")

    def update_mode_visuals(self, mode: InputMode):
        """Unifies placeholder and status bar updates based on the active input mode."""
        input_field = self.query_one("#input-field", Input)
        status_bar = self.query_one("#status-bar", Static)
        
        if mode == InputMode.SHELL:
            input_field.placeholder = "🐚 Shell 모드: 명령어를 입력하세요 (exit로 종료)"
            status_bar.update("✅ Shell 모드 진입 완료")
        else:
            # Reset to ConnectionMode style
            display_name = ConnectionMode.get_display_name(self.current_mode)
            _, _, symbol = ConnectionMode.get_theme_color(self.current_mode)
            input_field.placeholder = f"{symbol} [{display_name}] 메시지를 입력해 보세요..."
            status_bar.update(f"현재 연결: {symbol} {display_name} | 대화 전송: Enter")

    def compose(self):
        self.id = "input-container"
        yield Input(placeholder="메시지를 입력하세요...", id="input-field")
        yield Static("! shell mode", id="input-guide")
        yield Static("현재 연결: 로컬 AI 연결", id="status-bar")

    def on_input_submitted(self, event: Input.Submitted):
        text = event.value
        if not text:
            return

        # Capture current mode before dispatching to detect transitions
        previous_mode = self.dispatcher.mode
        mode, result = self.dispatcher.dispatch(text)
        
        # Clear input immediately for all dispatched actions (Shell, Command, etc.)
        self.query_one("#input-field", Input).value = ""

        if result == "SHELL_CONFIRMATION_REQUIRED":
            self.update_input_mode_style(InputMode.NORMAL)
            self.update_mode_visuals(InputMode.NORMAL)
            self.app.push_screen(
                ConfirmationModal(
                    title="Shell Mode Transition",
                    message="Entering shell mode will execute all following inputs as system commands. Continue?",
                    on_confirm=self.enter_shell_mode
                )
            )
            return

        # Handle Shell Mode and Shell Exit
        if previous_mode == InputMode.SHELL:
            if text.strip().lower() == "exit":
                self.update_input_mode_style(InputMode.NORMAL)
                self.update_mode_visuals(InputMode.NORMAL)
                self.post_message(InputResult(text="🐚 Shell 모드에서 종료되었습니다.", sender="system", is_shell=False))
                event.stop()
                return
            
            # Handle other shell outputs
            self.update_input_mode_style(InputMode.SHELL)
            self.update_mode_visuals(InputMode.SHELL)
            # First send the command the user typed
            self.post_message(InputResult(text=text, sender="user", is_shell=True))
            # Then send the result
            self.post_message(InputResult(text=f"🐚 Shell Output:\n{result}", sender="system", is_shell=True))
            event.stop()
            return

        # Handle Normal Mode
        self.update_input_mode_style(InputMode.NORMAL)
        self.update_mode_visuals(InputMode.NORMAL)
        
        # Do not log user input if it's a system command (starts with '!')
        if not text.startswith("!"):
            self.post_message(InputResult(text=text, sender="user"))
        
        if result and result != text:
            # If the dispatcher produced a distinct result, it's an AI response
            self.post_message(InputResult(text=result, sender="ai"))
        
        # Prevent the event from bubbling up to SessionWorkspace to avoid duplicate handling
        event.stop()


    def on_input_changed(self, event: Input.Changed):
        """Real-time suggestion trigger based on input prefix."""
        pass

    def enter_shell_mode(self):
        self.dispatcher.mode = InputMode.SHELL
        self.update_input_mode_style(InputMode.SHELL)
        self.update_mode_visuals(InputMode.SHELL)
        self.post_message(InputResult(text="🐚 Shell 모드에 진입했습니다. (exit로 종료)", sender="system", is_shell=False))

    def on_mount(self):
        # Setup initial design states based on default mode
        self.apply_mode_style(self.current_mode)
        # Map the Input widget to the on_change handler
        self.query_one("#input-field", Input).on_change = self.on_input_changed

    def apply_mode_style(self, mode: str):
        """Updates the style classes, placeholder texts, and indicators of the input area."""
        # Clean current styling classes
        for m in [ConnectionMode.LOCAL, ConnectionMode.NETWORK, ConnectionMode.GEMINI_ACP, ConnectionMode.OPENCODE]:
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
