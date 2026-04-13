from astralstory.engine.logger import engine_log
import random
from typing import List

# Keyword → feature set mapping for richer world generation
_WORLD_FEATURE_MAP = {
    "nebula":   ["shimmering gas clouds", "newborn star clusters", "ionized plasma rivers"],
    "crystal":  ["prismatic crystal spires", "resonant harmonic fields", "light-refracting caverns"],
    "desert":   ["endless dune seas", "ancient buried ruins", "whispering sandstorms"],
    "forest":   ["bioluminescent canopies", "ancient root networks", "symbiotic fauna"],
    "ocean":    ["bioluminescent deep currents", "pressure-glass formations", "tidal memory pools"],
    "void":     ["dark matter eddies", "collapsed star remnants", "quantum silence zones"],
    "prime":    ["foundational ley lines", "origin-event echoes", "stabilized reality anchors"],
    "garden":   ["cultivated biome domes", "seed-vault archives", "atmospheric nutrient clouds"],
}


def _world_features(template: str) -> List[str]:
    """Return a feature list for the given template, matched by keyword."""
    lower = template.lower()
    features: List[str] = []
    for keyword, feature_list in _WORLD_FEATURE_MAP.items():
        if keyword in lower:
            features.extend(feature_list)
    return features or ["vast open terrain", "scattered resource nodes", "unexplored regions"]


def initialize_world_engine() -> None:
    engine_log("INFO", "[WORLD] World engine initializing")
    # any setup you want later (loading models, resources, etc.)
    engine_log("OK", "[WORLD] World engine ready")


def build_world(template: str) -> dict:
    """Build a world from a named template.

    Args:
        template: The template identifier to use for world construction.

    Returns:
        A dict with keys ``template``, ``status``, ``details``,
        and ``features``.
    """
    engine_log("INFO", f"[WORLD] Building world using template '{template}'")

    features = _world_features(template)
    world = {
        "template": template,
        "status": "world-built",
        "details": f"World created using template '{template}'.",
        "features": features,
    }

    engine_log("OK", f"[WORLD] World built using template '{template}'")
    return world

def world_engine_health_check() -> None:
    # Placeholder logic — replace with real checks later
    load = random.randint(1, 100)

    if load < 70:
        engine_log("OK", f"[WORLD] World engine healthy (load {load}%)")
    elif load < 90:
        engine_log("WARN", f"[WORLD] World engine under stress (load {load}%)")
    else:
        engine_log("ERROR", f"[WORLD] World engine overloaded (load {load}%)")
  