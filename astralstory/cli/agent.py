import typer
from rich.console import Console
from astralstory.engine.agent_engine import run_agent

agent_app = typer.Typer(help="Run and evaluate AstralStory agents")
console = Console()


@agent_app.command("run")
def run(mission: str):
    """Run an agent on a mission."""
    result = run_agent(mission)
    console.print_json(data=result)
