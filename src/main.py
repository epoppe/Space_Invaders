import pygame
import random
import math
import json
import time
import sys
from datetime import datetime
from collections import deque

# Importer våre egne moduler
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT,
    WHITE, BLACK, GREEN, NEON_RED, YELLOW, BLUE,
    FPS, PLAYER_SPEED, BULLET_SPEED,
    STATE_MENU, STATE_PLAYING, STATE_GAME_OVER, STATE_NEW_HIGH_SCORE,
    STATE_HIGH_SCORE_INPUT, STATE_SHOW_HIGH_SCORES,
    ALIEN_TYPE_STANDARD, ALIEN_TYPE_SPEEDY, ALIEN_TYPE_TANK,
    BASE_ALIEN_SPEED
)
from src.utils import create_button, random_color
from src.managers import HighscoreManager, LevelConfigs
from src.entities import Star, BonusStar, BonusText, Particle, FireworkParticle
from src.sprites import create_alien_sprites, create_player_sprite
from src.game import (
    create_aliens, update_aliens, handle_alien_shooting, handle_alien_diving,
    check_collisions, create_explosion, create_firework_explosion, create_bonus_explosion
)
from src.renderer import (
    draw_game_elements, draw_game_over_screen, draw_high_score_celebration,
    draw_text_input_screen, draw_highscore_list, draw_level_message
)

def initialize_game():
    """Initialiserer spillet og returnerer alle spillobjekter"""
    # Initialiser Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Opprett spill-objekter
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    
    # Opprett sprite-bilder
    alien_sprites = create_alien_sprites(is_hd=True, max_rows=7)
    player_sprite = create_player_sprite(is_hd=True)
    
    # Last inn lydeffekter
    shoot_sound = None
    explosion_sound = None
    alien_shoot_sound = None
    bonus_sound = None
    
    try:
        shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
        alien_shoot_sound = pygame.mixer.Sound("assets/sounds/alien_shoot.wav")
        bonus_sound = pygame.mixer.Sound("assets/sounds/bonus.wav")
        
        # Juster lydvolum
        shoot_sound.set_volume(0.2)
        explosion_sound.set_volume(0.3)
        alien_shoot_sound.set_volume(0.2)
        bonus_sound.set_volume(0.4)
    except (FileNotFoundError, pygame.error) as e:
        print(f"Advarsel: Kunne ikke laste lydfilene: {e}")
        print("Spillet vil kjøre uten lyd.")
        shoot_sound = None
        explosion_sound = None
        alien_shoot_sound = None
        bonus_sound = None
    
    # Innstillinger for spiller
    player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
    player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
    player_speed = PLAYER_SPEED
    shoot_cooldown = 0
    shoot_cooldown_max = 20  # Frames mellom hvert skudd
    bullet_speed = BULLET_SPEED
    
    # Innstillinger for nivå
    current_level = 1
    current_wave = 1
    level_configs = LevelConfigs()
    level_config = level_configs.get_level(current_level, current_wave)
    
    # Innstillinger for aliens
    base_alien_speed = BASE_ALIEN_SPEED  # Fra constants.py
    alien_speed = base_alien_speed * level_config.get('speed_modifier', 1.0)  # Bruker speed_modifier fra level_config
    
    # Innstillinger for highscore
    highscore_manager = HighscoreManager()
    high_score = highscore_manager.get_highest_score()
    score = 0
    
    # Animasjonsvariabler
    animation_frame = 0
    animation_cooldown = 0
    
    # Opprett bakgrunnsstjerner
    NUM_STARS = 100
    stars = [Star() for _ in range(NUM_STARS)]
    
    # Opprett bonus-objekter
    bonus_star = BonusStar()
    bonus_text = BonusText()
    
    # Opprett spill-arrays
    bullets = []
    alien_bullets = []
    aliens = []
    particles = []
    fireworks = []
    explosion_particles = []
    
    # Opprett game over-elementer
    font = pygame.font.Font(None, 36)
    restart_button = create_button("Restart", WHITE, (100, 40))
    button_rect = restart_button.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
    
    # Opprett level-meldingselementer
    level_message_font = pygame.font.Font(None, 64)
    level_message = ""
    level_message_timer = 0
    level_message_duration = 120  # 2 sekunder med 60 FPS
    
    # Opprett high score-feiringselementer
    high_score_font = pygame.font.Font(None, 72)
    celebration_timer = 0
    celebration_duration = 180  # 3 sekunder med 60 FPS
    
    # Initialiser game state
    game_state = STATE_PLAYING
    
    # Game over-variabler
    flash_timer = 0
    flash_speed = 10  # Raskere blinking
    
    # High score-variabler
    initials = ""
    cursor_pos = 0
    
    # Initialiser alle spillobjekter
    game_objects = {
        # Overflater
        'screen': screen,
        'clock': clock,
        
        # Sprite-bilder
        'alien_sprites': alien_sprites,
        'player_sprite': player_sprite,
        
        # Lyder
        'shoot_sound': shoot_sound,
        'explosion_sound': explosion_sound,
        'alien_shoot_sound': alien_shoot_sound,
        'bonus_sound': bonus_sound,
        
        # Spiller-variabler
        'player_x': player_x,
        'player_y': player_y,
        'player_speed': player_speed,
        'bullet_speed': bullet_speed,
        'shoot_cooldown': shoot_cooldown,
        'shoot_cooldown_max': shoot_cooldown_max,
        
        # Alien-variabler
        'alien_speed': alien_speed,
        'animation_frame': animation_frame,
        'animation_cooldown': animation_cooldown,
        
        # Bakgrunnselementer
        'stars': stars,
        'bonus_star': bonus_star,
        'bonus_text': bonus_text,
        
        # Spill-arrays
        'bullets': bullets,
        'alien_bullets': alien_bullets,
        'aliens': aliens,
        'particles': particles,
        'fireworks': fireworks,
        'explosion_particles': explosion_particles,
        
        # Spillkontroll
        'score': score,
        'level_configs': level_configs,
        'current_level': current_level,
        'current_wave': current_wave,
        'high_score': high_score,
        'highscore_manager': highscore_manager,
        
        # UI-elementer
        'font': font,
        'restart_button': restart_button,
        'button_rect': button_rect,
        'level_message_font': level_message_font,
        'level_message': level_message,
        'level_message_timer': level_message_timer,
        'level_message_duration': level_message_duration,
        'high_score_font': high_score_font,
        'celebration_timer': celebration_timer,
        'celebration_duration': celebration_duration,
        
        # Spilltilstand
        'game_state': game_state,
        'flash_timer': flash_timer,
        'flash_speed': flash_speed,
        'initials': initials,
        'cursor_pos': cursor_pos
    }
    
    return game_objects

