from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import typer
from typer.rich_utils import RichHelpFormatter

console = Console()

class AstralHelpFormatter(RichHelpFormatter):
    def write_usage(self, prog, args="", prefix="USAGE: "):
        prefix_text = Text(prefix, style="bold cyan")
        usage_text = Text(f"{prog} {args}", style="white")
        self.write(prefix_text + usage_text)

    def write_heading(self, heading):
        heading_text = Text(heading.upper(), style="bold magenta")
        self.write(heading_text)

    def write(self, text):
        super().write(text)

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
        kwargs.setdefault("formatter_class", AstralHelpFormatter)
        super().__init__(*args, **kwargs)