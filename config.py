"""
Configuration loader module - handles loading and parsing config.json files.
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


class Config:
    """Handles loading and parsing configuration files."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize config loader.
        
        Args:
            config_path: Path to config.json. If None, searches in multiple locations:
                         - PROJECT_CONFIG_PATH environment variable (if set)
                         - Same directory as the script/executable
                         - User's home directory
                         - Current working directory
        """
        if config_path is None:
            config_path = self._find_config()
        
        self.config_path = Path(config_path).resolve()
        self.data: Dict[str, Any] = {}
        self.scripts: List[Dict[str, Any]] = []
        self._load()

    @staticmethod
    def _find_config() -> Path:
        """
        Find config.json in multiple locations using absolute paths.
        
        Search order (when running as exe):
        1. Same directory as the executable (bundled config.json)
        2. Current working directory
        3. User's home directory
        4. Desktop
        
        Search order (when running as script):
        1. Current working directory (project directory)
        2. User's home directory
        3. Desktop
        4. Same directory as the script
        
        Returns:
            Path to config.json
            
        Raises:
            FileNotFoundError: If config.json not found in any location
        """
        search_paths = []
        is_frozen = getattr(sys, 'frozen', False)
        
        # Determine script directory
        if is_frozen:
            # Running as executable (PyInstaller)
            script_dir = Path(sys.executable).parent
        else:
            # Running as Python script
            script_dir = Path(sys.argv[0]).parent.resolve()
        
        # When running as exe, prioritize bundled config
        if is_frozen:
            search_paths.append(script_dir / "config.json")
        
        # Current working directory
        search_paths.append(Path.cwd() / "config.json")
        
        # User's home directory
        search_paths.append(Path.home() / "config.json")
        
        # Desktop
        desktop = Path.home() / "Desktop"
        search_paths.append(desktop / "config.json")
        
        # Script directory (for non-frozen, or as fallback)
        if not is_frozen:
            search_paths.append(script_dir / "config.json")
        
        # Search for config.json
        for config_path in search_paths:
            if config_path.exists():
                return config_path
        
        # If not found, raise error with all searched locations
        locations = "\n  ".join(str(p) for p in search_paths)
        raise FileNotFoundError(
            f"Config file not found. Searched in:\n  {locations}"
        )

    def _load(self):
        """Load configuration from JSON file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            
            # Extract scripts and validate
            self.scripts = self.data.get("scripts", [])
            self._validate_scripts()

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")

    def _validate_scripts(self):
        """Validate script entries."""
        for i, script in enumerate(self.scripts):
            if not isinstance(script, dict):
                raise ValueError(f"Script {i} is not a dictionary")
            
            if "local_path" not in script or "link_name" not in script:
                raise ValueError(
                    f"Script {i} missing required fields (local_path, link_name)"
                )

    @property
    def app_title(self) -> str:
        """Get application title."""
        return self.data.get("app_title", "Scripts Launcher")

    @property
    def window_width(self) -> int:
        """Get window width."""
        return self.data.get("window_width", 1000)

    @property
    def window_height(self) -> int:
        """Get window height."""
        return self.data.get("window_height", 600)

    @property
    def app_icon(self) -> Optional[Path]:
        """Get app icon path if set."""
        icon_path = self.data.get("app_icon")
        if icon_path:
            return Path(icon_path).resolve()
        return None

    def get_scripts(self) -> List[Dict[str, Any]]:
        """Get all configured scripts."""
        return self.scripts.copy()

    def get_script_paths(self, relative_to: Optional[Path] = None) -> Dict[str, Path]:
        """
        Get script paths relative to config file.
        
        Args:
            relative_to: If provided, paths will be relative to this directory
            
        Returns:
            Dictionary of {link_name: resolved_path}
        """
        result = {}
        config_dir = self.config_path.parent
        
        for script in self.scripts:
            link_name = script["link_name"]
            local_path = script["local_path"]
            
            # Resolve path relative to config file location
            resolved_path = (config_dir / local_path).resolve()
            result[link_name] = resolved_path
        
        return result

    def reload(self):
        """Reload configuration from disk."""
        self.data.clear()
        self.scripts.clear()
        self._load()
