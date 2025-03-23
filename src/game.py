import pygame
import random
import math
import numpy as np
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT,
    BULLET_WIDTH, BULLET_HEIGHT, ALIEN_BULLET_WIDTH, ALIEN_BULLET_HEIGHT,
    BULLET_SPEED, ALIEN_BULLET_SPEED, PLAYER_SPEED, ALIEN_WIDTH, ALIEN_HEIGHT,
    DIVE_SPEED, DIVE_CHANCE, MAX_DIVERS, VERTICAL_STEP, SWAY_SPEED, SWAY_AMPLITUDE,
    ALIEN_SHOOT_CHANCE, BASE_ALIEN_SPEED, SPEED_INCREASE,
    ALIEN_TYPE_STANDARD, ALIEN_TYPE_SPEEDY, ALIEN_TYPE_TANK
)
from src.entities import Particle, FireworkParticle

# Definer manglende farger
NEON_RED = (255, 60, 60)

# Funksjoner for å håndtere aliens
def create_aliens(level_config):
    """Oppretter aliens basert på level-konfigurasjon"""
    aliens = []
    pattern = level_config['pattern']
    rows = level_config['rows']
    cols = level_config['cols']
    spacing_x = level_config['spacing_x']
    spacing_y = level_config['spacing_y']
    alien_types = level_config['alien_types']
    
    # Bestem hvilken mønsterfunksjon som skal brukes
    if pattern == 'grid':
        positions = create_grid_pattern(rows, cols, spacing_x, spacing_y)
    elif pattern == 'v_shape':
        positions = create_v_shape_pattern(rows, cols, spacing_x, spacing_y)
    elif pattern == 'diamond':
        positions = create_diamond_pattern(rows, cols, spacing_x, spacing_y)
    elif pattern == 'spiral':
        # Bruk sirkel-mønster for Level 5
        positions = create_circle_pattern(rows * cols, spacing_x, spacing_y)
    elif pattern == 'random':
        positions = create_random_pattern(rows * cols, spacing_x, spacing_y)
    else:
        # Standard grid som fallback
        positions = create_grid_pattern(rows, cols, spacing_x, spacing_y)
    
    # Opprett aliens basert på posisjonene
    for i, pos in enumerate(positions):
        x, y = pos
        
        # Bestem alien-type basert på level-konfigurasjon
        if len(alien_types) == 1:
            # Hvis bare én type, bruk den for alle
            alien_type = alien_types[0]
        else:
            # Ellers, velg type basert på posisjon og tilgjengelige typer
            if pattern in ['grid', 'v_shape']:
                # For grid og v-shape: mer avanserte aliens på bunnen, enkle på toppen
                row_index = i // cols
                row_normalized = row_index / max(1, rows - 1)  # Normaliser til 0-1
                type_index = min(len(alien_types) - 1, int(row_normalized * len(alien_types)))
                alien_type = alien_types[type_index]
            else:
                # For andre mønstre: tilfeldig fordeling av alien-typer
                alien_type = random.choice(alien_types)
        
        # Bestem hvilken rad alien er i (basert på mønster)
        if pattern in ['grid', 'v_shape']:
            row_index = i // cols
            # Vi bruker row_index til å definere fargen
        elif pattern == 'diamond':
            # For diamant, bruk y-posisjon for å estimere rad
            y_positions = [pos[1] for pos in positions]
            unique_y = sorted(list(set(y_positions)))
            row_index = unique_y.index(y)
        else:
            # For andre mønstre, bruk y-posisjon for å estimere rad
            normalized_y = (y - min([p[1] for p in positions])) / max(1, max([p[1] for p in positions]) - min([p[1] for p in positions]))
            row_index = int(normalized_y * (rows - 1))
        
        # Bestem om alien kan skyte
        can_shoot = random.random() < level_config['shoot_chance']
        
        # Bestem om alien kan dykke
        can_dive = random.random() < level_config['dive_chance']
        
        # Opprett alien-dict
        alien = {
            'rect': pygame.Rect(x, y, ALIEN_WIDTH, ALIEN_HEIGHT),
            'type': alien_type,
            'direction': 1,  # 1 = høyre, -1 = venstre
            'can_shoot': can_shoot,
            'can_dive': can_dive,
            'shooting_cooldown': random.randint(30, 120),  # Tilfeldig initial cooldown
            'diving': False,
            'dive_target_x': 0,
            'dive_target_y': 0,
            'original_x': x,
            'original_y': y,
            'dive_progress': 0,
            'dive_speed': random.uniform(0.006, 0.015),
            'health': 1 if alien_type == ALIEN_TYPE_STANDARD else 
                      2 if alien_type == ALIEN_TYPE_SPEEDY else 
                      3,  # ALIEN_TYPE_TANK
            'row_index': row_index  # Lagre rad-indeksen for å bruke den ved rendering
        }
        aliens.append(alien)
    
    return aliens

