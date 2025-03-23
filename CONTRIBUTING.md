# Bidragsguide for Space Invaders

Takk for at du vurderer å bidra til Space Invaders-prosjektet! Dette dokumentet inneholder retningslinjer for å bidra med kode, dokumentasjon eller feilrapporter.

## Hvordan bidra

### Rapportere problemer (Issues)

1. Sjekk først om problemet allerede er rapportert.
2. Bruk issue-malen hvis tilgjengelig.
3. Inkluder så mye informasjon som mulig:
   - Nøyaktig beskrivelse av problemet
   - Steg for å reprodusere
   - Forventet vs. faktisk oppførsel
   - Skjermbilder hvis relevant
   - Operativsystem og Python-versjon

### Pull Requests

1. Fork repoet og opprett en ny branch fra `main`
2. Bruk en beskrivende branch-navn som relaterer til endringen du gjør
3. Følg kodestil og konvensjoner (se nedenfor)
4. Oppdater dokumentasjon hvis relevant
5. Inkluder tester for ny funksjonalitet
6. Sørg for at alle tester passerer før du sender PR
7. Lag en tydelig PR-beskrivelse som forklarer:
   - Hva endringen gjør
   - Hvorfor den er nødvendig
   - Eventuelle avveininger eller kompromisser

## Utviklingsmiljø

1. Clone repoet:
   ```
   git clone https://github.com/erikpraskins/space_invaders.git
   cd space_invaders
   ```

2. Installer avhengigheter og utviklingsverktøy:
   ```
   python scripts/install.py --dev
   ```

3. Kjør tester for å sjekke at alt fungerer:
   ```
   python scripts/run_tests.py
   ```

## Kodestil og konvensjoner

- Følg PEP 8 for Python-kode
- Bruk dokumentasjonsstrenger (docstrings) for alle funksjoner og klasser
- Hold koden DRY (Don't Repeat Yourself)
- Bruk beskrivende variabel- og funksjonsnavn
- Kommentér kompleks logikk, men unngå overdrevent åpenbare kommentarer
- Maksimal linjelengde er 88 tegn
- Kjør `black` kodeformaterer før du committer:
  ```
  black src/
  ```

## Teststrategi

- Alle nye funksjoner bør ha tilhørende tester
- Kjør testene før du sender PR:
  ```
  python scripts/run_tests.py
  ```
- For test-coverage-analyse:
  ```
  python scripts/run_tests.py --coverage
  ```

## Prosjektstruktur

- `space_invaders.py`: Hovedinngangsfilpunkt
- `src/`: Modulær kodebase
  - `constants.py`: Spillkonstanter og innstillinger
  - `entities.py`: Klasser for spillentiteter
  - `game.py`: Spillmekanikk og logikk
  - `managers.py`: Administrasjon av highscores og nivåer
  - `main.py`: Hovedspilløkke
  - `renderer.py`: Tegnefunksjoner
  - `sprites.py`: Sprite- og grafikkgenerering
  - `utils.py`: Hjelpefunksjoner
  - `run_tests.py`: Test-script

## Releaseplan

Prosjektet bruker semantisk versjonering (MAJOR.MINOR.PATCH):
- MAJOR: Inkompatible API-endringer
- MINOR: Bakoverkompatibel funksjonalitet
- PATCH: Bakoverkompatible bugfikser

## Lisens

Ved å bidra til dette prosjektet, samtykker du til at bidragene dine vil bli lisensiert under MIT-lisensen. 