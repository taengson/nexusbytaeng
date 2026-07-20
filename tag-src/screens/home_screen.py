# ponytail: Beautiful HomeScreen / HomeView containing the 4 required entrance options

from textual.widgets import Button, Static
from textual.containers import Container
from src.core.state import ConnectionMode

class HomeScreen(Container):
    """Landing screen featuring the centralized connection mode selector menu."""
    
    def compose(self):
        with Container(id="home-container"):
            yield Static("NEXUS BY TAENG", id="home-title")
            yield Static("AI-Network TUI Hybrid Workspace", id="home-subtitle")
            
            yield Button("🤖 로컬 AI 연결", id="btn-local", classes="menu-button")
            yield Button("🌐 네트워크 연결", id="btn-network", classes="menu-button")
            yield Button("✨ GEMINI-CLI 연결", id="btn-gemini", classes="menu-button")
            yield Button("💻 OpenCode 연결", id="btn-opencode", classes="menu-button")

    def on_button_pressed(self, event: Button.Pressed):
        btn_id = event.button.id
        mode_map = {
            "btn-local": ConnectionMode.LOCAL,
            "btn-network": ConnectionMode.NETWORK,
            "btn-gemini": ConnectionMode.GEMINI,
            "btn-opencode": ConnectionMode.OPENCODE,
        }
        selected_mode = mode_map.get(btn_id)
        if selected_mode:
            # Transfer the application state into the SessionView screen
            self.app.enter_session(selected_mode)