def create_grid_pattern(rows, cols, spacing_x, spacing_y):
    """Opprett et rutenettmønster med aliens"""
    positions = []
    start_x = (SCREEN_WIDTH - (cols * spacing_x)) // 2
    start_y = 50  # Start litt ned fra toppen av skjermen
    
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y
            positions.append((x, y))
    
    return positions

def create_v_shape_pattern(rows, cols, spacing_x, spacing_y):
    """Opprett et V-formet mønster med aliens"""
    positions = []
    center_col = cols // 2
    
    for row in range(rows):
        for col in range(cols):
            # Beregn avstand fra midtkolonnen
            dist_from_center = abs(col - center_col)
            
            # Juster y-posisjon basert på avstand fra midten (lager V-form)
            y_offset = dist_from_center * spacing_y * 0.5
            
            x = (SCREEN_WIDTH - (cols * spacing_x)) // 2 + col * spacing_x
            y = 50 + row * spacing_y + y_offset
            
            positions.append((x, y))
    
    return positions

def create_diamond_pattern(rows, cols, spacing_x, spacing_y):
    """Opprett et diamantformet mønster med aliens"""
    positions = []
    center_x = SCREEN_WIDTH // 2
    center_y = 150  # Sentrum av diamanten
    
    # Beregn maksimal radius for diamanten
    max_radius = min(rows, cols) * spacing_x // 2
    
    # Total antall aliens
    num_aliens = rows * cols
    
    # Opprett diamantmønster
    for i in range(num_aliens):
        angle = 2 * math.pi * i / num_aliens
        # Bruk en hjerteformel for å lage diamantform
        radius = max_radius * (1 - 0.5 * math.sin(angle) ** 2)
        
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        positions.append((x, y))
    
    return positions

def create_spiral_pattern(num_aliens, spacing_x, spacing_y):
    """Opprett et spiralmønster med aliens"""
    positions = []
    center_x = SCREEN_WIDTH // 2
    center_y = 150  # Sentrum av spiralen
    
    # Parametre for spiral
    a = 0.1  # Bestemmer hvor "tett" spiralen er
    b = 5    # Bestemmer startradius
    
    for i in range(num_aliens):
        # Parametrisk spiralformel
        t = 0.3 * i
        r = a * t + b
        x = center_x + r * math.cos(t) * spacing_x / 30
        y = center_y + r * math.sin(t) * spacing_y / 30
        
        positions.append((x, y))
    
    return positions

def create_circle_pattern(num_aliens, spacing_x, spacing_y):
    """Opprett et sirkulært mønster med aliens for Level 5"""
    positions = []
    center_x = SCREEN_WIDTH // 2
    center_y = 180  # Sentrum av sirkelen, litt lavere enn spiral
    
    # Beregn radius for sirkelen
    radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) / 4
    
    # Fordel alienene jevnt i en sirkel
    for i in range(num_aliens):
        angle = (2 * math.pi * i) / num_aliens
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        # Legg til en liten variasjon i radius for å gjøre det mer interessant
        if i % 3 == 0:
            x = center_x + (radius - 20) * math.cos(angle)
            y = center_y + (radius - 20) * math.sin(angle)
        
        positions.append((x, y))
    
    return positions

