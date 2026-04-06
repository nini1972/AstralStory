import typer
from astralstory.cli.styling import AstralTyper, astral_panel
from .scene import scene_app
from .world import world_app
from .agent import agent_app
from .bridge import bridge_app
from rich.console import Console
from astralstory.cli.state import state
from astralstory.cli.animation import run_startup_animation
from .diagnostics import diagnostics_app
from .dashboard import dashboard_app
from .shell import shell_app


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
    ),
    fast_boot: bool = typer.Option(False, "--fast-boot", "-f", help="Skip startup animation but show banner.")

):
    """
    Global options for AstralStory CLI.
    """
    state.verbose = verbose
    state.quiet = quiet
    state.fast_boot = fast_boot

    if quiet:
        return
    else:
        if not fast_boot:
            run_startup_animation()
        console.print(astral_panel("ASTRALSTORY — OPERATOR CONSOLE"))

app.add_typer(scene_app, name="scene")
app.add_typer(world_app, name="world")
app.add_typer(agent_app, name="agent")
app.add_typer(bridge_app, name="bridge")
app.add_typer(diagnostics_app, name="diagnostics")
app.add_typer(dashboard_app, name="dashboard")
app.add_typer(shell_app, name="shell")

def run():
    app()
