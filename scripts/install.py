#!/usr/bin/env python3
"""
Installasjonsskript for Space Invaders.

Dette skriptet gir brukeren mulighet til å velge mellom
ulike installasjonsmåter for Space Invaders-spillet.
"""
import sys
import os
import subprocess
import argparse

# Finn prosjektmappe
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(script_dir, ".."))

def install_requirements():
    """Installer avhengigheter fra requirements.txt"""
    print("\nInstallerer avhengigheter...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", 
            os.path.join(project_dir, "requirements.txt")
        ])
        print("Avhengigheter installert!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FEIL: Kunne ikke installere avhengigheter: {e}")
        return False

def install_dev_requirements():
    """Installer utviklingsavhengigheter"""
    print("\nInstallerer utviklingsavhengigheter...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "pytest", "coverage", "cx_Freeze", "pylint", "black"
        ])
        print("Utviklingsavhengigheter installert!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FEIL: Kunne ikke installere utviklingsavhengigheter: {e}")
        return False

def install_package():
    """Installer prosjektet som en pakke"""
    print("\nInstallerer Space Invaders som pakke...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], cwd=project_dir)
        print("Pakken installert i utviklingsmodus!")
        print("Du kan nå kjøre spillet med kommandoen 'space-invaders'")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FEIL: Kunne ikke installere pakken: {e}")
        return False

def run_game():
    """Kjør spillet etter installasjon"""
    print("\nStarter spillet...")
    try:
        if os.path.exists(os.path.join(project_dir, "space_invaders.py")):
            subprocess.call([sys.executable, os.path.join(project_dir, "space_invaders.py")])
        else:
            print("FEIL: Finner ikke space_invaders.py")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FEIL: Kunne ikke starte spillet: {e}")
        return False

def main():
    """Hovedfunksjon for installasjonsskriptet"""
    parser = argparse.ArgumentParser(description="Installer Space Invaders")
    parser.add_argument("--dev", action="store_true", help="Installer utviklingsavhengigheter")
    parser.add_argument("--package", action="store_true", help="Installer som pakke")
    parser.add_argument("--run", action="store_true", help="Kjør spillet etter installasjon")
    args = parser.parse_args()

    print("=" * 70)
    print("Space Invaders - Installasjonsverktøy")
    print("=" * 70)
    
    # Hvis ingen argumenter er gitt, spør brukeren
    if not (args.dev or args.package or args.run):
        print("\nVelg installasjonstype:")
        print("1. Installer bare avhengigheter")
        print("2. Installer utviklingsavhengigheter")
        print("3. Installer som pakke (for utvikling)")
        print("4. Installer alt")
        
        choice = input("\nVelg et alternativ (1-4): ")
        
        if choice == "1":
            install_requirements()
        elif choice == "2":
            install_requirements()
            install_dev_requirements()
        elif choice == "3":
            install_requirements()
            install_package()
        elif choice == "4":
            install_requirements()
            install_dev_requirements()
            install_package()
        else:
            print("Ugyldig valg. Avslutter.")
            return
        
        run_game_choice = input("\nVil du starte spillet nå? (j/N): ").lower()
        if run_game_choice == "j":
            run_game()
    else:
        # Installer avhengigheter uansett
        install_requirements()
        
        if args.dev:
            install_dev_requirements()
        
        if args.package:
            install_package()
        
        if args.run:
            run_game()
    
    print("\nInstallasjon fullført!")
    print("God spilling!")

if __name__ == "__main__":
    main() 