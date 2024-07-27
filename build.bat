@echo off
setlocal enabledelayedexpansion

REM Set the default folders
set "app_folder=_application"

REM Check if arguments were provided
if "%~1" neq "" (
    set "app_folder=%~1"
)

REM Create virtual environment
echo Creating virtual environment
python -m venv "!app_folder!\env"

REM Activate virtual environment
echo Activating virtual environment
call "!app_folder!\env\Scripts\activate.bat"

REM Merge default requirements file and custom requirements file into temporary file
echo Merging requirements.txt files
(type "requirements.txt" & echo. & type "!app_folder!\requirements.txt") > "!app_folder!\.requirements.txt"

REM Install packages
echo Installing required packages
pip install -r "!app_folder!\.requirements.txt"

REM Delete existing output folder if it exists
if exist "!app_folder!\app" (
	rmdir /s/q "!app_folder!\app\"
)

if exist "!app_folder!\_build" (
	rmdir /s/q "!app_folder!\_build\"
)

REM Run pyinstaller within the same window
echo Running PyInstaller
pyinstaller app.py --onedir --distpath "!app_folder!" --icon "!app_folder!\logo.ico" --add-data "!app_folder!\manifest.json;." --add-data "!app_folder!\tasks;tasks" --add-data "!app_folder!\env\Lib\site-packages;."

REM Deactivate virtual environment
echo Deactivating virtual environment
call "!app_folder!\env\Scripts\deactivate.bat"

REM Clean up folders and move files
echo Cleaning Up
rmdir /s/q build\
del /Q /F "!app_folder!\.requirements.txt"
rename "!app_folder!\app" _build

REM Pause at the end to keep the window open if double-clicked
pause