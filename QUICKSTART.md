# Quick Start Guide

Get the Scripts Launcher up and running in 5 minutes.

## Step 1: Setup (2 minutes)

```bash
# Clone or download the project
git clone <repository-url>
cd centralized-local-scripts-gui-launcher

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Add Your Scripts (1 minute)

Create script files in the `scripts/` directory:

```bash
# Create your scripts
mkdir -p scripts
# Copy or create your .ps1, .sh, or .py files
```

## Step 3: Configure (1 minute)

Edit `config.json`:

```json
{
  "app_title": "My Scripts Launcher",
  "scripts": [
    {
      "link_name": "My First Script",
      "local_path": "./scripts/my_script.ps1",
      "description": "What this script does"
    }
  ]
}
```

## Step 4: Run (1 minute)

```bash
python main.py
```

That's it! Your GUI launcher is ready.

---

## Configuration Reference

### Minimal Config

```json
{
  "scripts": [
    {
      "link_name": "My Script",
      "local_path": "./scripts/script.ps1"
    }
  ]
}
```

### Full Config

```json
{
  "app_title": "Corporate Scripts Launcher",
  "window_width": 1200,
  "window_height": 800,
  "app_icon": "./icon.ico",
  "scripts": [
    {
      "link_name": "Deploy Application",
      "local_path": "./scripts/deploy.ps1",
      "description": "Deploys to production server"
    },
    {
      "link_name": "Run Tests",
      "local_path": "./scripts/test.sh",
      "description": "Runs the full test suite"
    },
    {
      "link_name": "Generate Report",
      "local_path": "./scripts/report.py",
      "description": "Generates monthly analytics report"
    }
  ]
}
```

---

## Common Paths

### Windows
```
C:\Users\YourUsername\AppData\Roaming\YourApp\scripts\
C:\Program Files\YourApp\scripts\
```

### Linux
```
/home/username/.local/share/yourapp/scripts/
/opt/yourapp/scripts/
```

### macOS
```
~/Library/Application Support/YourApp/scripts/
/Applications/YourApp.app/Contents/Resources/scripts/
```

---

## Troubleshooting

### Scripts don't run?

1. **Check paths** - Use absolute paths or relative to config.json
   ```json
   "local_path": "./scripts/my_script.ps1"  // Works
   "local_path": "../scripts/my_script.ps1" // Also works
   "local_path": "C:/full/path/my_script.ps1" // Absolute path
   ```

2. **Check permissions** - On Unix, make scripts executable:
   ```bash
   chmod +x scripts/my_script.sh
   ```

3. **Check the status bar** - Error messages appear there

### PowerShell scripts disabled?

Install PowerShell on your system:
- **Windows 11**: `winget install Microsoft.PowerShell`
- **Other**: Visit https://github.com/PowerShell/PowerShell/releases

### Bash scripts disabled?

On Windows, install Git Bash:
- Download from https://gitforwindows.org/
- Or use WSL: `wsl --install`

---

## Tips & Tricks

### Running With Arguments

For Python scripts that accept arguments, modify the config:

```python
# scripts/process_file.py
import sys
if len(sys.argv) > 1:
    filename = sys.argv[1]
    print(f"Processing {filename}...")
```

Then call it:
```bash
python main.py -c "path/to/config.json" "argument_value"
```

### Organizing Large Script Collections

Use multiple config files:

```json
// config_deploy.json
{
  "app_title": "Deployment Scripts",
  "scripts": [/* deployment scripts */]
}

// config_admin.json
{
  "app_title": "Admin Tools",
  "scripts": [/* admin scripts */]
}
```

Then run with different configs:
```bash
python main.py -c config_deploy.json
python main.py -c config_admin.json
```

### Custom Colors/Theme

Edit `theme.py` to customize colors:

```python
ACCENT = "#ff5500"  # Change from purple to orange
DANGER = "#ff0000"  # Change from red
SUCCESS = "#00ff00" # Change from green
```

---

## Next Steps

- **Build an executable**: `python build.py`
- **Add more scripts**: Edit `config.json` and add new entries
- **Customize theme**: Edit `theme.py`
- **Run tests**: `pytest tests/ -v`
- **Read full documentation**: See `README.md`

---

## Keyboard Shortcuts in VS Code

| Shortcut | Action |
|----------|--------|
| `F5` | Start debugging |
| `Ctrl+Shift+D` | Open Debug panel |
| `Ctrl+Shift+Y` | Open Debug Console |
| `Ctrl+K Ctrl+0` | Fold all |
| `Ctrl+K Ctrl+J` | Unfold all |

---

## Need Help?

1. **Check the README.md** - Comprehensive documentation
2. **Review example scripts** - In `scripts/` directory
3. **Run tests** - `pytest tests/ -v` to verify setup
4. **Check status bar** - When scripts fail to run

---

Enjoy your Scripts Launcher! 🚀
