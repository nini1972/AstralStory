from collections import deque
from dataclasses import dataclass
from datetime import datetime
from threading import Lock
from typing import Any


@dataclass
class CommandEntry:
    timestamp: str
    cmd: str
    args_str: str
    status: str   # "ok" | "error"
    result: Any


class ShellHistory:
    """Thread-safe in-memory store for shell command history, stats, and last result."""

    def __init__(self) -> None:
        self._lock = Lock()
        self.history: deque[CommandEntry] = deque(maxlen=10)
        self.stats: dict[str, dict[str, int]] = {}
        self.last_result: Any = None

    def record(self, cmd: str, args_str: str, status: str, result: Any) -> None:
        """Record a command execution atomically."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = CommandEntry(
            timestamp=timestamp,
            cmd=cmd,
            args_str=args_str,
            status=status,
            result=result,
        )
        with self._lock:
            self.history.append(entry)
            if cmd not in self.stats:
                self.stats[cmd] = {"runs": 0, "ok": 0, "error": 0}
            self.stats[cmd]["runs"] += 1
            self.stats[cmd][status] += 1
            if result is not None:
                self.last_result = result

    def snapshot_history(self) -> list[CommandEntry]:
        """Return a thread-safe copy of the history deque (newest last)."""
        with self._lock:
            return list(self.history)

    def get_stats(self) -> dict[str, dict[str, int]]:
        """Return a thread-safe copy of command statistics."""
        with self._lock:
            return {k: dict(v) for k, v in self.stats.items()}

    def get_last_result(self) -> Any:
        """Return the most recently recorded non-None result, thread-safely."""
        with self._lock:
            return self.last_result


shell_history = ShellHistory()
