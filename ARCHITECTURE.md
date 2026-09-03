# Architecture & Design

Technical overview of the Scripts Launcher application.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GUI Application (Tkinter)                │
│                  main.py - ScriptLauncherApp                │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Header Frame    │  │  Status Bar      │                │
│  │  - Title         │  │  - Messages      │                │
│  │  - Description   │  │  - Status        │                │
│  └──────────────────┘  └──────────────────┘                │
│  ┌─────────────────────────────────────────┐               │
│  │      Scripts Container (Scrollable)     │               │
│  │  ┌─────────────────────────────────┐   │               │
│  │  │ Script 1 Button Card            │   │               │
│  │  │  - Name, Description, Path      │   │               │
│  │  │  - [Launch] or [Unavailable]    │   │               │
│  │  └─────────────────────────────────┘   │               │
│  │  ┌─────────────────────────────────┐   │               │
│  │  │ Script 2 Button Card            │   │               │
│  │  │  - Name, Description, Path      │   │               │
│  │  │  - [Launch] or [Unavailable]    │   │               │
│  │  └─────────────────────────────────┘   │               │
│  └─────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
        ↓                                    ↓
┌──────────────────────────┐    ┌────────────────────────────┐
│   Configuration Layer    │    │   Execution Layer          │
│   config.py              │    │   script_runner.py         │
│                          │    │                            │
│ - Load config.json       │    │ - Detect system            │
│ - Validate scripts       │    │ - Select interpreter       │
│ - Resolve paths          │    │ - Execute scripts          │
│ - Cache data             │    │ - Handle errors            │
└──────────────────────────┘    └────────────────────────────┘
        ↓                                    ↓
  config.json              ┌──────────────────────────────┐
  - Script list            │   System Integration         │
  - Settings               │                              │
  - Paths                  │ - PowerShell (pwsh/ps.exe)   │
                           │ - Bash (sh/bash/wsl)         │
                           │ - Python Interpreter         │
                           │ - Executables (.exe)         │
                           └──────────────────────────────┘
                                   ↓
                           [External Scripts]
                           [External Programs]
                           [External Commands]
```

## Module Breakdown

### 1. **main.py** - GUI Application
**Purpose**: Creates and manages the graphical user interface.

**Key Classes**:
- `ScriptLauncherApp`: Main application controller
  - Initializes window and loads configuration
  - Creates UI components dynamically
  - Handles user interactions
  - Manages threading for script execution

**Key Methods**:
- `_build_ui()`: Constructs the user interface
- `_load_scripts()`: Creates buttons from config
- `_create_script_button()`: Creates individual script entry
- `_on_script_launch()`: Handles launch button clicks
- `_on_script_complete()`: Updates UI after execution

**Threading**:
- Uses `threading.Thread` with daemon flag
- Keeps UI responsive during script execution
- Calls GUI updates via `root.after()` to stay thread-safe

### 2. **config.py** - Configuration Management
**Purpose**: Loads, validates, and provides access to configuration.

**Key Classes**:
- `Config`: Configuration loader and validator
  - Parses JSON configuration files
  - Validates required fields
  - Resolves paths relative to config location
  - Provides properties for app settings

**Key Methods**:
- `_load()`: Reads config.json and parses JSON
- `_validate_scripts()`: Ensures all scripts have required fields
- `get_scripts()`: Returns list of script definitions
- `get_script_paths()`: Returns resolved file paths

**Configuration Structure**:
```python
{
    "app_title": str,
    "window_width": int,
    "window_height": int,
    "app_icon": str | None,
    "scripts": [
        {
            "link_name": str,      # Button label
            "local_path": str,     # File path
            "description": str     # Optional description
        }
    ]
}
```

### 3. **script_runner.py** - Script Execution Engine
**Purpose**: Detects available interpreters and executes scripts intelligently.

**Key Classes**:
- `ScriptRunner`: Handles script execution with environment detection
  - Detects available interpreters on startup
  - Determines execution method per file type
  - Launches scripts appropriately
  - Reports success/failure

**Key Methods**:
- `_cache_executables()`: Detects available interpreters
- `can_run()`: Checks if script is runnable on this system
- `run()`: Executes the script with appropriate method
- `_run_powershell()`: PowerShell execution
- `_run_shell()`: Shell script execution
- `_run_python()`: Python script execution
- `_run_executable()`: Direct executable execution

**Interpreter Detection**:
```
PowerShell (.ps1)
├── pwsh (PowerShell Core - preferred)
└── powershell.exe (Windows PowerShell - fallback)

Batch Scripts (.bat / .cmd)
└── cmd.exe /c (Windows only)

Shell Scripts (.sh)
├── Windows: Git Bash → WSL bash
├── Unix: bash → sh
└── macOS: bash → sh

Python (.py)
└── sys.executable (current Python interpreter)

Executables (.exe / no extension)
├── Windows: Direct execution
└── Unix: Requires execute permission
```

### 4. **theme.py** - UI Theme Definitions
**Purpose**: Defines colors, fonts, and styles for all UI components.

**Key Components**:
- Color palette constants
- Font definitions
- ttk.Style configurations for each widget type
- Pre-defined style classes

**Available Styles**:
- `Accent.TButton` - Primary action buttons
- `Danger.TButton` - Error/unavailable buttons
- `Success.TButton` - Success state buttons
- Various label and panel styles

## Data Flow

### Script Launch Flow

```
User clicks button
    ↓
