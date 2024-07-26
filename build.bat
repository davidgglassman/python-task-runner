@echo off
setlocal enabledelayedexpansion

REM Set the default folders
set "input_folder=_input"
set "output_folder=_output"

REM Check if arguments were provided
if "%~2" neq "" (
    set "input_folder=%~1"
    set "output_folder=%~2"
)

REM Create virtual environment
echo Creating virtual environment
python -m venv "!input_folder!\env"

REM Activate virtual environment
echo Activating virtual environment
call "!input_folder!\env\Scripts\activate.bat"

REM Install packages
echo Installing required packages
pip install -r "!input_folder!\requirements.txt"

REM Run pyinstaller within the same window
echo Running PyInstaller
pyinstaller app.py --onefile --distpath "!input_folder!" --icon "!input_folder!\logo.ico" --add-data "!input_folder!\manifest.json;." --add-data "!input_folder!\tasks;tasks"

REM Deactivate virtual environment
echo Deactivating virtual environment
call "!input_folder!\env\Scripts\deactivate.bat"

REM Clean up folders and move files
echo Cleaning Up
rmdir /s/q build\
mkdir "!output_folder!"
move "!input_folder!\app.exe" "!output_folder!"
rmdir /s/q "!input_folder!\env"

REM Pause at the end to keep the window open if double-clicked
pause