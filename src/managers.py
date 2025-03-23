import os
import json
import math
from src.constants import SCREEN_WIDTH, MAX_DIVERS, DIVE_SPEED, HIGHSCORE_FILE, ALIEN_TYPE_STANDARD, ALIEN_TYPE_SPEEDY, ALIEN_TYPE_TANK
import random
from datetime import datetime

# Highscore-system
class HighscoreManager:
    """Håndterer highscores for spillet"""
    
    def __init__(self, filename="highscores.json"):
        """Initialiserer highscore-manageren"""
        self.filename = filename
        self.highscores = self.load_highscores()
    
    def load_highscores(self):
        """Laster highscores fra fil"""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Hvis filen ikke finnes eller er tom, returner en tom liste
            return []
    
    def save_highscores(self):
        """Lagrer highscores til fil"""
        with open(self.filename, 'w') as f:
            json.dump(self.highscores, f)
    
    def add_score(self, score_data):
        """Legger til en ny score og lagrer den"""
        # Legg til score
        self.highscores.append(score_data)
        
        # Sorter highscores i synkende rekkefølge
        self.highscores = sorted(self.highscores, key=lambda x: x['score'], reverse=True)
        
        # Behold bare de 10 beste
        if len(self.highscores) > 10:
            self.highscores = self.highscores[:10]
        
        # Lagre oppdaterte highscores
        self.save_highscores()
    
    def get_highscores(self):
        """Henter alle highscores"""
        return self.highscores
    
    def get_highest_score(self):
        """Henter høyeste score"""
        if not self.highscores:
            return 0
        return self.highscores[0]['score']
    
    def get_lowest_high_score_entry(self):
        """Henter laveste highscore-oppføring"""
        if not self.highscores or len(self.highscores) < 10:
            return {'score': 0}  # Returner dummy-oppføring hvis det er mindre enn 10 scores
        return self.highscores[-1]
    
    def is_high_score(self, score):
        """Sjekker om en gitt score kvalifiserer som en high score"""
        if len(self.highscores) < 10:
            return True  # Hvis vi har mindre enn 10 highscores, er alle nye scores high scores
        return score > self.get_lowest_high_score_entry()['score']

