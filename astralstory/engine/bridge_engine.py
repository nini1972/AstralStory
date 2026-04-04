def sync_bridge(target: str) -> dict:
    """Synchronise AstralStory with a target system via the AstralBridge.

    Args:
        target: The target system identifier (e.g. ``"mars-kernel"``).

    Returns:
        A dict with keys ``target``, ``status``, and ``details``.
    """
    return {
        "target": target,
        "status": "synced",
        "details": f"Bridge synchronized with {target}.",
    }
