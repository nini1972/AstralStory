import time
import typer
import psutil
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from astralstory.cli.state import state
from astralstory.engine.logger import engine_log, LOG_FILE
from astralstory.engine.scene_engine import initialize_scene_engine
from astralstory.engine.world_engine import initialize_world_engine
from astralstory.engine.agent_engine import initialize_agent_engine
from astralstory.engine.bridge_engine import initialize_bridge_engine
from astralstory.engine.scene_engine import scene_engine_health_check
from astralstory.engine.world_engine import world_engine_health_check
from astralstory.engine.agent_engine import agent_engine_health_check
from astralstory.engine.bridge_engine import bridge_engine_health_check
from astralstory.cli.shell import COMMAND_USAGE



console = Console()

dashboard_app = typer.Typer(help="Live system dashboard.")

start_time = datetime.now()

def make_system_panel():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    uptime = datetime.now() - start_time

    table = Table(show_header=False, box=None)
    table.add_row("CPU Load", f"{cpu}%")
    table.add_row("Memory", f"{mem}%")
    table.add_row("Uptime", str(uptime).split(".")[0])

    return Panel(table, title="System", border_style="cyan")


def make_engine_panel():
    table = Table(show_header=False, box=None)
    for engine in ["scene", "world", "agent", "bridge"]:
        try:
            __import__(f"astralstory.engine.{engine}_engine")
            status = "[green]OK"
        except Exception:
            status = "[red]FAIL"
        table.add_row(engine.capitalize(), status)

    return Panel(table, title="Engines", border_style="magenta")


def make_info_panel():
    import platform
    import astralstory
    import importlib.metadata

    table = Table(show_header=False, box=None)
    table.add_row("Python", platform.python_version())
    table.add_row("Typer", typer.__version__)
    table.add_row("Rich", importlib.metadata.version("rich"))
    table.add_row("AstralStory", getattr(astralstory, "__version__", "unknown"))

    return Panel(table, title="Versions", border_style="blue")


def make_commands_panel():
    table = Table(show_header=True, box=None)
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Usage", style="italic dim")
    table.add_column("Description", style="white")
    for cmd, (usage, desc) in COMMAND_USAGE.items():
        table.add_row(cmd, usage, desc)
    return Panel(table, title="Shell Commands", border_style="green")


LEVEL_STYLES = {
    "[OK]": "green",
    "[INFO]": "cyan",
    "[WARN]": "yellow",
    "[ERROR]": "red",
    "[DEBUG]": "dim",
    "[SCENE]": "magenta",
}

MAX_LOGS = 20

def make_log_panel():
    from rich.text import Text

    if not LOG_FILE.exists():
        return Panel("No logs yet.", title="Logs", border_style="yellow")

    with LOG_FILE.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()

    entries = [line.rstrip() for line in lines if line.strip()][-MAX_LOGS:]

    if not entries:
        return Panel("No logs yet.", title="Logs", border_style="yellow")

    log_text = Text()
    for entry in entries:
        style = next((s for tag, s in LEVEL_STYLES.items() if tag in entry), "white")
        log_text.append(entry + "\n", style=style)

    return Panel(log_text, title="Logs", border_style="yellow")

def build_layout():
    layout = Layout()

    layout.split_row(
        Layout(name="left"),
        Layout(name="right")
    )

    layout["left"].split_column(
        Layout(name="system"),
        Layout(name="engines")
    )

    layout["right"].split_column(
        Layout(name="info", ratio=1),
        Layout(name="commands", ratio=1),
        Layout(name="logs", ratio=2)
    )

    return layout


@dashboard_app.command("run")
def run_dashboard():
    """
    Run the live system dashboard.
    """
    # Clear log file so each dashboard session starts fresh
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text("", encoding="utf-8")
    initialize_scene_engine()
    initialize_world_engine()
    initialize_agent_engine()
    initialize_bridge_engine()
    if state.quiet:
        console.print("Dashboard disabled in quiet mode.")
        raise typer.Exit()

    layout = build_layout()
    commands_panel = make_commands_panel()

    with Live(layout, refresh_per_second=4, screen=True):
        layout["commands"].update(commands_panel)
        try:
            while True:
                engine_log("INFO", "Dashboard heartbeat")  # temporary demo log
                engine_log("SCENE", "[SCENE] Purple test log — cross-process logging active")
                # Engine health checks
                scene_engine_health_check()
                world_engine_health_check()
                agent_engine_health_check()
                bridge_engine_health_check()
                            
                layout["system"].update(make_system_panel())
                layout["engines"].update(make_engine_panel())
                layout["info"].update(make_info_panel())
                layout["logs"].update(make_log_panel())
                time.sleep(2.0)
        except KeyboardInterrupt:
            console.print("\n[cyan]Dashboard terminated by user.")


            