# Level definitions
class LevelConfigs:
    """Definerer nivåer og vanskelighetsgrader i spillet"""
    
    def __init__(self):
        """Initialiserer nivåkonfigurasjoner"""
        # Definerer base-konfigurasjoner for hvert nivå
        self.level_configs = {
            # Nivå 1: Standard Invaders - Tradisjonell oppstilling
            1: {
                'name': 'Standard Invaders',
                'pattern': 'grid',  # Tradisjonelt rutenettmønster
                'rows': 5,
                'cols': 8,
                'spacing_x': 60,
                'spacing_y': 50,
                'alien_types': [0],  # Kun standard aliens
                'speed_modifier': 0.7,  # Redusert hastighet for første nivå
                'shoot_chance': 0.005,
                'dive_chance': 0.1,
                'max_bullets': 2
            },
            
            # Nivå 2: Advancing Invaders - Raskere nedstigning
            2: {
                'name': 'Advancing Invaders',
                'pattern': 'grid',
                'rows': 5,
                'cols': 9,
                'spacing_x': 55,
                'spacing_y': 45,
                'alien_types': [0, 1],  # Standard og raske aliens
                'speed_modifier': 1.2,  # Raskere enn nivå 1
                'shoot_chance': 0.008,
                'dive_chance': 0.2,
                'max_bullets': 3
            },
            
            # Nivå 3: V-Formation - V-formet angrep
            3: {
                'name': 'V-Formation',
                'pattern': 'v_shape',  # V-formet mønster
                'rows': 4,
                'cols': 9,
                'spacing_x': 60,
                'spacing_y': 50,
                'alien_types': [0, 1],
                'speed_modifier': 1.3,
                'shoot_chance': 0.01,
                'dive_chance': 0.3,
                'max_bullets': 3
            },
            
            # Nivå 4: Diamond Attack - Diamantformasjon
            4: {
                'name': 'Diamond Attack',
                'pattern': 'diamond',  # Diamantformet mønster
                'rows': 4,
                'cols': 9,  # Brukes til å beregne totalt antall aliens
                'spacing_x': 30,
                'spacing_y': 30,
                'alien_types': [0, 1, 2],  # Alle tre alien-typer
                'speed_modifier': 1.4,
                'shoot_chance': 0.012,
                'dive_chance': 0.35,
                'max_bullets': 4
            },
            
            # Nivå 5: Spiral Invasion - Spiralformet invasjon
            5: {
                'name': 'Spiral Invasion',
                'pattern': 'spiral',  # Spiralmønster (nå sirkulært mønster med rotasjon)
                'rows': 6,  # Økt antall rader for flere aliens i sirkelen
                'cols': 8,  # Brukes til å beregne totalt antall aliens
                'spacing_x': 25,
                'spacing_y': 25,
                'alien_types': [1, 2],  # Raske og tank aliens
                'speed_modifier': 1.5,
                'shoot_chance': 0.015,
                'dive_chance': 0.8,  # Økt dykkesjanse for å sikre mer aktivitet
                'max_bullets': 4
            },
            
            # Nivå 6: Scattered Assault - Spredt angrep
            6: {
                'name': 'Scattered Assault',
                'pattern': 'random',  # Tilfeldig mønster
                'rows': 5,
                'cols': 9,
                'spacing_x': 60,
                'spacing_y': 50,
                'alien_types': [0, 1, 2],  # Alle alien-typer
                'speed_modifier': 1.6,
                'shoot_chance': 0.02,
                'dive_chance': 0.5,
                'max_bullets': 5
            },
            
            # Nivå 7: Elite Invaders - Forbedret klassisk formasjon
            7: {
                'name': 'Elite Invaders',
                'pattern': 'grid',  # Tilbake til grid, men med vanskeligere aliens
                'rows': 6,
                'cols': 10,
                'spacing_x': 50,
                'spacing_y': 40,
                'alien_types': [1, 2],  # Bare raske og tank aliens
                'speed_modifier': 1.8,
                'shoot_chance': 0.025,
                'dive_chance': 0.6,
                'max_bullets': 6
            }
        }
    
    def get_level(self, level, wave=1):
        """Henter nivåkonfigurasjon med vanskelighetsgradskalering basert på bølgenummer"""
        # Hvis nivået er høyere enn det vi har definert, loop og skaler opp vanskelighetsgraden
        base_level = ((level - 1) % len(self.level_configs)) + 1
        repetition = (level - 1) // len(self.level_configs)
        
        # Hent basekonfigurasjonen
        config = self.level_configs[base_level].copy()
        
        # Juster vanskelighet basert på bølge (1-3)
        wave_modifier = (wave - 1) * 0.1  # 0, 0.1, 0.2 for wave 1, 2, 3
        
        # Skaler opp vanskeligheten basert på repetisjon (etter første gjennomgang av alle nivåer)
        if repetition > 0:
            # Øk hastighet med 10% for hver repetisjon
            config['speed_modifier'] *= (1 + repetition * 0.1)
            
            # Øk skyte- og dykkesjanse med 10% for hver repetisjon
            config['shoot_chance'] *= (1 + repetition * 0.1)
            config['dive_chance'] *= (1 + repetition * 0.1)
            
            # Cap verdiene for å unngå at spillet blir umulig
            config['speed_modifier'] = min(config['speed_modifier'], 3.0)
            config['shoot_chance'] = min(config['shoot_chance'], 0.05)
            config['dive_chance'] = min(config['dive_chance'], 0.8)
            
            # Legg til flere aliens i høyere nivåer
            if repetition > 1:
                config['rows'] = min(config['rows'] + 1, 8)
                config['cols'] = min(config['cols'] + 1, 12)
        
        # Juster hastighet basert på bølge
        config['speed_modifier'] += wave_modifier
        
        # Juster skyte- og dykkesjanse basert på bølge
        config['shoot_chance'] += wave_modifier * 0.005
        config['dive_chance'] += wave_modifier * 0.05
        
        return config 