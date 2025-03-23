#!/usr/bin/env python3
"""
Oppdaterer alle avhengigheter for Space Invaders-prosjektet.
Dette skriptet sjekker og oppdaterer avhengighetene som er definert i requirements.txt.
"""
import sys
import os
import subprocess
import pkg_resources

# Finn prosjektmappe
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(script_dir, ".."))

def get_installed_packages():
    """Returner oversikt over installerte pakker og deres versjoner"""
    installed = {}
    for dist in pkg_resources.working_set:
        installed[dist.project_name] = dist.version
    return installed

def get_requirements():
    """Les requirements.txt og returner pakkenavn og versjoner"""
    requirements_path = os.path.join(project_dir, "requirements.txt")
    if not os.path.exists(requirements_path):
        print(f"FEIL: Finner ikke {requirements_path}")
        return {}
    
    requirements = {}
    with open(requirements_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # Fjern eventuelle kommentarer
            if "#" in line:
                line = line.split("#")[0].strip()
            
            # Håndter ulike formater for versjonskrav
            if "==" in line:
                name, version = line.split("==")
                requirements[name] = {"version": version, "constraint": "=="}
            elif ">=" in line:
                name, version = line.split(">=")
                requirements[name] = {"version": version, "constraint": ">="}
            elif "<=" in line:
                name, version = line.split("<=")
                requirements[name] = {"version": version, "constraint": "<="}
            else:
                requirements[line] = {"version": None, "constraint": None}
    
    return requirements

def update_packages():
    """Oppdater alle pakker som er definert i requirements.txt"""
    print("Oppdaterer avhengigheter...")
    
    installed = get_installed_packages()
    requirements = get_requirements()
    
    print("\nInstallerte pakker:")
    for name, version in installed.items():
        if name.lower() in [pkg.lower() for pkg in requirements.keys()]:
            print(f"  - {name} (v{version})")
    
    print("\nAvhengigheter fra requirements.txt:")
    for name, info in requirements.items():
        version_str = f"{info['constraint']}{info['version']}" if info['version'] else "nyeste versjon"
        print(f"  - {name} ({version_str})")
    
    # Spør bruker om de ønsker å oppdatere
    answer = input("\nVil du oppdatere alle avhengigheter? (j/N): ").lower()
    if answer != "j":
        print("Avbryter oppdatering.")
        return
    
    print("\nOppdaterer pakker...")
    try:
        # Installer avhengigheter fra requirements.txt
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", 
            os.path.join(project_dir, "requirements.txt")
        ])
        print("\nVellykket oppdatering av avhengigheter!")
    except subprocess.CalledProcessError as e:
        print(f"\nFEIL: Kunne ikke oppdatere avhengigheter: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 70)
    print("Space Invaders - Avhengighetsoppdatering")
    print("=" * 70)
    
    update_packages()
    
    print("\nHvis du vil installere utviklingsavhengigheter, kjør:")
    print("  pip install pytest coverage cx_Freeze") 