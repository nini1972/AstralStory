"""Tests for engine stubs — verify deterministic outputs."""
from astralstory.engine.scene_engine import generate_scene
from astralstory.engine.world_engine import build_world
from astralstory.engine.agent_engine import run_agent
from astralstory.engine.bridge_engine import sync_bridge


def test_generate_scene():
    result = generate_scene("luna", "wonder")
    assert result["character"] == "luna"
    assert result["emotion"] == "wonder"
    assert "luna" in result["description"]
    assert "wonder" in result["description"]


def test_build_world():
    result = build_world("nebula-prime")
    assert result["template"] == "nebula-prime"
    assert result["status"] == "world-built"
    assert "nebula-prime" in result["details"]


def test_run_agent():
    result = run_agent("explore-sector-7")
    assert result["mission"] == "explore-sector-7"
    assert result["result"] == "mission-complete"
    assert "deterministically" in result["notes"]


def test_sync_bridge():
    result = sync_bridge("mars-kernel")
    assert result["target"] == "mars-kernel"
    assert result["status"] == "synced"
    assert "mars-kernel" in result["details"]
