# Space Invaders

En moderne versjon av det klassiske Space Invaders-spillet, implementert i Python med Pygame.

![Space Invaders Screenshot](assets/gameplay.png)

## Funksjoner

- HD-grafikk og animasjoner
- Flere nivåer med økende vanskelighetsgrad
- Forskjellige typer aliens med unik oppførsel
- Bonussystem med spesialeffekter
- Highscore-system
- Lydeffekter og musikk
- Partikkeleffekter for eksplosioner og fyrverkeri

## Installasjon

### Windows

1. Last ned spillet og pakk ut zip-filen
2. Dobbeltklick på `start_game.bat`

### Mac/Linux

1. Last ned spillet og pakk ut zip-filen
2. Åpne en terminal i spillets mappe
3. Gjør start-skriptet kjørbart: `chmod +x start_game.sh`
4. Start spillet: `./start_game.sh`

### Python-installasjon (alle plattformer)

1. Sørg for at du har Python 3.8 eller nyere installert
2. Installer avhengigheter:
   ```
   pip install pygame
   ```
3. Klon eller last ned dette prosjektet
4. Start spillet:
   ```
   python space_invaders.py
   ```

For mer detaljerte instruksjoner, se [INSTALL.md](INSTALL.md).

## Hvordan spille

### Kontroller

- **Piltaster (venstre/høyre)**: Beveg skipet
- **Mellomrom**: Skyt
- **P**: Pause spillet
- **ESC**: Avslutt spillet

### Spillmål

Beskytt jorden fra invaderende aliens! Skyt ned alle aliens for å komme til neste nivå. Unngå deres skudd og ikke la dem lande på planeten.

### Fiende-typer

- **Grønne aliens**: Standard-fiender
- **Cyan aliens**: Raskere og mer manøvrerbare
- **Røde aliens**: Tøffe fiender som krever flere treff

## Utvikling

### Krav for utvikling

- Python 3.8+
- Pygame 2.0.0+
- Støtte for enhetstesting (pytest)
- Kodeformatterere (black, pylint) for bidrag

### Utviklingsmiljø sette opp

1. Klon repoet:
   ```
   git clone https://github.com/erikpraskins/space_invaders.git
   cd space_invaders
   ```

2. Installer i utviklingsmodus:
   ```
   python scripts/install.py --dev
   ```

3. Kjør tester:
   ```
   python scripts/run_tests.py
   ```

### Prosjektstruktur

- `space_invaders.py`: Hovedspillfilen
- `src/`: Modulær kodebase
  - `constants.py`: Spillkonstanter og innstillinger
  - `entities.py`: Klasser for spillentiteter (stjerner, partikler, etc.)
  - `game.py`: Spillmekanikk og logikk
  - `managers.py`: Administrasjon av highscores og nivåer
  - `main.py`: Hovedspilløkke
  - `renderer.py`: Tegnefunksjoner
  - `sprites.py`: Sprite- og grafikkgenerering
  - `utils.py`: Hjelpefunksjoner
  - `run_tests.py`: Test-script
- `scripts/`: Nyttige skript for utvikling og distribusjon
  - `build_exe.py`: Lager en Windows exe-fil
  - `install.py`: Installasjonshjelper
  - `run_tests.py`: Kjører tester med coverage-analyse
  - `update_deps.py`: Oppdaterer avhengigheter

## Testing

For å kjøre tester:

```
python src/run_tests.py
```

For test-coverage-analyse:

```
python scripts/run_tests.py --coverage
```

## Distribusjon

For å bygge en Windows-kjørbar fil:

```
pip install cx_Freeze
python scripts/build_exe.py
```

## Bidrag

Bidrag er velkomne! Se [CONTRIBUTING.md](CONTRIBUTING.md) for retningslinjer om hvordan du kan bidra.

## Lisens

Dette prosjektet er lisensiert under [MIT License](LICENSE).
