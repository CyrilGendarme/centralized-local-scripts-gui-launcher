# Shared settings and helpers for the "VPS Radio" launcher buttons.
# The radio runs on the VPS from linux-ffmpeg-continuous-livestream (radiofull.sh)
# and its control webapp is served by start_control_api.py on port 8443.
#
# Override any setting without editing this file by creating
# vps_radio_local.ps1 next to it (untracked), e.g.:
#   $VpsSshHost = "myvps"
#   $VpsWebUrl  = "https://radio.example.com"

$VpsSshHost   = "hop"                                     # alias from ~/.ssh/config
$VpsRemoteDir = "~/linux-ffmpeg-continuous-livestream"   # repo path on the VPS
$VpsWebUrl    = "https://stream.popuri.fm"               # control webapp base URL (nginx -> :8443)

$localSettings = Join-Path $PSScriptRoot "vps_radio_local.ps1"
if (Test-Path $localSettings) { . $localSettings }

function Get-SshExe {
    # Prefer Windows OpenSSH: it uses ~/.ssh/config, known_hosts and the ssh-agent service.
    $winSsh = Join-Path $env:SystemRoot "System32\OpenSSH\ssh.exe"
    if (Test-Path $winSsh) { return $winSsh }
    $cmd = Get-Command ssh -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    throw "ssh not found. Install the Windows OpenSSH client."
}

function Invoke-VpsRadio {
    param(
        [Parameter(Mandatory)] [string] $Action,   # start|stop|restart|status|logs <name>
        [string] $Title = "VPS Radio: $Action"
    )
    $Host.UI.RawUI.WindowTitle = $Title
    $ssh = Get-SshExe
    $remote = "cd $VpsRemoteDir && ./radiofull.sh $Action"
    Write-Host "[$VpsSshHost] $remote" -ForegroundColor Cyan
    Write-Host ""
    # -t: a TTY so sudo (WireGuard on start) can ask for the password, and Ctrl+C stops 'logs'.
    & $ssh -t $VpsSshHost $remote
    $rc = $LASTEXITCODE
    Write-Host ""
    if ($rc -eq 0) {
        Write-Host "Done." -ForegroundColor Green
    } else {
        Write-Host "Exited with code $rc." -ForegroundColor Red
    }
    Read-Host "Press Enter to close"
}

function Open-VpsRadioPage {
    param([Parameter(Mandatory)] [string] $Path)
    $url = $VpsWebUrl.TrimEnd("/") + "/" + $Path.TrimStart("/")
    Write-Host "Opening $url"
    Start-Process $url
}
