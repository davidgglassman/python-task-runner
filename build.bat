@echo off
setlocal

REM Create virtual environment
python -m venv env

REM Activate virtual environment
call env\Scripts\activate.bat

REM Install packages
pip install -r requirements.txt

REM Run pyinstaller within the same window
pyinstaller app.spec --distpath .

REM Deactivate virtual environment
deactivate