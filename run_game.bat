@echo off
setlocal

echo Checking Python 3.11...
py -3.11 --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.11 tidak ditemukan.
    echo Install dulu Python 3.11 kemudian coba lagi.
    pause
    exit /b 1
)

echo Creating venv...
py -3.11 -m venv .venv

echo Activating venv...
call .venv\Scripts\activate

echo Installing dependencies...
pip install pygame pyopengl numpy

echo Running main.py...
py main.py

echo Deactivating venv...
deactivate

echo Done.
pause