import typer
from astralstory.cli.styling import AstralTyper, astral_panel
from .scene import scene_app
from .world import world_app
from .agent import agent_app
from .bridge import bridge_app
from rich.console import Console
from astralstory.cli.state import state


console = Console()

app = AstralTyper(help="AstralStory CLI — Cinematic Creative Engine")

@app.callback()
def main(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable detailed diagnostic output."
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress banners and non-essential output."
    )
):
    """
    Global options for AstralStory CLI.
    """
    state.verbose = verbose
    state.quiet = quiet

    if not quiet:
        console.print(astral_panel("ASTRALSTORY — OPERATOR CONSOLE"))

app.add_typer(scene_app, name="scene")
app.add_typer(world_app, name="world")
app.add_typer(agent_app, name="agent")
app.add_typer(bridge_app, name="bridge")

def run():
    app()
