import typer
from rich.console import Console
from typer.cli import state
from astralstory.cli import scene
from astralstory.engine.bridge_engine import sync_bridge
from astralstory.cli.styling import AstralTyper, astral_panel

bridge_app = AstralTyper(
    help="Synchronize AstralStory with external systems and mission kernels."
)
console = Console()

@bridge_app.command("sync")
def sync(
    target: str = typer.Option(
        ...,
        "--target",
        "-t",
        help="Target system to synchronize with (e.g., 'mars-kernel', 'astral-bridge')."
    )
):
    """
    Synchronize AstralStory data with an external system.

    This command ensures deterministic alignment between AstralStory and
    connected mission kernels or bridge systems.

    Example:
        astralstory bridge sync --target mars-kernel
    """
    if not state.quiet:
                console.print(astral_panel("BRIDGE SYNCHRONIZATION"))

    if state.verbose:
            console.log("[cyan]Synchronizing bridge with detailed diagnostics...[/cyan]")

    status = sync_bridge(target)

    if state.verbose:
            console.log(f"[magenta]Bridge data: {status}[/magenta]")

    console.print_json(data=status)


   