_on_script_launch() called
    ↓
Update status: "Launching..."
    ↓
Create daemon thread
    ↓
[Background Thread]
└─ runner.run(script_path)
   ├─ Verify file exists
   ├─ Check if runnable (can_run)
   ├─ Select executor based on file type
   ├─ Execute via subprocess.Popen()
   └─ Return (success, message)
    ↓
root.after() → _on_script_complete()
    ↓
Update status bar
    ↓
Show success/error message
    ↓
UI responsive again
```

### Application Startup Flow

```
main()
    ↓
Create Tk() root window
    ↓
ScriptLauncherApp(root)
    ├─ Load config.json
    ├─ Create ScriptRunner (detect interpreters)
    ├─ Apply theme
    ├─ Build UI
    └─ Load scripts (create buttons)
    ↓
root.mainloop()
    ↓
Wait for user interaction
```

## Threading Model

The application uses a **producer-consumer threading pattern**:

1. **Main Thread** (UI)
   - Handles Tkinter GUI
   - Responds to user input
   - Updates display

2. **Worker Threads** (Background)
   - Execute scripts
   - No direct UI access
   - Report results via `root.after()`

```python
# Thread-safe pattern used in app
def _on_script_launch(...):
    def run_script():
        success, message = self.runner.run(script_path)
        # Use root.after() for thread-safe GUI update
        self.root.after(0, lambda: self._on_script_complete(...))
    
    thread = threading.Thread(target=run_script, daemon=True)
    thread.start()  # Non-blocking
```

## Process Execution Model

Scripts are launched as **detached processes**:

```python
# Windows: inherit parent process
subprocess.Popen(..., start_new_session=False)

# Unix: create new session
subprocess.Popen(..., start_new_session=True)
```

Benefits:
- Script can continue running after launcher closes
- No process hierarchy dependencies
- User can interact with launcher while script runs

## Error Handling

Three-level error handling:

1. **Configuration Level**
   - File not found
   - Invalid JSON
   - Missing required fields
   - Path resolution errors

2. **Execution Level**
   - Script file not found
   - No suitable interpreter
   - Execution permission denied
   - Process launch failure

3. **UI Level**
   - Display error messages in status bar
   - Show detailed message boxes
   - Log to console for debugging

## Environment Detection

The runner performs **one-time initialization** of system capabilities:

```python
def _cache_executables(self):
    self.os_type = platform.system()  # "Windows", "Linux", "Darwin"
    self.is_windows = self.os_type == "Windows"
    self.has_powershell = shutil.which("powershell") is not None
    self.has_bash = shutil.which("bash") is not None
    # ... etc
```

This is done once on startup for performance.

## File Resolution

Paths in config.json are resolved **relative to config.json location**:

```
Project Structure:
├── config.json
├── scripts/
│   ├── script1.ps1
│   └── script2.sh
└── subfolder/
    └── script3.py

config.json contains:
- "./scripts/script1.ps1" → Resolves to {config_dir}/scripts/script1.ps1
- "./subfolder/script3.py" → Resolves to {config_dir}/subfolder/script3.py
```

Benefits:
- Can move entire project folder
- Relative paths work from any working directory
- No hardcoded absolute paths

## Building Executables

### PyInstaller Spec File

The `scripts_launcher.spec` file defines:
- Entry point: `main.py`
- Data files to include (config.json, theme.py)
- Build options (console, icon, etc.)
- Output configuration

### Build Process

```
build.py
    ↓
Check dependencies (PyInstaller)
    ↓
Run PyInstaller with spec file
    ↓
Analyze Python code
    ↓
Create bundle with dependencies
    ↓
Output to dist/ScriptsLauncher/
```

## Performance Characteristics

**Startup Time**: ~1 second (includes theme loading)
**Memory Usage**: ~50-100 MB (tkinter + modules)
**UI Responsiveness**: Maintained via threading
**Executable Size**: ~200-300 MB (includes Python runtime)

## Security Considerations

1. **Execution Policy**
   - PowerShell runs with `-ExecutionPolicy Bypass`
   - Scripts must be explicitly configured
   - No arbitrary code execution

2. **Path Handling**
   - All paths validated against filesystem
   - No relative path traversal allowed
   - File existence checked before execution

3. **User Permissions**
   - Scripts run with user permissions
   - No privilege escalation
   - No UAC bypass

## Extensibility

The architecture supports easy extensions:

1. **Adding Script Types**
   - Extend `ScriptRunner._run_*()` methods
   - Add extension to `can_run()` checks
   - Add executor detection

2. **UI Customization**
   - Modify `theme.py` for styling
   - Extend `ScriptLauncherApp` for features
   - Add custom button styles

3. **Configuration Features**
   - Add new config properties
   - Create config validators
   - Support multiple config files

## Development Guidelines

- Keep modules single-responsibility
- Use type hints for clarity
- Thread-safe GUI updates only via `root.after()`
- Test with different Python versions
- Document public APIs
- Use logging for debugging

## Testing Strategy

Test coverage includes:
- Configuration loading and validation
- Script runner detection and execution
- Path resolution
- UI responsiveness
- Error conditions

Run tests with:
```bash
pytest tests/ -v --cov=.
```
