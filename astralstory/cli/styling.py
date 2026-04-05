from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import typer

console = Console()

def astral_panel(title: str):
    return Panel(
        Text(title, justify="center", style="bold cyan"),
        border_style="cyan",
        padding=(1, 2),
    )

class AstralTyper(typer.Typer):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("help", "AstralStory CLI — Cinematic Creative Engine")
        kwargs.setdefault("rich_markup_mode", "rich")
        super().__init__(*args, **kwargs)