from datetime import datetime
from typing import Callable

LOG_SINK: Callable[[str, str], None] | None = None  # Will be set by the dashboard

def engine_log(level: str, message: str):
    """
    Engines call this to emit logs into the dashboard.
    """
    if callable(LOG_SINK):
        LOG_SINK(level, message)