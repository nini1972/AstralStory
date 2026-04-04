import typer
from rich.console import Console
from astralstory.engine.agent_engine import run_agent
from astralstory.cli.styling import AstralTyper, astral_panel

agent_app = AstralTyper(
    help="Run, evaluate, and interact with AstralStory agents."
)
console = Console()

@agent_app.command("run")
def run(
    mission: str = typer.Option(
        ...,
        "--mission",
        "-m",
        help="Mission description the agent should execute (e.g., 'retrieve memory shard')."
    )
):
    """
    Execute an AstralStory agent on a specific mission.

    Missions are deterministic tasks that agents perform inside the AstralStory
    universe. Useful for testing, pipelines, and narrative automation.

    Example:
        astralstory agent run --mission \"retrieve memory shard\"
    """

    if not state.quiet:
            console.print(astral_panel("AGENT EXECUTION"))

    if state.verbose:
        console.log("[cyan]Executing agent with detailed diagnostics...[/cyan]")

    result = run_agent(mission)

    if state.verbose:
        console.log(f"[magenta]Agent result: {result}[/magenta]")

    console.print_json(data=result)
