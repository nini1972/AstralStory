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
import astralstory.engine.logger as engine_logger
from astralstory.engine.logger import engine_log
from astralstory.engine.scene_engine import initialize_scene_engine
from astralstory.engine.world_engine import initialize_world_engine
from astralstory.engine.agent_engine import initialize_agent_engine
from astralstory.engine.bridge_engine import initialize_bridge_engine
from astralstory.engine.scene_engine import scene_engine_health_check
from astralstory.engine.world_engine import world_engine_health_check
from astralstory.engine.agent_engine import agent_engine_health_check
from astralstory.engine.bridge_engine import bridge_engine_health_check



console = Console()

dashboard_app = typer.Typer(help="Live system dashboard.")

start_time = datetime.now()

initialize_scene_engine()
initialize_world_engine()
initialize_agent_engine()
initialize_bridge_engine()


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




LOG_BUFFER = []
MAX_LOGS = 20

def add_log(level, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    LOG_BUFFER.append(f"[{timestamp}] [{level}] {message}")

    if len(LOG_BUFFER) > MAX_LOGS:
        LOG_BUFFER.pop(0)

def make_log_panel():
    from rich.text import Text

    if not LOG_BUFFER:
        return Panel("No logs yet.", title="Logs", border_style="yellow")

    log_text = Text()
    for entry in LOG_BUFFER:
        if "[OK]" in entry:
            log_text.append(entry + "\n", style="green")
        elif "[INFO]" in entry:
            log_text.append(entry + "\n", style="cyan")
        elif "[WARN]" in entry:
            log_text.append(entry + "\n", style="yellow")
        elif "[ERROR]" in entry:
            log_text.append(entry + "\n", style="red")
        elif "[DEBUG]" in entry:
            log_text.append(entry + "\n", style="dim")
        else:
            log_text.append(entry + "\n", style="white")

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
        Layout(name="info"),
        Layout(name="logs")
    )

    return layout


@dashboard_app.command("run")
def run_dashboard():
    """
    Run the live system dashboard.
    """
    engine_logger.LOG_SINK = add_log
    if state.quiet:
        console.print("Dashboard disabled in quiet mode.")
        raise typer.Exit()

    layout = build_layout()

    with Live(layout, refresh_per_second=4, screen=True):
        try:
            while True:
                engine_log("INFO", "Dashboard heartbeat")  # temporary demo log
                # Engine health checks
                scene_engine_health_check()
                world_engine_health_check()
                agent_engine_health_check()
                bridge_engine_health_check()
                            
                layout["system"].update(make_system_panel())
                layout["engines"].update(make_engine_panel())
                layout["info"].update(make_info_panel())
                layout["logs"].update(make_log_panel())
                time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("\n[cyan]Dashboard terminated by user.")


            