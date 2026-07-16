from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Button
from textual.containers import Vertical

class ConfirmationModal(ModalScreen):
    """A simple modal for confirming critical actions like Shell Mode transition."""
    
    def __init__(self, title: str, message: str, on_confirm: callable, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.message = message
        self.on_confirm = on_confirm

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm-modal-container"):
            yield Label(self.title, id="confirm-modal-title")
            yield Label(self.message, id="confirm-modal-text")
            with Vertical(id="confirm-modal-buttons"):
                yield Button("Confirm", id="confirm-yes", variant="success")
                yield Button("Cancel", id="confirm-no", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm-yes":
            self.on_confirm()
            self.app.pop_screen()
        elif event.button.id == "confirm-no":
            self.app.pop_screen()
