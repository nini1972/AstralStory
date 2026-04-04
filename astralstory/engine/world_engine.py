def build_world(template: str) -> dict:
    """Build a world from a named template.

    Args:
        template: The template identifier to use for world construction.

    Returns:
        A dict with keys ``template``, ``status``, and ``details``.
    """
    return {
        "template": template,
        "status": "world-built",
        "details": f"World created using template '{template}'.",
    }
