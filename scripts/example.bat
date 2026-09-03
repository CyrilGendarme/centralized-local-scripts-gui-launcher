@echo off
REM Example Windows Batch Script
REM This script demonstrates basic batch file operations

setlocal enabledelayedexpansion

echo.
echo ==================================
echo Scripts Launcher - Batch Demo
echo ==================================
echo.

echo Current Date and Time:
echo %date% %time%
echo.

echo Current Directory:
cd
echo.

echo System Information:
echo Processor: %PROCESSOR_IDENTIFIER%
echo OS: %OS%
echo.

echo Available Environment Variables:
echo USERNAME: %USERNAME%
echo COMPUTERNAME: %COMPUTERNAME%
echo USERPROFILE: %USERPROFILE%
echo.

echo Listing Files in Current Directory:
dir /b
echo.

echo Done! Script execution completed successfully.
echo.

pause
