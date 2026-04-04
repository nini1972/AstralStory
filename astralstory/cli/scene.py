import typer
from rich.console import Console
from astralstory.engine.scene_engine import generate_scene
from astralstory.cli.styling import AstralTyper, astral_panel
from astralstory.cli.state import state


scene_app = AstralTyper(
    help="Generate and refine cinematic scenes within the AstralStory universe."
)
console = Console()

@scene_app.command("generate")
def generate(
    character: str = typer.Option(
        ...,
        "--character",
        "-c",
        help="Name of the character featured in the scene (e.g., 'luna')."
    ),
    emotion: str = typer.Option(
        ...,
        "--emotion",
        "-e",
        help="Primary emotion driving the scene (e.g., 'wonder', 'fear', 'hope')."
    ),
):
    """
    Generate a cinematic scene for a character and emotion.

    This command creates a deterministic scene description based on the
    character and emotional tone you provide. Ideal for pipelines, agent
    workflows, and narrative prototyping.

    Example:
        astralstory scene generate --character luna --emotion wonder
    """
    if not state.quiet:
            console.print(astral_panel("SCENE GENERATION"))

    if state.verbose:
        console.log("[cyan]Generating scene with detailed diagnostics...[/cyan]")

    scene = generate_scene(character, emotion)

    if state.verbose:
        console.log(f"[magenta]Scene data: {scene}[/magenta]")

    console.print_json(data=scene)
