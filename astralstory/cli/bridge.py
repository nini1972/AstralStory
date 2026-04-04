import typer
from rich.console import Console
from astralstory.engine.bridge_engine import sync_bridge

bridge_app = typer.Typer(help="AstralBridge sync and status tools")
console = Console()


@bridge_app.command("sync")
def sync(target: str):
    """Sync AstralStory with a target system (e.g., Mars kernel)."""
    status = sync_bridge(target)
    console.print_json(data=status)
