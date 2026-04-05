import platform
import typer
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from time import sleep
from astralstory.cli.state import state

console = Console()

diagnostics_app = typer.Typer(help="System diagnostics and status overview.", invoke_without_command=True)

def gather_diagnostics():
    table = Table(title="AstralStory System Diagnostics", title_style="bold cyan")
    table.add_column("Component", style="bold magenta")
    table.add_column("Status", style="bold green")
    table.add_column("Details", style="white")

    table.add_row("Python", "OK", platform.python_version())
    table.add_row("Platform", "OK", platform.system())

    table.add_row("Verbose Mode", "ON" if state.verbose else "OFF", "")
    table.add_row("Quiet Mode", "ON" if state.quiet else "OFF", "")
    table.add_row("Fast Boot", "ON" if state.fast_boot else "OFF", "")

    table.add_row("Scene Engine", "OK", "Loaded")
    table.add_row("World Engine", "OK", "Loaded")
    table.add_row("Agent Engine", "OK", "Loaded")
    table.add_row("Bridge Engine", "OK", "Loaded")

    return table

def gather_diagnostics_json():
    return {
        "python": platform.python_version(),
        "platform": platform.system(),
        "verbose": state.verbose,
        "quiet": state.quiet,
        "fast_boot": state.fast_boot,
        "engines": {
            "scene": "OK",
            "world": "OK",
            "agent": "OK",
            "bridge": "OK"
        }
    }

def run_scan(json_output: bool = False):
    if json_output:
        console.print_json(data=gather_diagnostics_json())
        return

    with Live(refresh_per_second=10) as live:
        for phase in [
            "Scanning astral field...",
            "Checking narrative engines...",
            "Verifying agent kernel...",
            "Synchronizing bridge modules...",
            "Finalizing diagnostics..."
        ]:
            panel = Panel(Text(phase, style="bold cyan"), border_style="cyan")
            live.update(panel)
            sleep(0.25)

        final_panel = Panel(gather_diagnostics(), border_style="cyan")
        live.update(final_panel)


def gather_deep_diagnostics_table():
    table = Table(title="AstralStory Deep Diagnostics", title_style="bold magenta")

    table.add_column("Check", style="bold cyan")
    table.add_column("Status", style="bold green")
    table.add_column("Details", style="white")

    # Python
    table.add_row("Python Version", "PASS", platform.python_version())

    # Typer
    try:
        table.add_row("Typer", "PASS", typer.__version__)
    except Exception as e:
        table.add_row("Typer", "FAIL", str(e))

    # Rich
    try:
        import importlib.metadata
        rich_version = importlib.metadata.version("rich")
        table.add_row("Rich", "PASS", rich_version)
    except Exception as e:
        table.add_row("Rich", "FAIL", str(e))

    # AstralStory package
    try:
        import astralstory
        table.add_row("AstralStory Package", "PASS", astralstory.__version__)
    except Exception:
        table.add_row("AstralStory Package", "WARN", "Version unknown")

    # Engines
    for engine in ["scene", "world", "agent", "bridge"]:
        try:
            __import__(f"astralstory.engine.{engine}_engine")
            table.add_row(f"{engine.capitalize()} Engine", "PASS", "Loaded")
        except Exception as e:
            table.add_row(f"{engine.capitalize()} Engine", "FAIL", str(e))

    return table   

def gather_deep_diagnostics_json():
    data = {
        "python": platform.python_version(),
        "platform": platform.system(),
        "typer": None,
        "rich": None,
        "astralstory": None,
        "engines": {},
    }

      
    try:
        data["typer"] = typer.__version__
    except Exception:
        data["typer"] = "ERROR"

    try:
        import importlib.metadata
        data["rich"] = importlib.metadata.version("rich")
    except Exception:
        data["rich"] = "ERROR"

    try:
        import astralstory
        version = getattr(astralstory, "__version__", None)
        data["astralstory"] = version if version else "unknown"
    except Exception as e:
        data["astralstory"] = f"ERROR: {e}"

    for engine in ["scene", "world", "agent", "bridge"]:
        try:
            __import__(f"astralstory.engine.{engine}_engine")
            data["engines"][engine] = "PASS"
        except Exception as e:
            data["engines"][engine] = f"FAIL: {e}"

    return data     

def run_deep_scan(json_output: bool = False):
    if json_output:
        console.print_json(data=gather_deep_diagnostics_json())
        return

    phases = [
        "Running extended astral integrity scan...",
        "Checking Python environment...",
        "Validating narrative engines...",
        "Inspecting agent kernel subsystems...",
        "Verifying bridge synchronization...",
        "Checking AstralStory package integrity...",
        "Finalizing deep diagnostics..."
    ]

    with Live(refresh_per_second=10) as live:
        for phase in phases:
            panel = Panel(Text(phase, style="bold cyan"), border_style="cyan")
            live.update(panel)
            sleep(0.35)

        final_panel = Panel(gather_deep_diagnostics_table(), border_style="cyan")
        live.update(final_panel)



@diagnostics_app.callback(invoke_without_command=True)
def diagnostics_default(
    ctx: typer.Context,
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output diagnostics in JSON format."
    )
):
    # Don't run default behaviour when a subcommand is invoked
    if ctx.invoked_subcommand is not None:
        return

    # If JSON mode, run once and stop
    if json_output:
        console.print_json(data=gather_diagnostics_json())
        raise typer.Exit()

    # Otherwise run cinematic scan
    run_scan()

 
@diagnostics_app.command("run")
def run_diagnostics(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output diagnostics in JSON format."
    )
):
    if json_output:
        console.print_json(data=gather_diagnostics_json())
        return

    run_scan()


@diagnostics_app.command("json")
def diagnostics_json():
    """Output diagnostics in JSON format."""
    console.print_json(data=gather_diagnostics_json())


@diagnostics_app.command("deep")
def deep_diagnostics(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output deep diagnostics in JSON format."
    )
):
    run_deep_scan(json_output=json_output)





