from datetime import datetime
from pathlib import Path
from typing import Callable

LOG_SINK: Callable[[str, str], None] | None = None  # Optional in-process override

# Project-local log file: <project_root>/logs/engine.log
LOG_FILE: Path = Path(__file__).resolve().parent.parent.parent / "logs" / "engine.log"


def engine_log(level: str, message: str) -> None:
    """
    Engines call this to emit logs.
    Always writes to LOG_FILE; also calls LOG_SINK if set.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}\n"

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(line)

    if callable(LOG_SINK):
        LOG_SINK(level, message)  # pylint: disable=not-callable