"""Tests for AstralStory CLI commands using Typer test client."""
import json
from typer.testing import CliRunner
from astralstory.cli.main import app

runner = CliRunner()


def test_scene_generate():
    result = runner.invoke(app, ["scene", "generate", "--character", "luna", "--emotion", "wonder"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["character"] == "luna"
    assert data["emotion"] == "wonder"
    assert "luna" in data["description"]


def test_world_build():
    result = runner.invoke(app, ["world", "build", "nebula-prime"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["template"] == "nebula-prime"
    assert data["status"] == "world-built"


def test_agent_run():
    result = runner.invoke(app, ["agent", "run", "explore-sector-7"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["mission"] == "explore-sector-7"
    assert data["result"] == "mission-complete"


def test_bridge_sync():
    result = runner.invoke(app, ["bridge", "sync", "mars-kernel"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["target"] == "mars-kernel"
    assert data["status"] == "synced"


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "AstralStory CLI" in result.output


def test_scene_generate_missing_options():
    result = runner.invoke(app, ["scene", "generate"])
    assert result.exit_code != 0
