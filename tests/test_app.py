"""
Unit tests for the Scripts Launcher application.
"""
import json
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from config import Config
from script_runner import ScriptRunner


class TestConfig:
    """Tests for Config class."""

    def test_config_load_valid(self, tmp_path):
        """Test loading a valid config file."""
        config_data = {
            "app_title": "Test Launcher",
            "window_width": 800,
            "window_height": 600,
            "scripts": [
                {
                    "link_name": "Test Script",
                    "local_path": "./test.ps1",
                    "description": "A test script"
                }
            ]
        }
        
        config_file = tmp_path / "config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f)
        
        config = Config(config_file)
        
        assert config.app_title == "Test Launcher"
        assert config.window_width == 800
        assert config.window_height == 600
        assert len(config.get_scripts()) == 1

    def test_config_missing_file(self):
        """Test loading a non-existent config file."""
        with pytest.raises(FileNotFoundError):
            Config(Path("/nonexistent/config.json"))

    def test_config_invalid_json(self, tmp_path):
        """Test loading an invalid JSON file."""
        config_file = tmp_path / "config.json"
        with open(config_file, "w") as f:
            f.write("{ invalid json }")
        
        with pytest.raises(ValueError):
            Config(config_file)

    def test_config_missing_required_fields(self, tmp_path):
        """Test config with missing required script fields."""
        config_data = {
            "scripts": [
                {
                    "link_name": "Test"
                    # Missing local_path
                }
            ]
        }
        
        config_file = tmp_path / "config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f)
        
        with pytest.raises(ValueError):
            Config(config_file)

    def test_config_get_script_paths(self, tmp_path):
        """Test retrieving script paths."""
        config_data = {
            "scripts": [
                {
                    "link_name": "Test Script",
                    "local_path": "./scripts/test.ps1"
                }
            ]
        }
        
        config_file = tmp_path / "config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f)
        
        config = Config(config_file)
        paths = config.get_script_paths()
        
        assert "Test Script" in paths
        assert paths["Test Script"].name == "test.ps1"


class TestScriptRunner:
    """Tests for ScriptRunner class."""

    def test_runner_initialization(self):
        """Test ScriptRunner initialization."""
        runner = ScriptRunner()
        assert runner.python_executable is not None
        assert runner.os_type in ["Windows", "Linux", "Darwin"]

    def test_can_run_python_script(self, tmp_path):
        """Test detection of runnable Python scripts."""
        runner = ScriptRunner()
        script_file = tmp_path / "test.py"
        script_file.write_text("print('test')")
        
        assert runner.can_run(script_file)

    def test_cannot_run_nonexistent_script(self):
        """Test that non-existent scripts cannot run."""
        runner = ScriptRunner()
        script_file = Path("/nonexistent/script.ps1")
        
        assert not runner.can_run(script_file)

    def test_get_supported_extensions(self):
        """Test getting supported file extensions."""
        runner = ScriptRunner()
        supported = runner.get_supported_extensions()
        
        assert ".py" in supported
        assert supported[".py"] is True  # Python always supported
        assert ".ps1" in supported
        assert ".sh" in supported

    @patch('subprocess.Popen')
    def test_run_python_script(self, mock_popen, tmp_path):
        """Test running a Python script."""
        runner = ScriptRunner()
        script_file = tmp_path / "test.py"
        script_file.write_text("print('test')")
        
        success, message = runner.run(script_file)
        
        assert success
        assert "Python script launched" in message
        mock_popen.assert_called_once()

    def test_run_nonexistent_script(self):
        """Test running a non-existent script."""
        runner = ScriptRunner()
        script_file = Path("/nonexistent/script.py")
        
        success, message = runner.run(script_file)
        
        assert not success
        assert "not found" in message.lower()


class TestIntegration:
    """Integration tests."""

    def test_full_workflow(self, tmp_path):
        """Test complete workflow: load config, create runner, check scripts."""
        # Create config
        config_data = {
            "app_title": "Test Launcher",
            "scripts": [
                {
                    "link_name": "Test Script",
                    "local_path": "./test.py"
                }
            ]
        }
        
        config_file = tmp_path / "config.json"
        with open(config_file, "w") as f:
            json.dump(config_data, f)
        
        # Create actual script
        script_file = tmp_path / "test.py"
        script_file.write_text("print('Hello')")
        
        # Load config and check
        config = Config(config_file)
        runner = ScriptRunner()
        
        paths = config.get_script_paths()
        script_path = paths["Test Script"]
        
        assert runner.can_run(script_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
