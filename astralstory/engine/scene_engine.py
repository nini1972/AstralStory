import hashlib
from astralstory.engine.logger import engine_log
import random

# Deterministic scene description templates — variety without randomness
_SCENE_TEMPLATES = [
    "{character} experiences {emotion} under a shimmering astral sky.",
    "In the fading twilight, {character} is overcome by {emotion} as stardust swirls overhead.",
    "{character} stands at the edge of the cosmos, feeling {emotion} wash over their spirit.",
    "The nebula pulses with light as {character} surrenders to {emotion} deep in the astral plane.",
    "As the astral winds howl, {character} confronts {emotion} amid swirling constellations.",
]


def _pick_scene_template(character: str, emotion: str) -> tuple:
    """Select a description template deterministically based on inputs.

    Returns:
        A tuple of (template_string, 1-based index).
    """
    seed = f"{character.lower()}:{emotion.lower()}"
    idx = int(hashlib.sha256(seed.encode()).hexdigest(), 16) % len(_SCENE_TEMPLATES)
    return _SCENE_TEMPLATES[idx], idx + 1


def initialize_scene_engine() -> None:
    engine_log("INFO", "[SCENE] Scene engine initializing")
    # any setup you want later (loading models, resources, etc.)
    engine_log("OK", "[SCENE] Scene engine ready")



def generate_scene(character: str, emotion: str) -> dict:
    """Generate a cinematic scene for a character and emotion.

    Args:
        character: The character name.
        emotion: The emotion to portray.

    Returns:
        A dict with keys ``character``, ``emotion``, ``description``,
        and ``template_id``.
    """
    engine_log("INFO", f"[SCENE] Generating scene for character '{character}' with emotion '{emotion}'")
    template, template_id = _pick_scene_template(character, emotion)
    scene = {
        "character": character,
        "emotion": emotion,
        "description": template.format(character=character, emotion=emotion),
        "template_id": template_id,
    }
    engine_log("OK", f"[SCENE] Scene generated for '{character}' with emotion '{emotion}'")
    return scene

def scene_engine_health_check() -> None:
    # Placeholder logic — replace with real checks later
    load = random.randint(1, 100)

    if load < 70:
        engine_log("OK", f"[SCENE] Scene engine healthy (load {load}%)")
    elif load < 90:
        engine_log("WARN", f"[SCENE] Scene engine under stress (load {load}%)")
    else:
        engine_log("ERROR", f"[SCENE] Scene engine overloaded (load {load}%)")
