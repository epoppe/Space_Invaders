#!/usr/bin/env python3
"""
Build script for creating a Windows executable using cx_Freeze.
"""
import sys
import os
from cx_Freeze import setup, Executable

# Legg til prosjektets rot i Python-stien
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, project_dir)

# Definer hovedfilen
MAIN_FILE = os.path.join(project_dir, "space_invaders.py")

# Definer filer som skal inkluderes
INCLUDE_FILES = [
    (os.path.join(project_dir, "assets"), "assets"),
    (os.path.join(project_dir, "LICENSE"), "LICENSE"),
    (os.path.join(project_dir, "README.md"), "README.md"),
]

# Definer byggevalg
BUILD_OPTIONS = {
    "packages": ["pygame", "os", "sys", "random", "json", "math", "time", "datetime"],
    "excludes": [],
    "include_files": INCLUDE_FILES,
    "include_msvcr": True,
}

# Definer utførbar fil
EXECUTABLES = [
    Executable(
        MAIN_FILE,
        target_name="SpaceInvaders.exe",
        base="Win32GUI" if sys.platform == "win32" else None,
        icon=os.path.join(project_dir, "assets", "icon.ico"),
    )
]

# Kjør oppsett
setup(
    name="Space Invaders",
    version="1.0.0",
    description="En moderne versjon av det klassiske Space Invaders-spillet",
    author="Erik Praskins",
    options={"build_exe": BUILD_OPTIONS},
    executables=EXECUTABLES,
)

print("Bygget fullført! Utførbar fil er i build-mappen.")
print("Merk: Du må ha cx_Freeze installert for å kjøre dette skriptet.")
print("Installer med: pip install cx_Freeze") 