"""
Scripts Launcher - A generic GUI application for launching local scripts.

This application provides a clean, modern interface for launching various types
of scripts (.ps1, .sh, .py, .exe) with intelligent environment detection.

Features:
- Multi-format script support (PowerShell, Bash, Python, Executables)
- Environment-aware execution with fallback options
- Configuration-driven button generation
- Dark theme UI with Tkinter
- Cross-platform compatibility (Windows, Linux, macOS)
"""

__version__ = "1.0.0"
__author__ = "Scripts Launcher Contributors"
__description__ = "A generic GUI application for launching local scripts"

def main():
    """Entry point for the application."""
    from main import main as app_main
    app_main()

if __name__ == "__main__":
    main()
