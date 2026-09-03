"""
Script runner module - handles execution of various script types.
Dynamically determines the best way to launch files based on OS and available executables.
"""
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


class ScriptRunner:
    """Handles launching scripts with appropriate interpreters based on file type and OS."""

    def __init__(self):
        """Initialize script runner and detect available executables."""
        self.os_type = platform.system()  # "Windows", "Linux", "Darwin"
        self.is_windows = self.os_type == "Windows"
        self.python_executable = sys.executable
        self._cache_executables()

    def _cache_executables(self):
        """Cache available executables for quick lookups."""
        self.has_powershell = self._find_executable("powershell") is not None
        self.has_pwsh = self._find_executable("pwsh") is not None
        self.has_bash = self._find_executable("bash") is not None
        self.has_sh = self._find_executable("sh") is not None
        self.has_git_bash = (
            self.is_windows and Path("C:\\Program Files\\Git\\bin\\bash.exe").exists()
        )

    @staticmethod
    def _find_executable(name: str) -> Optional[str]:
        """Find executable in system PATH."""
        return shutil.which(name)

    def can_run(self, script_path: Path) -> bool:
        """Check if script can be run on current system."""
        if not script_path.exists():
            return False

        suffix = script_path.suffix.lower()

        if suffix == ".ps1":
            return self.has_powershell or self.has_pwsh
        elif suffix == ".sh":
            return self.has_bash or self.has_sh or (
                self.is_windows and self.has_git_bash
            )
        elif suffix == ".py":
            return True
        elif suffix == ".exe" or not suffix:
            return self.is_windows or os.access(script_path, os.X_OK)

        return False

    def run(self, script_path: Path) -> Tuple[bool, str]:
        """
        Run the script with appropriate interpreter.
        
        Args:
            script_path: Path to the script file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        script_path = Path(script_path).resolve()

        if not script_path.exists():
            return False, f"Script not found: {script_path}"

        if not self.can_run(script_path):
            return False, f"Cannot run script: {script_path} (no suitable interpreter)"

        try:
            suffix = script_path.suffix.lower()
            
            if suffix == ".ps1":
                return self._run_powershell(script_path)
            elif suffix == ".sh":
                return self._run_shell(script_path)
            elif suffix == ".py":
                return self._run_python(script_path)
            elif suffix == ".exe" or not suffix:
                return self._run_executable(script_path)
            else:
                return False, f"Unsupported file type: {suffix}"

        except Exception as e:
            return False, f"Error running script: {str(e)}"

    def _run_powershell(self, script_path: Path) -> Tuple[bool, str]:
        """Run PowerShell script."""
        try:
            # Use pwsh (PowerShell Core) if available, otherwise powershell
            ps_exe = self._find_executable("pwsh") or self._find_executable("powershell")
            
            if not ps_exe:
                return False, "PowerShell not found"

            cmd = [
                ps_exe,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(script_path),
            ]
            
            subprocess.Popen(cmd, start_new_session=not self.is_windows)
            return True, f"PowerShell script launched: {script_path.name}"

        except Exception as e:
            return False, f"Failed to run PowerShell script: {str(e)}"

    def _run_shell(self, script_path: Path) -> Tuple[bool, str]:
        """Run shell script (.sh)."""
        try:
            # On Windows, try Git Bash first, then WSL bash
            if self.is_windows:
                bash_exe = None
                if self.has_git_bash:
                    bash_exe = "C:\\Program Files\\Git\\bin\\bash.exe"
                else:
                    bash_exe = self._find_executable("bash")

                if not bash_exe:
                    return False, "Bash not found (install Git Bash or WSL)"

                cmd = [bash_exe, str(script_path)]
            else:
                # On Unix-like systems
                bash_exe = self._find_executable("bash") or self._find_executable("sh")
                if not bash_exe:
                    return False, "Bash/sh not found"
                
                cmd = [bash_exe, str(script_path)]

            subprocess.Popen(cmd, start_new_session=not self.is_windows)
            return True, f"Shell script launched: {script_path.name}"

        except Exception as e:
            return False, f"Failed to run shell script: {str(e)}"

    def _run_python(self, script_path: Path) -> Tuple[bool, str]:
        """Run Python script."""
        try:
            cmd = [self.python_executable, str(script_path)]
            subprocess.Popen(cmd, start_new_session=not self.is_windows)
            return True, f"Python script launched: {script_path.name}"

        except Exception as e:
            return False, f"Failed to run Python script: {str(e)}"

    def _run_executable(self, script_path: Path) -> Tuple[bool, str]:
        """Run executable file."""
        try:
            if self.is_windows and script_path.suffix.lower() != ".exe":
                return False, "Non-.exe executables require Unix permissions"

            cmd = [str(script_path)]
            subprocess.Popen(cmd, start_new_session=not self.is_windows)
            return True, f"Executable launched: {script_path.name}"

        except Exception as e:
            return False, f"Failed to run executable: {str(e)}"

    def get_supported_extensions(self) -> dict:
        """Get supported file extensions and their availability."""
        return {
            ".ps1": self.has_powershell or self.has_pwsh,
            ".sh": self.has_bash or self.has_sh or self.has_git_bash,
            ".py": True,
            ".exe": self.is_windows,
        }
