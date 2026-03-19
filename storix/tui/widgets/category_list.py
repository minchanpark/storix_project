"""Category list widget for the TUI left panel."""

from textual.widgets import ListView, ListItem
from textual.app import ComposeResult
from textual.widgets import Label

from storix.models.enums import Category
from storix.utils.size import format_size


CATEGORY_LABELS = {
    Category.ALL: "All",
    Category.XCODE: "Xcode",
    Category.ANDROID: "Android",
    Category.FLUTTER: "Flutter",
    Category.NODE: "Node/Web",
    Category.PYTHON: "Python",
    Category.VSCODE: "VS Code",
    Category.GENERAL: "General",
}


class CategoryList(ListView):
    """Left-panel category list."""

    DEFAULT_CSS = """
    CategoryList {
        width: 20;
        height: 100%;
        border-right: solid $primary;
    }
    CategoryList > ListItem {
        padding: 0 1;
    }
    CategoryList > ListItem.--highlight {
        background: $primary;
        color: $text;
    }
    """

    def __init__(self, category_sizes: dict[Category, int] | None = None, **kwargs):
        super().__init__(**kwargs)
        self._category_sizes = category_sizes or {}

    def compose(self) -> ComposeResult:
        for cat in [
            Category.ALL,
            Category.XCODE,
            Category.ANDROID,
            Category.FLUTTER,
            Category.NODE,
            Category.PYTHON,
            Category.VSCODE,
            Category.GENERAL,
        ]:
            label = CATEGORY_LABELS[cat]
            size = self._category_sizes.get(cat, 0)
            if size > 0 and cat != Category.ALL:
                label = f"{label} [{format_size(size)}]"
            item = ListItem(Label(label), id=f"cat-{cat.value}")
            yield item
