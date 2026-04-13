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


def test_generate_scene_extra_fields():
    """Scene result includes the new template_id field."""
    result = generate_scene("luna", "wonder")
    assert "template_id" in result
    assert isinstance(result["template_id"], int)
    assert result["template_id"] >= 1


def test_generate_scene_deterministic():
    """Same inputs always produce the same description."""
    r1 = generate_scene("luna", "wonder")
    r2 = generate_scene("luna", "wonder")
    assert r1["description"] == r2["description"]
    assert r1["template_id"] == r2["template_id"]


def test_generate_scene_variety():
    """Different inputs may produce different descriptions."""
    descriptions = {
        generate_scene(c, e)["description"]
        for c, e in [("luna", "wonder"), ("sol", "fear"), ("nova", "hope"), ("orion", "rage"), ("vega", "joy")]
    }
    # With 5 templates there should be at least 2 distinct descriptions
    assert len(descriptions) >= 2


def test_build_world():
    result = build_world("nebula-prime")
    assert result["template"] == "nebula-prime"
    assert result["status"] == "world-built"
    assert "nebula-prime" in result["details"]


def test_build_world_features_nebula():
    """Nebula templates include nebula-specific features."""
    result = build_world("nebula-garden")
    assert "features" in result
    assert isinstance(result["features"], list)
    assert len(result["features"]) > 0
    # nebula keyword should match at least one feature
    assert any("cloud" in f or "star" in f or "plasma" in f for f in result["features"])


def test_build_world_features_unknown():
    """Unknown templates fall back to generic features."""
    result = build_world("unknown-world-xyz")
    assert "features" in result
    assert result["features"] == ["vast open terrain", "scattered resource nodes", "unexplored regions"]


def test_run_agent():
    result = run_agent("explore-sector-7")
    assert result["mission"] == "explore-sector-7"
    assert result["result"] == "mission-complete"
    assert "deterministically" in result["notes"]


def test_run_agent_extra_fields():
    """Agent result includes steps_taken and outcome fields."""
    result = run_agent("explore sector seven now")
    assert "steps_taken" in result
    assert result["steps_taken"] == 4  # 4 words
    assert "outcome" in result
    assert "4" in result["outcome"]


def test_sync_bridge():
    result = sync_bridge("mars-kernel")
    assert result["target"] == "mars-kernel"
    assert result["status"] == "synced"
    assert "mars-kernel" in result["details"]


def test_sync_bridge_extra_fields():
    """Bridge result includes protocol and latency_ms fields."""
    result = sync_bridge("mars-kernel")
    assert result["protocol"] == "AstralBridge-v1"
    assert result["latency_ms"] == 0
