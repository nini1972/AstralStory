import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from astralstory.cli.styling import AstralTyper, astral_panel
from astralstory.cli.state import state
from astralstory.engine.scene_engine import generate_scene
from astralstory.engine.world_engine import build_world
from astralstory.engine.agent_engine import run_agent
from astralstory.engine.bridge_engine import sync_bridge
from astralstory.cli.diagnostics import gather_diagnostics

shell_app = AstralTyper(help="Interactive AstralStory operator shell.")

console = Console()

HELP_TEXT = """\
[bold cyan]AstralStory Operator Shell — Available Commands[/bold cyan]

  [cyan]scene[/cyan] [italic]<character> <emotion>[/italic]   Generate a cinematic scene
  [cyan]world[/cyan] [italic]<template>[/italic]              Build a world from a template
  [cyan]agent[/cyan] [italic]<mission...>[/italic]            Run an agent on a mission
  [cyan]bridge[/cyan] [italic]<target>[/italic]               Sync with an external system
  [cyan]diag[/cyan]                           Run a quick diagnostics check
  [cyan]help[/cyan]                           Show this help message
  [cyan]exit[/cyan] / [cyan]quit[/cyan]                    Exit the shell

[dim]All activity is logged to logs/engine.log and visible on the dashboard.[/dim]
"""

COMMAND_USAGE: dict[str, tuple[str, str]] = {
    "scene":       ("<character> <emotion>", "Generate a cinematic scene"),
    "world":       ("<template>",            "Build a world from a template"),
    "agent":       ("<mission...>",          "Run an agent on a mission"),
    "bridge":      ("<target>",              "Sync with an external system"),
    "diag":        ("",                      "Run a quick diagnostics check"),
    "help":        ("",                      "Show this help message"),
    "exit / quit": ("",                      "Exit the shell"),
}


def _cmd_scene(args: list[str]) -> None:
    if len(args) < 2:
        console.print("[yellow]Usage: scene <character> <emotion>[/yellow]")
        return
    console.print_json(data=generate_scene(args[0], args[1]))


def _cmd_world(args: list[str]) -> None:
    if not args:
        console.print("[yellow]Usage: world <template>[/yellow]")
        return
    console.print_json(data=build_world(args[0]))


def _cmd_agent(args: list[str]) -> None:
    if not args:
        console.print("[yellow]Usage: agent <mission...>[/yellow]")
        return
    console.print_json(data=run_agent(" ".join(args)))


def _cmd_bridge(args: list[str]) -> None:
    if not args:
        console.print("[yellow]Usage: bridge <target>[/yellow]")
        return
    console.print_json(data=sync_bridge(args[0]))


def _cmd_diag(_args: list[str]) -> None:
    console.print(gather_diagnostics())


def _cmd_help(_args: list[str]) -> None:
    console.print(Panel(Text.from_markup(HELP_TEXT), border_style="cyan"))


COMMANDS: dict[str, object] = {
    "scene": _cmd_scene,
    "world": _cmd_world,
    "agent": _cmd_agent,
    "bridge": _cmd_bridge,
    "diag": _cmd_diag,
    "help": _cmd_help,
}


def _dispatch(line: str) -> bool:
    """Parse and execute one shell line. Returns False to signal exit."""
    parts = line.strip().split()
    if not parts:
        return True

    cmd, args = parts[0].lower(), parts[1:]

    if cmd in ("exit", "quit"):
        return False

    handler = COMMANDS.get(cmd)
    if handler is None:
        console.print(f"[red]Unknown command:[/red] {cmd}  (type [cyan]help[/cyan] for available commands)")
        return True

    handler(args)  # pylint: disable=not-callable
    return True


@shell_app.command("run")
def run_shell():
    """
    Launch the interactive AstralStory operator shell.

    Type commands directly without flags. All engine activity is logged
    to logs/engine.log and visible on the live dashboard.

    Example:
        astralstory shell run
    """
    if state.quiet:
        console.print("Shell disabled in quiet mode.")
        raise typer.Exit()

    if not state.quiet:
        console.print(astral_panel("ASTRALSTORY OPERATOR SHELL"))
        console.print("[dim]Type [cyan]help[/cyan] for commands, [cyan]exit[/cyan] to quit.[/dim]\n")

    while True:
        try:
            line = input("\u25b6 ")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[cyan]Shell terminated.[/cyan]")
            break

        if not _dispatch(line):
            console.print("[cyan]Goodbye.[/cyan]")
            break
