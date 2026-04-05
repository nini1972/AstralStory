import typer
from rich.console import Console
from astralstory.engine.world_engine import build_world
from astralstory.cli.styling import AstralTyper, astral_panel
from astralstory.cli.state import state

world_app = AstralTyper(
    help="Tools for constructing, shaping, and exporting AstralStory worlds."
)
console = Console()

@world_app.command("build")
def build(
    template: str = typer.Option(
        ...,
        "--template",
        "-t",
        help="Name of the world template to use (e.g., 'nebula-garden', 'crystal-dunes')."
    )
):
    """
    Build a new world using a predefined template.

    This command constructs a fully deterministic world structure based on the
    selected template. Ideal for pipelines, agent workflows, and world previews.

    Example:
        astralstory world build --template nebula-garden
    """
    if not state.quiet:
        console.print(astral_panel("WORLD BUILDING"))

    if state.verbose:
        console.log("[cyan]Building world with detailed diagnostics...[/cyan]")

    world = build_world(template)

    if state.verbose:
        console.log(f"[magenta]World data: {world}[/magenta]")

    console.print_json(data=world)
