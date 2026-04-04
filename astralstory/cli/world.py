import typer
from rich.console import Console
from astralstory.engine.world_engine import build_world

world_app = typer.Typer(help="World building and export tools")
console = Console()


@world_app.command("build")
def build(template: str):
    """Build a world from a template."""
    world = build_world(template)
    console.print_json(data=world)
