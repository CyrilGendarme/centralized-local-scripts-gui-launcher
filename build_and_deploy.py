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
    """Copy the built executable to desktop."""
    desktop = get_desktop_path()
    
    if not desktop.exists():
        print(f"✗ Desktop path not found: {desktop}")
        return False
    
    # Source executable
    dist_path = Path(__file__).parent / "dist" / "ScriptsLauncher" / "ScriptsLauncher.exe"
    dist_dir = dist_path.parent
    
    if not dist_path.exists():
        print(f"✗ Executable not found: {dist_path}")
        return False
    
    # Clean up any leftover marker files in dist folder
    config_root_file = dist_dir / ".config_root"
    if config_root_file.exists():
        config_root_file.unlink()
        print(f"✓ Cleaned up marker file")
    
    # Destination on desktop
    desktop_exe = desktop / "ScriptsLauncher.exe"
    
    try:
        # Copy executable to desktop
        print(f"Copying executable to desktop...")
        shutil.copy2(dist_path, desktop_exe)
        print(f"✓ Executable copied to: {desktop_exe}")
        
        # Clean up any leftover marker files on desktop
        desktop_marker = desktop / ".config_root"
        if desktop_marker.exists():
            desktop_marker.unlink()
            print(f"✓ Cleaned up leftover marker file from desktop")
        
        print(f"\n✓ ScriptsLauncher.exe created on desktop")
        print(f"  Run from the project directory to auto-detect config.json")
        
        return True
    except Exception as e:
        print(f"✗ Failed to deploy: {e}")
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
    print("✓ ScriptsLauncher.exe created on your Desktop")
    print("✓ Double-click ScriptsLauncher.exe to launch the app")
    print("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
