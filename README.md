# AstralStory

**AstralStory** is a deterministic creative engine exposed as a CLI. It provides four subsystems — **Scene**, **World**, **Agent**, and **Bridge** — each backed by a pure-Python engine layer and a [Typer](https://typer.tiangolo.com/) CLI frontend with [Rich](https://rich.readthedocs.io/) output.

---

## Features

| Subsystem | Command | What it does |
|-----------|---------|--------------|
| Scene | `scene generate` | Generates a cinematic scene for a character and emotion |
| World | `world build` | Constructs a world from a named template |
| Agent | `agent run` | Runs an agent on a mission and returns the outcome |
| Bridge | `bridge sync` | Synchronises AstralStory with a target system (e.g. Mars kernel) |

All commands return structured JSON output, making AstralStory easy to integrate into pipelines.

---

## Requirements

- Python ≥ 3.9

---

## Installation

```bash
# Clone the repository
git clone https://github.com/nini1972/AstralStory.git
cd AstralStory

# Install (editable, with dev dependencies)
pip install -e ".[dev]"
```

---

## Usage

```bash
# Top-level help
astralstory --help

# Generate a cinematic scene
astralstory scene generate --character luna --emotion wonder

# Build a world from a template
astralstory world build nebula-prime

# Run an agent on a mission
astralstory agent run "explore-sector-7"

# Sync with a target system
astralstory bridge sync mars-kernel
```

### Example output — `scene generate`

```json
{
  "character": "luna",
  "emotion": "wonder",
  "description": "luna experiences wonder under a shimmering astral sky."
}
```

---

## Project structure

```
astralstory/
├── cli/            # Typer command groups (scene, world, agent, bridge)
│   ├── main.py     # Entry point — assembles all sub-apps
│   ├── scene.py
│   ├── world.py
│   ├── agent.py
│   └── bridge.py
└── engine/         # Pure-Python engine layer (no CLI dependencies)
    ├── scene_engine.py
    ├── world_engine.py
    ├── agent_engine.py
    └── bridge_engine.py
tests/
├── test_cli.py     # CLI integration tests (Typer test runner)
└── test_engines.py # Engine unit tests
```

---

## Running tests

```bash
pytest
```

---

## License

MIT

