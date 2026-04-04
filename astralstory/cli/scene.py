import typer
from rich.console import Console
from astralstory.engine.scene_engine import generate_scene

scene_app = typer.Typer(help="Scene generation and refinement tools")
console = Console()


@scene_app.command("generate")
def generate(
    character: str = typer.Option(...),
    emotion: str = typer.Option(...),
):
    """Generate a cinematic scene for a character and emotion."""
    scene = generate_scene(character, emotion)
    console.print_json(data=scene)
