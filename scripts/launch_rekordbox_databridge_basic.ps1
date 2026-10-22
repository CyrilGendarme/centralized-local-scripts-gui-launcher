# Rekordbox + DataBridge Basic (Partial) - Launch script
# Launches Rekordbox and the rekordbox-databridge in basic GUI mode

$ErrorActionPreference = "Stop"

# Store process IDs for cleanup
$global:ProcessIds = @()

# Cleanup function to be called on exit
function Cleanup-Processes {
    Write-Host "Cleaning up processes..."
    foreach ($proc_id in $global:ProcessIds) {
        try {
            $process = Get-Process -Id $proc_id -ErrorAction SilentlyContinue
            if ($process) {
                Write-Host "Terminating process $proc_id..."
                Stop-Process -Id $proc_id -Force -ErrorAction SilentlyContinue
                Start-Sleep -Milliseconds 500
            }
        } catch {
            # Process already terminated
        }
    }
}

# Register cleanup on script exit
$null = Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action { Cleanup-Processes }

# Wrap entire script execution in try-catch for better error handling
try {
    # Launch Rekordbox and wait until it is fully launched (main window up and responding)
    $RekordboxExePath = Get-ChildItem -Path "C:\Program Files\rekordbox\*\rekordbox.exe" -ErrorAction SilentlyContinue |
        Sort-Object -Property CreationTime -Descending |
        Select-Object -First 1 -ExpandProperty FullName

    $RekordboxTimeoutSeconds = 180
    $rekordboxRunning = Get-Process -Name "rekordbox" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 }

    if (-not $rekordboxRunning) {
        if (-not $RekordboxExePath) {
            throw "Rekordbox not found under C:\Program Files\rekordbox"
        }

        # Created through WMI so Rekordbox is not a child of this console: closing the CLI windows will not close it
        $created = ([wmiclass]"\\.\root\cimv2:Win32_Process").Create(@(
            CommandLine      = "`"$RekordboxExePath`""
            CurrentDirectory = (Split-Path -Parent $RekordboxExePath)
        ))

        if ($created.ReturnValue -ne 0) { throw "Failed to launch Rekordbox (WMI return code $($created.ReturnValue))" }
        Write-Host "Launched Rekordbox"
    } else {
        Write-Host "Rekordbox is already running"
    }

    Write-Host "Waiting for Rekordbox to be fully launched..."
    $deadline = (Get-Date).AddSeconds($RekordboxTimeoutSeconds)
    $rekordboxReady = $false

    while ((Get-Date) -lt $deadline) {
        $rb = Get-Process -Name "rekordbox" -ErrorAction SilentlyContinue |
            Where-Object { $_.MainWindowHandle -ne 0 }
        if ($rb) { $rekordboxReady = $true; break }
        Start-Sleep -Milliseconds 500
    }

    if (-not $rekordboxReady) {
        throw "Rekordbox did not become ready within $RekordboxTimeoutSeconds seconds"
    }

    Write-Host "Rekordbox window detected, waiting 20 seconds for it to finish loading..."
    Start-Sleep -Seconds 20
    Write-Host "Rekordbox is ready"

    # Paths
    $Python = "python"    # Or: "C:\path\to\venv\Scripts\python.exe"
    $DataBridgeMainPath = "C:\Users\User\Desktop\ProjetsIT\rekordbox-databridge\main.py"

    function Resolve-ScriptPath {
        param(
            [Parameter(Mandatory = $true)]
            [string]$Path
        )

        if (-not (Test-Path -LiteralPath $Path)) {
            throw "Script not found: $Path"
        }

        return (Resolve-Path -LiteralPath $Path).Path
    }

    function Stop-ExistingScriptProcess {
        param(
            [Parameter(Mandatory = $true)]
            [string]$ScriptPath
        )

        $escapedPath = [regex]::Escape($ScriptPath)
        $existing = Get-CimInstance Win32_Process |
            Where-Object {
                $_.Name -match "python|py" -and
                $_.CommandLine -and
                $_.CommandLine -match $escapedPath
            }

        foreach ($proc in $existing) {
            Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped existing process for $ScriptPath (PID $($proc.ProcessId))"
        }
    }

    # Function to launch a script and track its process ID
    function Start-PythonScript {
        param (
            [string]$ScriptPath,
            [string]$LaunchScenario
        )

        $resolvedScriptPath = Resolve-ScriptPath -Path $ScriptPath
        $scriptDirectory = Split-Path -Parent $resolvedScriptPath
        $lastWriteTime = (Get-Item -LiteralPath $resolvedScriptPath).LastWriteTime

        Stop-ExistingScriptProcess -ScriptPath $resolvedScriptPath

        Write-Host "Launching: $resolvedScriptPath"
        Write-Host "LastWriteTime: $lastWriteTime"
        
        # Build PowerShell command to run the script with environment variables
        $command = @"
Write-Host "Launching: $resolvedScriptPath"
Write-Host "LastWriteTime: $lastWriteTime"
Set-Location -LiteralPath '$scriptDirectory'

`$env:LAUNCH_SCENARIO = '$LaunchScenario'
`$env:PRODJ_LOG_LEVEL = 'ERROR'
`$env:PYTHONDONTWRITEBYTECODE = '1'

try {
    & '$Python' -B '$resolvedScriptPath'
} catch {
    Write-Host "Script error: `$_" -ForegroundColor Red
    Write-Host "Press Enter to close this window..."
    Read-Host ""
}
"@

        # Launch PowerShell window with -NoExit so it stays open on error
        $process = Start-Process -FilePath powershell `
            -ArgumentList "-NoExit", "-Command", $command `
            -WorkingDirectory $scriptDirectory `
            -PassThru
        
        $global:ProcessIds += $process.Id
        
        Write-Host "Started PowerShell process with PID $($process.Id)"
    }

    # Launch the DataBridge script with basic GUI
    Start-PythonScript -ScriptPath $DataBridgeMainPath -LaunchScenario "GUI"

    Write-Host "All scripts launched. Press Ctrl+C to gracefully shutdown..."

    # Keep the script running and wait for Ctrl+C
    try {
        while ($true) {
            # Monitor processes and exit if all are gone
            $allProcessesAlive = $true
            foreach ($proc_id in $global:ProcessIds) {
                $process = Get-Process -Id $proc_id -ErrorAction SilentlyContinue
                if (-not $process) {
                    $allProcessesAlive = $false
                    Write-Host "⚠️  Process $proc_id has exited" -ForegroundColor Yellow
                }
            }

            if (-not $allProcessesAlive) {
                Write-Host "All processes have exited. Script will close in 5 seconds..."
                Start-Sleep -Seconds 5
                break
            }

            Start-Sleep -Seconds 1
        }
    } catch {
        Write-Host "Error in monitoring loop: $_" -ForegroundColor Red
    }
} catch {
    Write-Host "Fatal error: $_" -ForegroundColor Red
    Write-Host "Press Enter to close this window..."
    Read-Host ""
    exit 1
}

Write-Host "Script cleanup complete"
