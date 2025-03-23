# Installasjonsveiledning for Space Invaders

## Forutsetninger

- Python 3.8 eller nyere
- pip (Python pakkehåndterer)

## Metode 1: Installere med pip

1. Klon eller last ned prosjektet:
   ```
   git clone https://github.com/erikpraskins/space_invaders.git
   cd space_invaders
   ```

2. Installer pakken i utviklingsmodus:
   ```
   pip install -e .
   ```

3. Start spillet via kommandolinjen:
   ```
   space-invaders
   ```

## Metode 2: Kjøre direkte uten installasjon

1. Klon eller last ned prosjektet:
   ```
   git clone https://github.com/erikpraskins/space_invaders.git
   cd space_invaders
   ```

2. Installer avhengigheter:
   ```
   pip install -r requirements.txt
   ```

3. Kjør spillet direkte:
   ```
   python space_invaders.py
   ```
   
   Eller:
   ```
   python -m src
   ```

## Metode 3: Installere fra PyPI (ikke tilgjengelig ennå)

Når pakken er publisert på PyPI, kan du installere den direkte:

```
pip install space-invaders
```

Og deretter kjøre:

```
space-invaders
```

## Feilsøking

### Pygame ikke installert

Hvis du får en feilmelding om at Pygame ikke er installert, kjør:

```
pip install pygame
```

### Filrettigheter (Linux/Mac)

Hvis du får feilmeldinger relatert til filrettigheter på Linux eller Mac, prøv:

```
chmod +x space_invaders.py
./space_invaders.py
```

### Skjermstørrelse

Hvis spillet vises feil på skjermen din, kan du justere skjermstørrelsen i `src/constants.py`. 