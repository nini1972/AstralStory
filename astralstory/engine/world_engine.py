from astralstory.engine.logger import engine_log
import random

def initialize_world_engine():
    engine_log("INFO", "[WORLD] World engine initializing")
    # any setup you want later (loading models, resources, etc.)
    engine_log("OK", "[WORLD] World engine ready")
    
def build_world(template: str) -> dict:
    """Build a world from a named template.

    Args:
        template: The template identifier to use for world construction.

    Returns:
        A dict with keys ``template``, ``status``, and ``details``.
    """
    engine_log("INFO", f"[WORLD] Building world using template '{template}'")

    world = {
        "template": template,
        "status": "world-built",
        "details": f"World created using template '{template}'.",
    }

    engine_log("OK", f"[WORLD] World built using template '{template}'")
    return world

def world_engine_health_check():
    # Placeholder logic — replace with real checks later
    load = random.randint(1, 100)

    if load < 70:
        engine_log("OK", f"[WORLD] World engine healthy (load {load}%)")
    elif load < 90:
        engine_log("WARN", f"[WORLD] World engine under stress (load {load}%)")
    else:
        engine_log("ERROR", f"[WORLD] World engine overloaded (load {load}%)")  