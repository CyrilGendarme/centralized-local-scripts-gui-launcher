. "$PSScriptRoot\vps_radio_common.ps1"
$name = Read-Host "Component to follow (radio / switcher / mediamtx) [radio]"
if ([string]::IsNullOrWhiteSpace($name)) { $name = "radio" }
if ($name -notin @("radio", "switcher", "mediamtx")) { Write-Host "Unknown component: $name" -ForegroundColor Red; Read-Host "Press Enter to close"; exit 1 }
Write-Host "Ctrl+C stops following." -ForegroundColor DarkGray
Invoke-VpsRadio -Action "logs $name" -Title "VPS Radio logs: $name"
