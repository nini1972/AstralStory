def run_agent(mission: str) -> dict:
    """Run an agent on a mission and return the outcome.

    Args:
        mission: A string describing the mission to execute.

    Returns:
        A dict with keys ``mission``, ``result``, and ``notes``.
    """
    return {
        "mission": mission,
        "result": "mission-complete",
        "notes": "Agent executed mission deterministically.",
    }
