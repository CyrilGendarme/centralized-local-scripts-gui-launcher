# Scripts Launcher

A generic Python GUI application that generates buttons for launching local scripts with intelligent environment detection and dynamic executor selection.

## Features

- **Multi-format Support**: Launch PowerShell (.ps1), Batch (.bat/.cmd), Bash (.sh), Python (.py), and executable files (.exe)
- **Environment-aware Execution**: Automatically detects available interpreters and selects the best method to run scripts
- **Configuration-driven**: Simple JSON config file to define buttons and script paths
- **Dark Theme**: Professional dark UI with purple and teal accents using tkinter
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Threaded Execution**: Scripts run in background threads to keep UI responsive
- **Status Feedback**: Real-time status updates and error messages
- **Execution Logs**: Live log output captured during script execution displayed in a textarea

## Project Structure

```
.
├── main.py                      # Main application entry point
├── config.py                    # Configuration loader
├── script_runner.py             # Script execution engine
├── theme.py                     # Dark theme definitions
├── config.json                  # Configuration file (scripts list)
├── requirements.txt             # Python dependencies
├── build.py                     # Build script for executable
├── scripts_launcher.spec        # PyInstaller spec file
├── .vscode/
│   └── launch.json              # VS Code debug configurations
├── scripts/                     # Example scripts directory
│   ├── example.ps1
│   ├── example.bat
│   ├── example.sh
│   └── example.py
└── README.md                    # This file

```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- tkinter (included with most Python distributions)

### 1. Clone or download the project

```bash
git clone <repository-url>
cd centralized-local-scripts-gui-launcher
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure scripts

Edit `config.json` to add your scripts:

```json
{
  "app_title": "My Scripts Launcher",
  "window_width": 1000,
  "window_height": 600,
  "scripts": [
    {
      "link_name": "Backup Database",
      "local_path": "./scripts/backup.ps1",
      "description": "Backs up the database to external storage"
    },
    {
      "link_name": "Deploy App",
      "local_path": "./scripts/deploy.sh",
      "description": "Deploys application to production"
    }
  ]
}
```

### 4. Run the application

**From command line:**
```bash
python main.py
```

**From VS Code:**
- Open the workspace
- Press `Ctrl+Shift+D` to open Debug view
- Select "Python: Launch GUI App"
- Press `F5` to start debugging

## Configuration File (config.json)

### Top-level properties:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `app_title` | string | "Scripts Launcher" | Window title |
| `window_width` | integer | 1000 | Initial window width |
| `window_height` | integer | 600 | Initial window height |
| `app_icon` | string \| null | null | Path to icon file |
| `scripts` | array | [] | List of script definitions |

### Script object properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `link_name` | string | Yes | Label shown on the button |
| `local_path` | string | Yes | Relative path to script file |
| `description` | string | No | Description shown below button |

### Finding config.json

When the application starts, it searches for `config.json` in the following order:

1. **Same directory as the executable/script**
   - When running the compiled executable from Desktop, config.json should be there
   - This is the primary location after deployment

2. **User's home directory**
   - `C:\Users\<YourUsername>\config.json` (Windows)
   - `~/.config.json` (Linux/macOS)

3. **Current working directory**
   - Wherever you run the application from

**Deployment Tip**: After building with `make build-deploy`, copy `config.json` to your Desktop alongside `ScriptsLauncher.exe`.

## Script Execution

The application automatically determines how to execute scripts based on file type and system environment:

### PowerShell (.ps1)
- Uses `pwsh` (PowerShell Core) if available
- Falls back to `powershell.exe` on Windows
- Automatically bypasses execution policy

### Batch Scripts (.bat and .cmd)
- **Windows**: Uses `cmd.exe /c` to execute
- **Other Systems**: Not supported (button disabled)
- No additional dependencies required on Windows

### Shell Scripts (.sh)
- **Windows**: Uses Git Bash or WSL bash
- **Linux/macOS**: Uses system bash or sh
- Makes script executable if needed

### Python (.py)
- Executes with current Python interpreter
- Can pass arguments if needed

### Executables (.exe or no extension)
- **Windows**: Directly launches .exe files
- **Unix**: Requires file to be executable (chmod +x)

### Unavailability Handling

If a script cannot run on the current system:
- Button is disabled (shown in red with "⊘ Unavailable")
- Clicking shows details about required interpreters
- Example: Shell scripts disabled on Windows without Git Bash

## VS Code Integration

### Debug Configurations

The `.vscode/launch.json` includes configurations for:

1. **Python: Current File** - Run active file
2. **Python: Launch GUI App** - Run main application
3. **Python: Launch with Config Path** - Run with custom config
4. **Python: Tests** - Run pytest suite
5. **Python: Module (Debug)** - Debug specific module

### Keyboard Shortcuts

- `F5` - Start debugging (uses default config)
- `Ctrl+Shift+D` - Open Debug view
- `Ctrl+Shift+Y` - Open Debug Console

## Building an Executable

### Option 1: Using build script (recommended)

```bash
python build.py
```

This will:
1. Check and install PyInstaller if needed
2. Build the executable
3. Output to `dist/ScriptsLauncher/` directory

### Option 2: Using PyInstaller directly

```bash
pyinstaller scripts_launcher.spec
```

### Option 3: Build and Deploy to Desktop

```bash
python build_and_deploy.py
```

This will:
1. Build the executable using PyInstaller
2. Automatically copy the executable **and config.json** to your Desktop
3. Create a complete deployment you can easily access and run

**Via VS Code**:
- Open the Debug/Run dropdown menu (Ctrl+Shift+D)
- Select **"Build & Deploy to Desktop"**
- Press F5 or click the Run button
- Both executable and config.json will be placed on your Desktop
- Run `ScriptsLauncher.exe` to start the application

**Result**: You get both files on Desktop, ready to run without additional setup.

### Output Structure

```
dist/
└── ScriptsLauncher/
    ├── ScriptsLauncher.exe     # Main executable
    ├── config.json              # Configuration
    ├── theme.py                 # Theme file
    └── [other dependencies]     # DLLs and modules
