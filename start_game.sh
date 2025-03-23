#!/bin/bash

echo "Space Invaders"
echo "============="
echo ""

# Sjekk om Python er installert
if ! command -v python3 &> /dev/null; then
    echo "Python 3 er ikke installert eller er ikke i PATH."
    echo "Vennligst installer Python 3 fra https://www.python.org/"
    echo "Eller bruk din pakkebehandler (apt, brew, etc.)"
    echo ""
    read -p "Trykk ENTER for å avslutte..."
    exit 1
fi

# Sjekk Python-versjon (minimum 3.8)
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [ $(echo "$python_version < 3.8" | bc -l) -eq 1 ]; then
    echo "Python-versjon $python_version er for gammel. Minst versjon 3.8 er påkrevd."
    echo "Vennligst oppgrader Python."
    echo ""
    read -p "Trykk ENTER for å avslutte..."
    exit 1
fi

# Sjekk om pygame er installert
if ! python3 -c "import pygame" &> /dev/null; then
    echo "Pygame er ikke installert. Vil installere det nå..."
    pip3 install pygame
    if [ $? -ne 0 ]; then
        echo "Kunne ikke installere Pygame. Vennligst installer manuelt med 'pip3 install pygame'."
        read -p "Trykk ENTER for å avslutte..."
        exit 1
    fi
fi

# Gjør skriptet kjørbart
chmod +x space_invaders.py 2>/dev/null

# Start spillet
echo "Starter Space Invaders..."
python3 space_invaders.py

# Hvis spillet avsluttes med en feilkode
if [ $? -ne 0 ]; then
    echo ""
    echo "Spillet avsluttet med en feil."
    echo ""
    echo "Hvis du har problemer med å starte spillet, prøv følgende:"
    echo "1. Kjør 'pip3 install pygame' for å sjekke om Pygame er installert riktig."
    echo "2. Sjekk at Python 3.8 eller nyere er installert med 'python3 --version'."
    echo ""
    read -p "Trykk ENTER for å avslutte..."
fi 