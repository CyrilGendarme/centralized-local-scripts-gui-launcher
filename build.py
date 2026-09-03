"""
Build script for creating the executable.
Handles both PyInstaller and pre-build checks.
"""
import os
import subprocess
import sys
from pathlib import Path


def check_requirements():
    """Check if required packages are installed."""
    required_packages = ['pyinstaller']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is not installed")
            print(f"  Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def build_executable():
    """Build the executable using PyInstaller."""
    spec_file = Path(__file__).parent / "scripts_launcher.spec"
    
    if not spec_file.exists():
        print(f"✗ Spec file not found: {spec_file}")
        return False
    
    print(f"Building executable from {spec_file}...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", str(spec_file)],
            cwd=str(spec_file.parent),
            capture_output=False
        )
        
        if result.returncode == 0:
            print("✓ Build completed successfully!")
            dist_path = spec_file.parent / "dist" / "ScriptsLauncher"
            if dist_path.exists():
                print(f"✓ Executable location: {dist_path}")
                exe_file = dist_path / "ScriptsLauncher.exe"
                if exe_file.exists():
                    print(f"✓ Main executable: {exe_file}")
            return True
        else:
            print("✗ Build failed")
            return False
            
    except Exception as e:
        print(f"✗ Error during build: {e}")
        return False


def main():
    """Main build entry point."""
    print("=" * 60)
    print("Scripts Launcher - Build Script")
    print("=" * 60)
    print()
    
    print("[1/2] Checking requirements...")
    print()
    check_requirements()
    
    print()
    print("[2/2] Building executable...")
    print()
    if build_executable():
        print()
        print("=" * 60)
        print("✓ Build successful!")
        print("=" * 60)
        sys.exit(0)
    else:
        print()
        print("=" * 60)
        print("✗ Build failed")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
