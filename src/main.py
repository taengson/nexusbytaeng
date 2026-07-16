# ponytail: Minimal main entry point for NexusByTaeng App

from textual.app import App
from textual.widgets import TabbedContent, TabPane, Footer, Static
from textual.containers import Container
from src.widgets.session_workspace import SessionWorkspace
from src.widgets.project_tree import ProjectTreePanel
from src.core.state import ConnectionMode
from src.screens.home_screen import HomeScreen

class NexusApp(App):
    """The central coordinator for the NexusByTaeng Hybrid Chat TUI."""
    
    CSS_PATH = "styles/nexus.tcss"
    BINDINGS = [
        ("q", "quit", "앱 종료"),
        ("h", "go_home", "홈으로"),
    ]

    def compose(self):
        with Container(id="main-area"):
            yield HomeScreen(id="home-view")
            
            with Container(id="workspace-container", classes="hidden"):
                yield ProjectTreePanel(id="global-project-panel")
                yield TabbedContent(id="workspaces")
        yield Footer()

    def on_mount(self):
        pass

    def action_go_home(self):
        self.query_one("#home-view").display = True
        self.query_one("#workspace-container").display = False

    def enter_session(self, mode: str):
        self.query_one("#home-view").display = False
        container = self.query_one("#workspace-container")
        container.display = True
        
        workspaces = self.query_one("#workspaces", TabbedContent)
        
        tab_id = f"session-{workspaces.tab_count}"
        title = ConnectionMode.get_display_name(mode)
        
        workspaces.add_pane(TabPane(f"{title}", SessionWorkspace(mode), id=tab_id))
        workspaces.active = tab_id

if __name__ == "__main__":
    NexusApp().run()
