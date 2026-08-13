from textual.widgets import Static, ListItem, ListView
from textual.containers import Vertical
from textual.app import ComposeResult
from textual.widgets import Label

class SuggestionPanel(Static):
    """A floating panel to show suggestions for commands and paths with keyboard navigation."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hidden = True
        self._list = None
        self._guide = None

    def compose(self) -> ComposeResult:
        self._guide = Label("", id="suggestion-guide")
        self._list = ListView(id="suggestion-list")
        yield self._guide
        yield self._list

    def update_suggestions(self, guide: str, suggestions: list[str]):
        self._guide.update(guide)
        self._list.clear()
        if not suggestions:
            self._list.append(ListItem(Label("No suggestions found")))
        else:
            for s in suggestions:
                self._list.append(ListItem(Label(s)))
        self.hidden = False
        self.display = True

    def hide(self):
        self.hidden = True
        self.display = False

    def get_selected(self) -> str | None:
        if self._list.index is not None:
            try:
                item = self._list.children[self._list.index]
                return item.query_one(Label).renderable
            except (IndexError, Exception):
                return None
        return None
