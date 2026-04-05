from time import sleep
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

console = Console()

def run_startup_animation():
    steps = [
        "Initializing astral field",
        "Calibrating narrative vectors",
        "Synchronizing world modules",
        "Activating agent kernel",
        "Operator console ready"
    ]

    with Live(refresh_per_second=12) as live:
        for step in steps:
            panel = Panel(
                Spinner("dots", text=Text(step, style="bold cyan")),
                border_style="cyan",
                padding=(1, 2),
            )
            live.update(panel)
            sleep(0.25)  # total animation ~1.2 seconds