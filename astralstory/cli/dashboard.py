import json
import select
import sys
import time
import typer
import psutil
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from astralstory.cli.state import state
from astralstory.engine.logger import engine_log, LOG_FILE, LOG_BUFFER
from astralstory.engine.scene_engine import initialize_scene_engine
from astralstory.engine.world_engine import initialize_world_engine
from astralstory.engine.agent_engine import initialize_agent_engine
from astralstory.engine.bridge_engine import initialize_bridge_engine
from astralstory.engine.scene_engine import scene_engine_health_check
from astralstory.engine.world_engine import world_engine_health_check
from astralstory.engine.agent_engine import agent_engine_health_check
from astralstory.engine.bridge_engine import bridge_engine_health_check
from astralstory.cli.shell import COMMAND_USAGE, _dispatch
from astralstory.cli.shell_history import shell_history



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
    table.add_column("Runs", style="bold yellow", justify="right")
    stats = shell_history.get_stats()
    for cmd, (usage, desc) in COMMAND_USAGE.items():
        runs = str(stats.get(cmd, {}).get("runs", 0))
        table.add_row(cmd, usage, desc, runs)
    return Panel(table, title="Shell Commands", border_style="green")


def make_history_panel():
    table = Table(show_header=True, box=None)
    table.add_column("Time", style="dim", no_wrap=True)
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Args", style="italic dim")
    table.add_column("Status", no_wrap=True)
    entries = shell_history.snapshot_history()
    for entry in reversed(entries):
        status_cell = "[green]ok[/green]" if entry.status == "ok" else "[red]error[/red]"
        table.add_row(entry.timestamp, entry.cmd, entry.args_str, status_cell)
    if not entries:
        table.add_row("[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]", "[dim]none[/dim]")
    return Panel(table, title="Command History", border_style="cyan")


def make_last_result_panel():
    result = shell_history.get_last_result()
    if result is None:
        return Panel(Text("No result yet.", style="dim"), title="Last Result", border_style="blue")
    try:
        json_str = json.dumps(result, indent=2)
        syntax = Syntax(json_str, "json", theme="ansi_dark", word_wrap=True)
        return Panel(syntax, title="Last Result", border_style="blue")
    except (TypeError, ValueError):
        return Panel(Text(str(result), style="white"), title="Last Result", border_style="blue")


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
    entries = list(LOG_BUFFER)[-MAX_LOGS:]

    if not entries:
        return Panel("No logs yet.", title="Logs", border_style="yellow")

    log_text = Text()
    for entry in entries:
        style = next((s for tag, s in LEVEL_STYLES.items() if tag in entry), "white")
        log_text.append(entry.rstrip() + "\n", style=style)

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
        Layout(name="commands", ratio=2),
        Layout(name="history", ratio=2),
        Layout(name="last_result", ratio=2),
        Layout(name="logs", ratio=3),
    )

    return layout


def _handle_keyboard_input(live: Live) -> bool:
    """
    Check for a keypress and dispatch the typed command.

    Stops the Live display, captures a full input line, then restarts the
    display. Returns True when the user types 'exit' or 'quit'.

    Uses ``msvcrt.kbhit`` on Windows and ``select`` on Linux/macOS so that
    the dashboard is fully cross-platform.
    """
    try:
        import msvcrt
        has_input = msvcrt.kbhit()
    except ImportError:
        # Unix/macOS: timeout=0 makes select a non-blocking poll, mirroring msvcrt.kbhit()
        readable, _, _ = select.select([sys.stdin], [], [], 0)
        has_input = bool(readable)

    if not has_input:
        return False
    live.stop()
    try:
        line = input("▶ ")
    except (EOFError, KeyboardInterrupt):
        line = "exit"
    live.start()
    if line.strip().lower() in ("exit", "quit"):
        return True
    _dispatch(line, echo=False)
    return False


@dashboard_app.command("run")
def run_dashboard():
    """
    Run the live system dashboard.

    Press any key while the dashboard is active to open an inline command
    prompt. Type any shell command (scene / world / agent / bridge / diag)
    and press Enter — results appear immediately in the History and Last
    Result panels without leaving the dashboard.
    """
    # Clear in-memory buffer and log file for a fresh session
    LOG_BUFFER.clear()
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

    with Live(layout, refresh_per_second=4, screen=True) as live:
        tick = 0
        try:
            while True:
                if _handle_keyboard_input(live):
                    break

                # ── Heavy refresh every 2 s (20 ticks × 100 ms) ─────────────
                if tick % 20 == 0:
                    engine_log("INFO", "Dashboard heartbeat")
                    engine_log("SCENE", "[SCENE] Purple test log — cross-process logging active")
                    scene_engine_health_check()
                    world_engine_health_check()
                    agent_engine_health_check()
                    bridge_engine_health_check()
                    layout["system"].update(make_system_panel())
                    layout["engines"].update(make_engine_panel())
                    layout["info"].update(make_info_panel())

                # ── Responsive panels every 500 ms (5 ticks × 100 ms) ───────
                if tick % 5 == 0:
                    layout["commands"].update(make_commands_panel())
                    layout["history"].update(make_history_panel())
                    layout["last_result"].update(make_last_result_panel())
                    layout["logs"].update(make_log_panel())

                time.sleep(0.1)
                tick += 1

        except KeyboardInterrupt:
            pass

    console.print("\n[cyan]Dashboard terminated by user.[/cyan]")


            