def create_random_pattern(num_aliens, spacing_x, spacing_y):
    """Opprett et tilfeldig mønster med aliens"""
    positions = []
    
    # Definerer området der aliens kan plasseres
    min_x = spacing_x
    max_x = SCREEN_WIDTH - spacing_x - ALIEN_WIDTH
    min_y = spacing_y
    max_y = SCREEN_HEIGHT // 3  # Bare bruk øvre tredjedel av skjermen
    
    # Opprett tilfeldige posisjoner, men unngå overlapping
    for _ in range(num_aliens):
        valid_position = False
        attempts = 0
        
        while not valid_position and attempts < 50:
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            
            # Sjekk om denne posisjonen overlapper med eksisterende posisjoner
            overlapping = False
            for pos in positions:
                px, py = pos
                if (abs(px - x) < spacing_x * 0.8 and 
                    abs(py - y) < spacing_y * 0.8):
                    overlapping = True
                    break
            
            if not overlapping:
                valid_position = True
                positions.append((x, y))
            
            attempts += 1
        
        # Hvis vi ikke fant en gyldig posisjon etter 50 forsøk, bare plasser i grid
        if not valid_position:
            row = len(positions) // 10
            col = len(positions) % 10
            x = min_x + col * spacing_x
            y = min_y + row * spacing_y
            positions.append((x, y))
    
    return positions

def update_aliens(aliens, speed, level_config):
    """Oppdater posisjoner og oppførsel for aliens"""
    # Sjekk om vi er på Level 5 (Spiral Invasion) - den bruker nå sirkelrotasjon
    pattern = level_config.get('pattern', 'grid')
    is_level5_circle = pattern == 'spiral'
    
    if is_level5_circle:
        update_circle_aliens(aliens, speed)
        return
    
    # Standard oppdatering for andre nivåer
    # Sjekk om noen alien treffer kanten av skjermen
    change_direction = False
    lowest_y = 0
    
    # Finn først ut om vi trenger å endre retning og hva som er laveste y-verdi
    for alien in aliens:
        if not alien['diving']:  # Bare sjekk aliens som ikke dykker
            alien_rect = alien['rect']
            if (alien_rect.right >= SCREEN_WIDTH and alien['direction'] > 0) or \
               (alien_rect.left <= 0 and alien['direction'] < 0):
                change_direction = True
            if alien_rect.y > lowest_y:
                lowest_y = alien_rect.y
    
    # Oppdater hver alien basert på tilstanden
    for alien in aliens:
        if alien['diving']:
            # Oppdater aliens som dykker med bezier-kurve
            update_diving_alien(alien)
        else:
            # Oppdater normale aliens som beveger seg sidelengs
            multiplier = 1.5 if alien['type'] == ALIEN_TYPE_SPEEDY else 1.0
            
            if change_direction:
                alien['direction'] *= -1
                # Flytt ned hvis vi endrer retning og ikke er for langt nede
                if lowest_y < SCREEN_HEIGHT - 200:
                    alien['rect'].y += 20
            
            # Flytt alien sidelengs
            alien['rect'].x += alien['direction'] * speed * multiplier
        
        # Oppdater skyting cooldown
        if alien['can_shoot'] and alien['shooting_cooldown'] > 0:
            alien['shooting_cooldown'] -= 1

