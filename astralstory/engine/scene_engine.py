def generate_scene(character: str, emotion: str) -> dict:
    """Generate a cinematic scene for a character and emotion.

    Args:
        character: The character name.
        emotion: The emotion to portray.

    Returns:
        A dict with keys ``character``, ``emotion``, and ``description``.
    """
    return {
        "character": character,
        "emotion": emotion,
        "description": f"{character} experiences {emotion} under a shimmering astral sky.",
    }
