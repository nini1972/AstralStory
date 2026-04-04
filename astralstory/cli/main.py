import typer
from .scene import scene_app
from .world import world_app
from .agent import agent_app
from .bridge import bridge_app

app = typer.Typer(help="AstralStory CLI — deterministic creative engine")

app.add_typer(scene_app, name="scene")
app.add_typer(world_app, name="world")
app.add_typer(agent_app, name="agent")
app.add_typer(bridge_app, name="bridge")


def run():
    app()