def update_circle_aliens(aliens, speed):
    """Spesiell oppdateringsfunksjon for Level 5 med roterende sirkel"""
    # Finn sentrum av sirkel
    center_x = SCREEN_WIDTH // 2
    center_y = 180
    
    # Initialiser rotasjonsteller hvis den ikke finnes
    if not hasattr(update_circle_aliens, "angle"):
        update_circle_aliens.angle = 0
        update_circle_aliens.radius_pulsation = 0
        update_circle_aliens.dive_counter = 0
    
    # Øk rotasjonsvinkel
    update_circle_aliens.angle += 0.01 * speed
    update_circle_aliens.radius_pulsation += 0.02
    
    # Pulsering for radius
    radius_mod = math.sin(update_circle_aliens.radius_pulsation) * 20
    
    # Marker første alien som starter sirkulær dykking
    update_circle_aliens.dive_counter += 1
    should_dive = update_circle_aliens.dive_counter >= 60  # Omtrent hvert sekund
    has_diver = False
    
    # Oppdater hver alien
    for i, alien in enumerate(aliens):
        if alien['diving']:
            # Bruk standard dykking
            update_diving_alien(alien)
            has_diver = True
            continue
        
        # Beregn ny posisjon i sirkel med rotasjon
        base_angle = (2 * math.pi * i) / len(aliens) + update_circle_aliens.angle
        
        # Variasjon i radius
        radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) / 4
        if i % 3 == 0:
            radius = radius - 20 + radius_mod  # Pulserende effekt
        else:
            radius = radius + radius_mod
        
        # Beregn ny posisjon
        new_x = center_x + radius * math.cos(base_angle)
        new_y = center_y + radius * math.sin(base_angle)
        
        # Oppdater alien-posisjon
        alien['rect'].x = new_x
        alien['rect'].y = new_y
        
        # Lagre original posisjon for dykking
        alien['original_x'] = new_x
        alien['original_y'] = new_y
        
        # Sjekk om alien skal dykke
        if should_dive and not has_diver and alien['can_dive'] and random.random() < 0.3:
            # Start dykking fra sirkel
            alien['diving'] = True
            alien['dive_progress'] = 0
            
            # Sett mål til et tilfeldig punkt nær bunnen av skjermen
            alien['dive_target_x'] = random.randint(100, SCREEN_WIDTH - 100)
            alien['dive_target_y'] = random.randint(SCREEN_HEIGHT - 150, SCREEN_HEIGHT - 50)
            
            # Sett innstillinger for dykking
            alien['dive_speed'] = random.uniform(0.006, 0.01)
            has_diver = True
    
    # Reset dykketeller hvis vi har startet en dykking
    if has_diver and should_dive:
        update_circle_aliens.dive_counter = 0

def update_diving_alien(alien):
    """Oppdater en alien som dykker mot spilleren"""
    # Bruk Bezier-kurve for å lage en fin, buet dykkebane
    # t går fra 0 til 1, der 0 er start og 1 er slutt
    t = alien['dive_progress']
    
    # Kontrollpunkter for Bezier-kurven (start, kontroll, slutt)
    p0 = (alien['original_x'], alien['original_y'])
    # Kontrollpunkt over målet
    p1 = (alien['dive_target_x'], alien['original_y'] + (alien['dive_target_y'] - alien['original_y']) / 2 - 100)
    p2 = (alien['dive_target_x'], alien['dive_target_y'])
    
    # Kvadratisk Bezier-formel: B(t) = (1-t)^2*P0 + 2(1-t)t*P1 + t^2*P2
    x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
    y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
    
    # Oppdater alienens posisjon
    alien['rect'].x = x
    alien['rect'].y = y
    
    # Øk fremgangen
    alien['dive_progress'] += alien['dive_speed']
    
    # Hvis dykket er ferdig, gå tilbake til normal tilstand
    if alien['dive_progress'] >= 1.0:
        alien['diving'] = False
        alien['dive_progress'] = 0
        alien['rect'].x = alien['original_x']
        alien['rect'].y = alien['original_y']

