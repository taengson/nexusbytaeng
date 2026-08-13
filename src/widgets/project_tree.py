# ponytail: Simple wrap around DirectoryTree for modular project file list

import os
from textual.widgets import DirectoryTree, Static
from textual.containers import Container

class ProjectTreePanel(Container):
    """Left-side panel showing the project file tree."""

    def __init__(self, path: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self._path = path or os.getcwd()

    def compose(self):
        # Defaults to the current working directory (workspace root)
        yield DirectoryTree(self._path, id="project-tree")

    def update_path(self, path: str):
        """Rebuild the tree for a new directory path."""
        self._path = path
        tree = self.query_one("#project-tree", DirectoryTree)
        tree.path = path
