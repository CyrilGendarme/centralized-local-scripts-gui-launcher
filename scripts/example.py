#!/usr/bin/env python3
"""
Example Python Script
Demonstrates basic Python operations.
"""

import os
import platform
import sys
from datetime import datetime


def main():
    """Main function."""
    print("=" * 50)
    print("Scripts Launcher - Python Demo")
    print("=" * 50)
    print()

    print("Current Date & Time:")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    print("Current Directory:")
    print(f"  {os.getcwd()}")
    print()

    print("Python Information:")
    print(f"  Python Version: {sys.version.split()[0]}")
    print(f"  Platform: {platform.platform()}")
    print(f"  Processor: {platform.processor()}")
    print()

    print("System Information:")
    print(f"  Machine: {platform.machine()}")
    print(f"  Node: {platform.node()}")
    print()

    print("Environment Variables (sample):")
    for var in ['PATH', 'HOME', 'USER', 'PYTHONPATH']:
        value = os.environ.get(var)
        if value:
            # Truncate long values
            if len(value) > 50:
                value = value[:47] + "..."
            print(f"  {var}: {value}")
    print()

    print("✓ Demo completed successfully!")
    print()

    input("Press Enter to close this window: ")


if __name__ == "__main__":
    main()