def handle_alien_shooting(aliens, alien_bullets, shoot_sound, level_config):
    """Sjekker om aliens skal skyte og oppretter nye kuler."""
    # Sjekk maks antall kuler
    if len(alien_bullets) >= level_config.get('max_bullets', 3):
        return

    for alien in aliens:
        if alien['can_shoot'] and random.random() < level_config.get('shoot_chance', 0.01):
            # Opprett en ny kule
            bullet = pygame.Rect(
                alien['rect'].centerx - ALIEN_BULLET_WIDTH // 2,
                alien['rect'].bottom,
                ALIEN_BULLET_WIDTH,
                ALIEN_BULLET_HEIGHT
            )
            alien_bullets.append(bullet)
            
            # Spill av lydeffekt
            if shoot_sound:
                shoot_sound.play()
            
            # Bare én alien skyter om gangen
            break

def handle_alien_diving(aliens, player_x, player_y, level_config):
    """Håndter aliens som dykker mot spillerens posisjon"""
    if random.random() > 0.005 * level_config['dive_chance']:
        return  # Ikke prøv å dykke denne gangen
    
    # Finn aliens som kan dykke og ikke allerede dykker
    diving_candidates = [a for a in aliens if a['can_dive'] and not a['diving']]
    if not diving_candidates:
        return
    
    # Velg en tilfeldig alien
    alien = random.choice(diving_candidates)
    
    # Sett dykkemål til området rundt spilleren
    target_x = player_x + random.randint(-100, 100)
    target_y = player_y + random.randint(-20, 50)
    
    # Lagre original posisjon og sett dykkeparametre
    alien['original_x'] = alien['rect'].x
    alien['original_y'] = alien['rect'].y
    alien['dive_target_x'] = target_x
    alien['dive_target_y'] = target_y
    alien['diving'] = True
    alien['dive_progress'] = 0
    
    # Reduser dykkehastigheten til 30% av opprinnelig verdi
    alien['dive_speed'] = random.uniform(0.006, 0.015)  # Redusert fra 0.02-0.05

def check_collisions(player_x, player_y, bullets, alien_bullets, aliens, bonus_star, 
                    particles, explosion_sound, bonus_sound, bonus_text, current_score):
    """Sjekker kollisjoner mellom objekter."""
    player_hit = False
    score_delta = 0
    
    # Lag player rect for kollisjonsjekk
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    # Sjekk om aliens traff spilleren
    alien_hit_idx = -1
    for idx, alien in enumerate(aliens):
        if alien['rect'].colliderect(player_rect):
            alien_hit_idx = idx
            player_hit = True
            break
    
    # Fjern alien som traff spilleren og opprett partikler
    if alien_hit_idx >= 0:
        alien = aliens.pop(alien_hit_idx)
        create_explosion(alien['rect'].centerx, alien['rect'].centery, particles, NEON_RED)
        if explosion_sound:
            explosion_sound.play()
    
    # Sjekk kollisjon mellom spiller-kuler og aliens
    updated_score = check_bullet_alien_collisions(bullets, aliens, current_score, particles, bonus_star, bonus_text)
    score_delta = updated_score - current_score
    
    # Sjekk kollisjon mellom alien-kuler og spilleren
    if check_bullet_player_collision(alien_bullets, player_x, player_y):
        player_hit = True
    
    # Sjekk kollisjon mellom spiller og bonusstjerne
    if bonus_star.active:
        bonus_rect = pygame.Rect(bonus_star.x, bonus_star.y, bonus_star.size, bonus_star.size)
        if bonus_rect.colliderect(player_rect):
            bonus_star.active = False
            
            # Legg til poeng og vis bonustekst
            bonus_points = 100
            bonus_text.activate(
                bonus_star.rect.centerx, 
                bonus_star.rect.centery, 
                f"+{bonus_points}",
                bonus_points
            )
            score_delta += bonus_points
            
            # Opprett partikkeleffekt
            create_bonus_explosion(bonus_star.x, bonus_star.y, particles)
            
            # Spill av lydeffekt
            if bonus_sound:
                bonus_sound.play()
    
    return player_hit, score_delta

