from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

LOG_SINK: Optional[Callable[[str, str], None]] = None  # Optional in-process override

# In-memory ring buffer for the dashboard (single-process reads)
LOG_BUFFER: deque[str] = deque(maxlen=50)

# Project-local log file: <project_root>/logs/engine.log
LOG_FILE: Path = Path(__file__).resolve().parent.parent.parent / "logs" / "engine.log"


def engine_log(level: str, message: str) -> None:
    """
    Engines call this to emit logs.
    Always writes to LOG_FILE and LOG_BUFFER; also calls LOG_SINK if set.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}"

    LOG_BUFFER.append(line)

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")

    if callable(LOG_SINK):
        LOG_SINK(level, message)  # pylint: disable=not-callable