def reset_game(game_objects):
    """Tilbakestiller spillet til starttilstand"""
    # Tilbakestill spiller
    game_objects['player_x'] = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
    game_objects['player_y'] = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
    game_objects['shoot_cooldown'] = 0
    
    # Tøm alle arrays
    game_objects['bullets'].clear()
    game_objects['alien_bullets'].clear()
    game_objects['aliens'].clear()
    game_objects['particles'].clear()
    game_objects['fireworks'].clear()
    game_objects['explosion_particles'].clear()
    
    # Tilbakestill score og level
    game_objects['score'] = 0
    game_objects['current_level'] = 1
    game_objects['current_wave'] = 1
    
    # Opprett aliens for første level
    level_config = game_objects['level_configs'].get_level(
        game_objects['current_level'], game_objects['current_wave']
    )
    game_objects['aliens'] = create_aliens(level_config)
    
    # Oppdater alien_speed basert på level_config
    game_objects['alien_speed'] = BASE_ALIEN_SPEED * level_config.get('speed_modifier', 1.0)
    
    # Tilbakestill bonusobjekter
    game_objects['bonus_star'].active = False
    game_objects['bonus_text'].active = False
    
    # Vis level-melding
    game_objects['level_message'] = f"LEVEL {game_objects['current_level']}"
    game_objects['level_message_timer'] = game_objects['level_message_duration']
    
    # Sett spilltilstand til playing
    game_objects['game_state'] = STATE_PLAYING

