@echo off
set PYTHON=C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe
set MOSHPRO=C:\Program Files\Mosh-Pro\Mosh-Pro.exe
set EFFECTS_DIR=C:\Users\User\Desktop\ProjetsIT\audio-analysis-data-to-moshpro-effects
set GLUE_GUI=C:\Users\User\Desktop\ProjetsIT\moshpro-spout-obs-glue-script\src\gui\main_gui.py
set GLUE_DIR=C:\Users\User\Desktop\ProjetsIT\moshpro-spout-obs-glue-script

echo Launching Mosh-Pro dynamic effects setup...

if not exist "%MOSHPRO%" (
    echo ERROR: Mosh-Pro not found at %MOSHPRO%
    pause
    exit /b 1
)

start "" /D "C:\Program Files\Mosh-Pro" "%MOSHPRO%"
timeout /t 5 >nul

start "Audio analysis -> Mosh-Pro effects" /D "%EFFECTS_DIR%" "%PYTHON%" "%EFFECTS_DIR%\main.py"
timeout /t 2 >nul

start "Mosh-Pro Spout -> OBS glue" /D "%GLUE_DIR%" "%PYTHON%" "%GLUE_GUI%"

echo All programs launched.
timeout /t 3 >nul