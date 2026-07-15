# ponytail: Simple wrap around DirectoryTree for modular project file list

import os
from textual.widgets import DirectoryTree, Static
from textual.containers import Container

class ProjectTreePanel(Container):
    """Left-side panel showing the project file tree."""
    
    def compose(self):
        yield Static("📂 PROJECT EXPLORER", id="project-header")
        # Defaults to the current working directory (workspace root)
        yield DirectoryTree(os.getcwd(), id="project-tree")
