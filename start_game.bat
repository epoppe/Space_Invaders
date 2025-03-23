@echo off
echo Space Invaders
echo =============
echo.

REM Sjekk om Python er installert
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python er ikke installert eller er ikke i PATH.
    echo Vennligst installer Python fra https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Sjekk om pygame er installert
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pygame er ikke installert. Vil installere det nå...
    pip install pygame
    if %errorlevel% neq 0 (
        echo Kunne ikke installere Pygame. Vennligst installer manuelt med 'pip install pygame'.
        pause
        exit /b 1
    )
)

REM Start spillet
echo Starter Space Invaders...
python space_invaders.py

REM Hvis spillet avsluttes med en feilkode
if %errorlevel% neq 0 (
    echo.
    echo Spillet avsluttet med en feil (kode %errorlevel%).
    echo.
    echo Hvis du har problemer med å starte spillet, prøv følgende:
    echo 1. Kjør 'python -m pip install pygame' for å sjekke om Pygame er installert riktig.
    echo 2. Sjekk at Python 3.8 eller nyere er installert med 'python --version'.
    echo.
    pause
) 