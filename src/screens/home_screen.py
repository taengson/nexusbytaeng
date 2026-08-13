# ponytail: Beautiful HomeScreen / HomeView containing the 4 required entrance options

from textual.widgets import Button, Static
from textual.containers import Container
from src.core.state import ConnectionMode

# Ordered, data-driven button definitions to keep compose and handler in sync.
HOME_BUTTONS = [
    ("btn-network", ConnectionMode.NETWORK),
    ("btn-gemini", ConnectionMode.GEMINI_ACP),
    ("btn-hermes", ConnectionMode.HERMES_ACP),
    ("btn-opencode", ConnectionMode.OPENCODE_ACP),
]

class HomeScreen(Container):
    """Landing screen featuring the centralized connection mode selector menu."""

    def compose(self):
        with Container(id="home-container"):
            yield Static("NEXUS BY TAENG", id="home-title")
            yield Static("AI-Network TUI Hybrid Workspace", id="home-subtitle")

            for btn_id, mode in HOME_BUTTONS:
                _, _, symbol = ConnectionMode.get_theme_color(mode)
                display_name = ConnectionMode.get_display_name(mode)
                yield Button(f"{symbol} {display_name}", id=btn_id, classes="menu-button")

    def on_button_pressed(self, event: Button.Pressed):
        mode_map = {btn_id: mode for btn_id, mode in HOME_BUTTONS}
        selected_mode = mode_map.get(event.button.id)
        if selected_mode:
            # Transfer the application state into the SessionView screen
            self.app.enter_session(selected_mode)
