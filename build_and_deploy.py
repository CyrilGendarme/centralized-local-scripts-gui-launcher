"""
Build and deploy script - creates executable and copies to desktop.
"""
import shutil
import subprocess
import sys
from pathlib import Path


def get_desktop_path():
    """Get the user's desktop path."""
    if sys.platform == "win32":
        # Windows
        from pathlib import Path
        desktop = Path.home() / "Desktop"
    else:
        # Linux/macOS
        desktop = Path.home() / "Desktop"
    
    return desktop


def build_executable():
    """Run the build.py script to create the executable."""
    build_script = Path(__file__).parent / "build.py"
    
    print("Building executable...")
    result = subprocess.run([sys.executable, str(build_script)], cwd=str(build_script.parent))
    
    return result.returncode == 0


def copy_to_desktop():
    """Copy the built executable to the desktop."""
    desktop = get_desktop_path()
    
    if not desktop.exists():
        print(f"✗ Desktop path not found: {desktop}")
        return False
    
    # Source executable
    dist_path = Path(__file__).parent / "dist" / "ScriptsLauncher" / "ScriptsLauncher.exe"
    
    if not dist_path.exists():
        print(f"✗ Executable not found: {dist_path}")
        return False
    
    # Destination on desktop
    desktop_exe = desktop / "ScriptsLauncher.exe"
    
    try:
        print(f"Copying executable to desktop...")
        shutil.copy2(dist_path, desktop_exe)
        print(f"✓ Executable copied to: {desktop_exe}")
        return True
    except Exception as e:
        print(f"✗ Failed to copy executable: {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 60)
    print("Scripts Launcher - Build & Deploy")
    print("=" * 60)
    print()
    
    if not build_executable():
        print()
        print("=" * 60)
        print("✗ Build failed - deployment cancelled")
        print("=" * 60)
        sys.exit(1)
    
    print()
    if not copy_to_desktop():
        print()
        print("=" * 60)
        print("✗ Deployment failed")
        print("=" * 60)
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("✓ Build and deployment successful!")
    print("✓ Executable is now on your desktop")
    print("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