```

### Customizing the Build

Edit `scripts_launcher.spec` to:
- Add icon: Set `icon='path/to/icon.ico'`
- Show console: Set `console=True`
- Add data files: Add to `datas=[]` list
- Include hidden imports: Add to `hiddenimports=[]`

## User Interface Layout

The application features a split-pane design:

### Left Pane: Script Buttons
- Displays all configured scripts as clickable cards
- Each card shows:
  - Script name (in accent color)
  - Description (in dim color)
  - File name (in monospace font)
  - Launch button (green if available, red if unavailable)
- Scrollable area for many scripts
- Click any button to execute the script

### Right Pane: Execution Logs
- Real-time display of script execution logs
- Shows timestamps for each execution event
- Displays:
  - Script launch information
  - Execution status and results
  - Error messages (if any)
- Auto-scrolls to show latest logs
- **Clear Logs** button to clear all logged output

### Status Bar
- Located at the bottom of the window
- Shows current operation status
- Displays error/success messages
- Updates in real-time during script execution

## Creating Example Scripts

### PowerShell Example (.ps1)

```powershell
# scripts/example.ps1
Write-Host "Hello from PowerShell!" -ForegroundColor Green
Get-Date
Read-Host "Press Enter to exit"
```

### Batch Example (.bat)

```batch
@echo off
REM scripts/example.bat
echo Hello from Batch!
echo %date% %time%
pause
```

### Bash Example (.sh)

```bash
#!/bin/bash
echo "Hello from Bash!"
date
read -p "Press Enter to exit"
```

### Python Example (.py)

```python
# scripts/example.py
print("Hello from Python!")
import datetime
print(datetime.datetime.now())
input("Press Enter to exit")
```

## Troubleshooting

### "Bash not found" on Windows

- Install Git Bash: https://gitforwindows.org/
- Or install WSL: `wsl --install`

### "PowerShell not found"

- Ensure PowerShell is in your PATH
- On Windows 11, use built-in PowerShell 7: `winget install Microsoft.PowerShell`

### Scripts don't launch

1. Verify `config.json` paths are correct
2. Check file extensions (.ps1, .sh, .py, .exe)
3. On Unix, ensure scripts have executable permission: `chmod +x script.sh`
4. Check status bar for error messages

### GUI not rendering properly

- Install or update tkinter: `pip install tk`
- On Linux: `sudo apt-get install python3-tk`

## Development

### Project Code Overview

**main.py** - GUI application
- `ScriptLauncherApp` class manages UI and interactions
- Creates buttons dynamically from config
- Handles button clicks and script launches

**config.py** - Configuration management
- `Config` class loads and validates config.json
- Resolves script paths relative to config location
- Provides configuration properties and methods

**script_runner.py** - Execution engine
- `ScriptRunner` class detects system capabilities
- Implements execution for each file type
- Handles process launching and error reporting

**theme.py** - UI theme
- Color palette definitions
- ttk Style configurations
- Ready-to-use style classes (Accent.TButton, etc.)

### Running Tests

```bash
pytest tests/ -v
```

## Common Use Cases

### Remote Server Deployment
```json
{
  "scripts": [
    {
      "link_name": "Deploy to Staging",
      "local_path": "./scripts/deploy_staging.sh"
    },
    {
      "link_name": "Deploy to Production",
      "local_path": "./scripts/deploy_prod.sh"
    }
  ]
}
```

### Database Management
```json
{
  "scripts": [
    {
      "link_name": "Backup Database",
      "local_path": "./scripts/backup.ps1"
    },
    {
      "link_name": "Restore Database",
      "local_path": "./scripts/restore.ps1"
    }
  ]
}
```

### Development Tasks
```json
{
  "scripts": [
    {
      "link_name": "Run Tests",
      "local_path": "./scripts/run_tests.py"
    },
    {
      "link_name": "Format Code",
      "local_path": "./scripts/format.py"
    },
    {
      "link_name": "Build Docs",
      "local_path": "./scripts/build_docs.sh"
    }
  ]
}
```

## License

MIT License - Feel free to modify and distribute

## Support

For issues, suggestions, or contributions, please open an issue or submit a pull request.

## Customization Tips

### Theme Customization

Modify `theme.py` to change colors:
```python
ACCENT = "#7c6af7"  # Change primary color
DANGER = "#e05c6a"  # Change error/disabled color
SUCCESS = "#3ddc97" # Change success color
```

### Button Styling

Add custom button styles in `theme.py`:
```python
style.configure("Custom.TButton",
    background="#custom_color",
    foreground="#text_color",
    # ... other properties
)
```

Then use in main.py button creation:
```python
button = ttk.Button(..., style="Custom.TButton")
```

## Performance Notes

- **Startup**: Typically < 1 second
- **Script Launch**: Non-blocking (runs in background thread)
- **Memory**: ~50-100 MB for GUI + modules
- **Executable Size**: ~200-300 MB (PyInstaller bundle)

The application is lightweight and suitable for deployment on any system.
