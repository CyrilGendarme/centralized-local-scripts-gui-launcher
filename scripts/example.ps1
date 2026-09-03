@echo off
REM Example PowerShell Script for Windows
REM This script demonstrates basic PowerShell operations

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Scripts Launcher - PowerShell Demo" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Current Date & Time:" -ForegroundColor Yellow
Get-Date

Write-Host ""
Write-Host "Current Directory:" -ForegroundColor Yellow
Get-Location

Write-Host ""
Write-Host "Available Drives:" -ForegroundColor Yellow
Get-Volume | Select-Object DriveLetter, FileSystemLabel, Size

Write-Host ""
Write-Host "✓ Demo completed successfully!" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to close this window"