def handle_input_events(game_objects):
    """Håndterer inndata-hendelser basert på spilltilstand"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Håndter taster basert på spilltilstand
        if event.type == pygame.KEYDOWN:
            # Avslutt spillet med Escape uansett tilstand
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            # Hopp til spesifikt level med Ctrl + tall
            if event.mod & pygame.KMOD_CTRL:
                # Sjekk for talltaster (1-9)
                if pygame.K_1 <= event.key <= pygame.K_9:
                    requested_level = event.key - pygame.K_0  # Konverter keykode til faktisk tall
                    
                    # Hopp kun til nivå hvis vi er i spilltilstand
                    if game_objects['game_state'] == STATE_PLAYING:
                        # Maksimalt nivå er 7 i vår implementasjon
                        if requested_level <= 7:
                            # Oppdater level og reset aliens, men behold poeng
                            game_objects['current_level'] = requested_level
                            game_objects['current_wave'] = 1
                            
                            # Hent level-konfigurasjon
                            level_config = game_objects['level_configs'].get_level(
                                game_objects['current_level'], game_objects['current_wave']
                            )
                            
                            # Opprett nye aliens for nivået
                            game_objects['aliens'] = create_aliens(level_config)
                            
                            # Vis level-beskjed
                            game_objects['level_message'] = f"Level {game_objects['current_level']}: {level_config['name']}"
                            game_objects['level_message_timer'] = game_objects['level_message_duration']
                            
                            print(f"Hoppet til nivå {requested_level}: {level_config['name']}")
            
            # Håndter input basert på spilltilstand
            if game_objects['game_state'] == STATE_PLAYING:
                # Ingen spesielle nøkkelhendelser for playing-tilstand
                pass
                
            elif game_objects['game_state'] == STATE_GAME_OVER:
                # Start nytt spill ved Enter
                if event.key == pygame.K_RETURN:
                    reset_game(game_objects)
                    
            elif game_objects['game_state'] == STATE_HIGH_SCORE_INPUT:
                # Håndter navneinntasting for high score
                if event.key == pygame.K_RETURN:
                    # Lagre score og vis highscore-listen
                    if len(game_objects['initials']) == 3:
                        game_objects['highscore_manager'].add_score({
                            'initials': game_objects['initials'],
                            'score': game_objects['score'],
                            'date': datetime.now().strftime("%Y-%m-%d")
                        })
                        game_objects['game_state'] = STATE_SHOW_HIGH_SCORES
                
                elif event.key == pygame.K_BACKSPACE:
                    # Slett bokstav
                    if game_objects['cursor_pos'] > 0:
                        game_objects['cursor_pos'] -= 1
                        if game_objects['cursor_pos'] < len(game_objects['initials']):
                            game_objects['initials'] = game_objects['initials'][:game_objects['cursor_pos']] + game_objects['initials'][game_objects['cursor_pos']+1:]
                
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    # Flytt markør
                    direction = -1 if event.key == pygame.K_LEFT else 1
                    game_objects['cursor_pos'] = max(0, min(game_objects['cursor_pos'] + direction, 3 - 1))
                
                elif event.unicode.isalpha() and len(game_objects['initials']) < 3:
                    # Legg til bokstav (kun store bokstaver)
                    letter = event.unicode.upper()
                    if game_objects['cursor_pos'] >= len(game_objects['initials']):
                        game_objects['initials'] += letter
                    else:
                        game_objects['initials'] = game_objects['initials'][:game_objects['cursor_pos']] + letter + game_objects['initials'][game_objects['cursor_pos']:]
                    game_objects['cursor_pos'] = min(game_objects['cursor_pos'] + 1, 3)
            
            elif game_objects['game_state'] == STATE_SHOW_HIGH_SCORES:
                # Start nytt spill ved Enter
                if event.key == pygame.K_RETURN:
                    reset_game(game_objects)
            
            elif game_objects['game_state'] == STATE_NEW_HIGH_SCORE:
                # Gå til innmatingstilstand etter high score-feiring
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Sett initialer til tom streng og nullstill markørposisjon
                    game_objects['initials'] = ""
                    game_objects['cursor_pos'] = 0
                    game_objects['game_state'] = STATE_HIGH_SCORE_INPUT
        
        # Håndter museklikk
        if event.type == pygame.MOUSEBUTTONDOWN and game_objects['game_state'] == STATE_GAME_OVER:
            # Sjekk om restart-knappen ble klikket
            if game_objects['button_rect'].collidepoint(event.pos):
                reset_game(game_objects)

def update_game_state(game_objects):
    """Oppdaterer spilltilstanden basert på nåværende tilstand"""
    if game_objects['game_state'] == STATE_PLAYING:
        update_playing_state(game_objects)
    elif game_objects['game_state'] == STATE_GAME_OVER:
        update_game_over_state(game_objects)
    elif game_objects['game_state'] == STATE_NEW_HIGH_SCORE:
        update_high_score_celebration(game_objects)
    # STATE_HIGH_SCORE_INPUT og STATE_SHOW_HIGH_SCORES håndteres kun med rendering og input

def update_playing_state(game_objects):
    """Oppdaterer spillet i spilltilstanden"""
    # Oppdater spillerposisjon
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        game_objects['player_x'] = max(0, game_objects['player_x'] - game_objects['player_speed'])
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        game_objects['player_x'] = min(SCREEN_WIDTH - 64, game_objects['player_x'] + game_objects['player_speed'])
    
    # Håndter skyting
    if game_objects['shoot_cooldown'] > 0:
        game_objects['shoot_cooldown'] -= 1
    
    if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and game_objects['shoot_cooldown'] == 0:
        # Opprett ny kule
        bullet = pygame.Rect(
            game_objects['player_x'] + 28,  # Sentrer kulen på spilleren
            game_objects['player_y'] - 10,  # Start kulen foran spilleren
            8, 20  # Størrelse på kulen
        )
        game_objects['bullets'].append(bullet)
        if game_objects['shoot_sound']:
            game_objects['shoot_sound'].play()
        game_objects['shoot_cooldown'] = game_objects['shoot_cooldown_max']
    
    # Oppdater kuler
    for bullet in game_objects['bullets'][:]:
        bullet.y -= game_objects['bullet_speed']
        if bullet.y < 0:
            game_objects['bullets'].remove(bullet)
    
    # Oppdater alien-kuler
    for bullet in game_objects['alien_bullets'][:]:
        bullet.y += game_objects['bullet_speed'] * 0.5  # Alien-kuler er mye langsommere (endret fra 0.7)
        if bullet.y > SCREEN_HEIGHT:
            game_objects['alien_bullets'].remove(bullet)
    
    # Oppdater aliens
    game_objects['animation_cooldown'] += 1
    animation_speed = max(10, int(20 - game_objects['alien_speed'] * 5))  # Raskere aliens = raskere animasjon
    if game_objects['animation_cooldown'] >= animation_speed:
        game_objects['animation_frame'] = 1 - game_objects['animation_frame']  # Bytt mellom 0 og 1
        game_objects['animation_cooldown'] = 0
    
    # Få level-konfigurasjon for denne bølgen
    level_config = game_objects['level_configs'].get_level(
        game_objects['current_level'], game_objects['current_wave']
    )
    
    # Oppdater aliens med aktuelle konfigurasjoner
    update_aliens(
        game_objects['aliens'], 
        game_objects['alien_speed'], 
        level_config
    )
    
    # Håndter alien skyting
    handle_alien_shooting(
        game_objects['aliens'],
        game_objects['alien_bullets'],
        game_objects['alien_shoot_sound'],
        level_config
    )
    
    # Håndter alien dykking
    handle_alien_diving(
        game_objects['aliens'],
        game_objects['player_x'],
        game_objects['player_y'],
        level_config
    )
    
    # Sjekk kollisjoner
    player_hit, score_delta = check_collisions(
        game_objects['player_x'],
        game_objects['player_y'],
        game_objects['bullets'],
        game_objects['alien_bullets'],
        game_objects['aliens'],
        game_objects['bonus_star'],
        game_objects['particles'],
        game_objects['explosion_sound'],
        game_objects['bonus_sound'],
        game_objects['bonus_text'],
        game_objects['score']
    )
    
    # Oppdater score hvis endret
    if score_delta > 0:
        game_objects['score'] += score_delta
        
        # Sjekk om vi har ny high score
        if game_objects['score'] > game_objects['high_score']:
            game_objects['high_score'] = game_objects['score']
    
    # Sjekk om spilleren ble truffet
    if player_hit:
        # Game over
        game_objects['game_state'] = STATE_GAME_OVER
        
        # Lag eksplosjon der spilleren var
        create_explosion(
            game_objects['player_x'] + 32,
            game_objects['player_y'] + 32,
            game_objects['particles'],
            (255, 200, 100)
        )
        
        # Sjekk om vi har en ny high score
        if game_objects['score'] > 0:
            try:
                lowest_score = game_objects['highscore_manager'].get_lowest_high_score_entry()['score']
                if game_objects['score'] > lowest_score:
                    game_objects['game_state'] = STATE_NEW_HIGH_SCORE
                    # Opprett fyrverkeri for high score feiring
                    for _ in range(5):
                        rocket = FireworkParticle(
                            random.randint(100, SCREEN_WIDTH - 100),
                            SCREEN_HEIGHT + 10,
                            random.randint(-3, 3),
                            random.randint(-15, -10),
                            random_color()
                        )
                        game_objects['fireworks'].append(rocket)
                    game_objects['celebration_timer'] = game_objects['celebration_duration']
            except (AttributeError, IndexError, KeyError):
                # Hvis metoden ikke finnes eller det ikke er noen highscores ennå
                if game_objects['highscore_manager'].is_high_score(game_objects['score']):
                    game_objects['game_state'] = STATE_NEW_HIGH_SCORE
                    # Opprett fyrverkeri for high score feiring
                    for _ in range(5):
                        rocket = FireworkParticle(
                            random.randint(100, SCREEN_WIDTH - 100),
                            SCREEN_HEIGHT + 10,
                            random.randint(-3, 3),
                            random.randint(-15, -10),
                            random_color()
                        )
                        game_objects['fireworks'].append(rocket)
                    game_objects['celebration_timer'] = game_objects['celebration_duration']
    
    # Sjekk om alle aliens er drept
    if len(game_objects['aliens']) == 0:
        # Øk wave eller level
        game_objects['current_wave'] += 1
        if game_objects['current_wave'] > 3:  # 3 bølger per level
            game_objects['current_wave'] = 1
            game_objects['current_level'] += 1
            game_objects['level_message'] = f"LEVEL {game_objects['current_level']}"
        else:
            game_objects['level_message'] = f"LEVEL {game_objects['current_level']} - WAVE {game_objects['current_wave']}"
        
        # Vis level/wave-melding
        game_objects['level_message_timer'] = game_objects['level_message_duration']
        
        # Få level-konfigurasjon for neste bølge
        level_config = game_objects['level_configs'].get_level(
            game_objects['current_level'], game_objects['current_wave']
        )
        
        # Opprett aliens for neste level/wave
        game_objects['aliens'] = create_aliens(level_config)
        
        # Oppdater alien_speed basert på level_config
        game_objects['alien_speed'] = BASE_ALIEN_SPEED * level_config.get('speed_modifier', 1.0)
    
    # Oppdater stjerner
    for star in game_objects['stars']:
        star.update()
    
    # Oppdater partikler
    for particle in game_objects['particles'][:]:
        particle.update()
        if particle.lifetime <= 0:
            game_objects['particles'].remove(particle)
    
    # Oppdater bonusstjerne
    game_objects['bonus_star'].update()
    
    # Oppdater bonustekst
    game_objects['bonus_text'].update()
    
    # Oppdater level-meldingstimer
    if game_objects['level_message_timer'] > 0:
        game_objects['level_message_timer'] -= 1

def update_game_over_state(game_objects):
    """Oppdaterer spillobjekter i game over-tilstanden"""
    # Oppdater stjerner
    for star in game_objects['stars']:
        star.update()
    
    # Oppdater partikler (eksplosjon fra spilleren)
    for particle in game_objects['particles'][:]:
        particle.update()
        if particle.lifetime <= 0:
            game_objects['particles'].remove(particle)
    
    # Oppdater blinkende bakgrunn
    game_objects['flash_timer'] = (game_objects['flash_timer'] + 1) % (game_objects['flash_speed'] * 2)

def update_high_score_celebration(game_objects):
    """Oppdaterer high score-feiring"""
    # Oppdater stjerner
    for star in game_objects['stars']:
        star.update()
    
    # Oppdater fyrverkeri
    for fw in game_objects['fireworks'][:]:
        fw.update()
        
        # Når fyrverkeri når toppen, lag eksplosjon
        if fw.vy > -2 and not fw.exploded:
            fw.exploded = True
            explosion = create_firework_explosion(fw.x, fw.y, fw.color)
            game_objects['explosion_particles'].extend(explosion)
    
    # Fjern fyrverkeri som er ferdig
    game_objects['fireworks'] = [fw for fw in game_objects['fireworks'] if not (fw.exploded and fw.y > SCREEN_HEIGHT)]
    
    # Oppdater eksplosjon-partikler
    for ep in game_objects['explosion_particles'][:]:
        ep.update()
        if ep.lifetime <= 0:
            game_objects['explosion_particles'].remove(ep)
    
    # Countdown celebration timer
    game_objects['celebration_timer'] -= 1
    if game_objects['celebration_timer'] <= 0 and not game_objects['fireworks'] and not game_objects['explosion_particles']:
        # Gå til high score-inntastingstilstand
        game_objects['initials'] = ""
        game_objects['cursor_pos'] = 0
        game_objects['game_state'] = STATE_HIGH_SCORE_INPUT
    
    # Lag nytt fyrverkeri med jevne mellomrom
    if random.random() < 0.03 and len(game_objects['fireworks']) < 3:
        rocket = FireworkParticle(
            random.randint(100, SCREEN_WIDTH - 100),
            SCREEN_HEIGHT + 10,
            random.randint(-3, 3),
            random.randint(-15, -10),
            random_color()
        )
        game_objects['fireworks'].append(rocket)

def render_game(game_objects):
    """Rendrer spillet basert på nåværende spilltilstand"""
    if game_objects['game_state'] == STATE_PLAYING:
        # Tegn alle spillelementer
        draw_game_elements(
            game_objects['screen'],
            game_objects['stars'],
            game_objects['player_x'],
            game_objects['player_y'],
            game_objects['bullets'],
            game_objects['alien_bullets'],
            game_objects['aliens'],
            game_objects['animation_frame'],
            game_objects['particles'],
            game_objects['score'],
            game_objects['high_score'],
            game_objects['current_level'],
            game_objects['current_wave'],
            game_objects['bonus_star'],
            game_objects['bonus_text'],
            game_objects['alien_sprites'],
            game_objects['player_sprite']
        )
        
        # Tegn level-melding hvis aktiv
        draw_level_message(
            game_objects['screen'],
            game_objects['level_message'],
            game_objects['level_message_timer'],
            game_objects['level_message_duration'],
            game_objects['level_message_font']
        )
        
    elif game_objects['game_state'] == STATE_GAME_OVER:
        # Rendrer game over-skjermen med blinkende effekt
        game_objects['flash_timer'] = draw_game_over_screen(
            game_objects['screen'],
            game_objects['score'],
            game_objects['high_score'],
            game_objects['restart_button'],
            game_objects['button_rect'],
            game_objects['flash_timer'],
            game_objects['flash_speed'],
            game_objects['font']
        )
        
        # Tegn partikler (spillerens eksplosjon)
        for particle in game_objects['particles']:
            particle.draw(game_objects['screen'])
            
    elif game_objects['game_state'] == STATE_NEW_HIGH_SCORE:
        # Rendrer high score-feiringen
        game_objects['screen'].fill(BLACK)
        
        # Tegn stjerner i bakgrunnen
        for star in game_objects['stars']:
            star.draw(game_objects['screen'])
        
        # Tegn high score-feiring
        draw_high_score_celebration(
            game_objects['screen'],
            game_objects['celebration_timer'],
            game_objects['fireworks'],
            game_objects['explosion_particles'],
            game_objects['high_score_font']
        )
        
        # Tegn instruksjoner
        instruction_font = pygame.font.Font(None, 36)
        instruction_text = instruction_font.render("Trykk Enter for å fortsette", True, WHITE)
        game_objects['screen'].blit(
            instruction_text,
            (SCREEN_WIDTH//2 - instruction_text.get_width()//2, SCREEN_HEIGHT - 100)
        )
        
    elif game_objects['game_state'] == STATE_HIGH_SCORE_INPUT:
        # Rendrer input-skjermen for initialer
        draw_text_input_screen(
            game_objects['screen'],
            game_objects['initials'],
            game_objects['cursor_pos']
        )
        
    elif game_objects['game_state'] == STATE_SHOW_HIGH_SCORES:
        # Rendrer high score-listen
        draw_highscore_list(
            game_objects['screen'],
            game_objects['highscore_manager']
        )
    
    # Oppdater skjermen
    pygame.display.flip()

def main():
    """Hovedfunksjonen som starter og kjører spillet"""
    # Initialiser spillet
    game_objects = initialize_game()
    
    # Opprett stjerner
    game_objects['stars'] = [Star() for _ in range(100)]
    
    # Opprett aliens for første level
    level_config = game_objects['level_configs'].get_level(
        game_objects['current_level'], game_objects['current_wave']
    )
    game_objects['aliens'] = create_aliens(level_config)
    
    # Vis velkomstmelding
    game_objects['level_message'] = f"LEVEL {game_objects['current_level']}"
    game_objects['level_message_timer'] = game_objects['level_message_duration']
    
    # Spill-loop
    while True:
        # Håndter input
        handle_input_events(game_objects)
        
        # Oppdater spilltilstand
        update_game_state(game_objects)
        
        # Rendrer spillet
        render_game(game_objects)
        
        # Kontroller framerate
        game_objects['clock'].tick(FPS)

if __name__ == "__main__":
    main() 