def create_explosion(x, y, particles, color, count=15, speed=3):
    """Create an explosion at the specified position"""
    for _ in range(count):
        # Lag tilfeldige hastigheter
        angle = random.uniform(0, 2 * math.pi)
        velocity = random.uniform(1, speed)
        vx = math.cos(angle) * velocity
        vy = math.sin(angle) * velocity
        
        # Lag tilfeldige størrelser og levetid
        size = random.randint(2, 5)
        lifetime = random.randint(20, 40)
        
        # Legg til partikkel
        particles.append(Particle(x, y, vx, vy, color, size, lifetime))
    return particles

def create_bonus_explosion(x, y, particles, color=(255, 215, 0), count=30, speed=4):
    """Create a larger explosion for bonus items"""
    for _ in range(count):
        # Lag tilfeldige hastigheter
        angle = random.uniform(0, 2 * math.pi)
        velocity = random.uniform(1, speed)
        vx = math.cos(angle) * velocity
        vy = math.sin(angle) * velocity
        
        # Lag tilfeldige størrelser og levetid
        size = random.randint(2, 6)
        lifetime = random.randint(30, 60)
        
        # Legg til partikkel
        particles.append(Particle(x, y, vx, vy, color, size, lifetime))
    return particles

def create_firework(x=None, y=None):
    """Create a firework particle starting from the bottom of the screen"""
    if x is None:
        x = random.randint(50, SCREEN_WIDTH - 50)
    if y is None:
        y = random.randint(50, SCREEN_HEIGHT // 2)
    
    return FireworkParticle(x, y)

def create_firework_explosion(x, y, color=None, count=30):
    """Create an explosion of particles at the specified position and color"""
    if color is None:
        # Random explosion color if not specified
        color = random.choice([
            (255, 50, 50),   # Red
            (50, 255, 50),   # Green
            (50, 50, 255),   # Blue
            (255, 255, 50),  # Yellow
            (255, 50, 255),  # Magenta
            (50, 255, 255)   # Cyan
        ])
    
    particles = []
    for _ in range(count):
        # Lag tilfeldige hastigheter
        angle = random.uniform(0, 2 * math.pi)
        velocity = random.uniform(1, 5)
        vx = math.cos(angle) * velocity
        vy = math.sin(angle) * velocity
        
        # Lag tilfeldige størrelser og levetid
        size = random.randint(1, 3)
        lifetime = random.randint(30, 60)
        
        # Legg til partikkel
        particles.append(Particle(x, y, vx, vy, color, size, lifetime))
    return particles

# Kollisjonsdeteksjon
def check_bullet_alien_collisions(bullets, aliens, score, particles, bonus_star, bonus_text):
    """Sjekker kollisjoner mellom spillerens kuler og aliens"""
    for bullet in bullets[:]:
        for alien in aliens[:]:
            if bullet.colliderect(alien['rect']):
                # Lag eksplosjon
                create_explosion(alien['rect'].centerx, alien['rect'].centery, particles, (255, 60, 60))
                
                if bullet in bullets:
                    bullets.remove(bullet)
                
                aliens.remove(alien)
                
                # Gi mer poeng for dykkende aliens
                score += 10 + (20 if alien['diving'] else 0)
    
    # Sjekk treff på bonusstjerne
    for bullet in bullets[:]:
        if bonus_star.active and bullet.colliderect(bonus_star.rect):
            create_bonus_explosion(bonus_star.rect.centerx, bonus_star.rect.centery, particles)
            bonus_points = 50  # Bonuspoeng for å treffe stjernen
            score += bonus_points
            bonus_text.activate(
                bonus_star.rect.centerx, 
                bonus_star.rect.centery, 
                f"+{bonus_points}",
                bonus_points
            )
            bonus_star.active = False
            if bullet in bullets:
                bullets.remove(bullet)
    
    return score

def check_bullet_player_collision(alien_bullets, player_x, player_y):
    """Sjekker om alien-kuler treffer spilleren"""
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    for bullet in alien_bullets[:]:
        if bullet.colliderect(player_rect):
            return True  # Spilleren er truffet
    
    return False  # Ingen treff 