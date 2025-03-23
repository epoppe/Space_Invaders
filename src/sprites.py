import pygame
from src.utils import draw_hd_alien_shape, draw_hd_player_shape
from src.constants import ALIEN_WIDTH, ALIEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, GREEN, NEON_RED

def create_alien_sprites(is_hd=True, max_rows=7):
    """Oppretter alien sprites for alle typer, rader og animasjonsframes"""
    sprites = {}
    
    # Basisfarger for alien-typene
    base_colors = [
        (20, 255, 60),    # Type 0: Kraftigere grønn
        (20, 210, 255),   # Type 1: Kraftigere cyan
        (255, 70, 70)     # Type 2: Kraftigere rød
    ]
    
    # Farger for de ulike radene - gjort kraftigere og mer neon-aktige
    row_colors = [
        (50, 255, 70),      # Neon grønn
        (30, 220, 255),     # Kraftig cyan
        (255, 70, 80),      # Kraftig rød
        (255, 255, 50),     # Kraftig gul
        (255, 70, 255),     # Neon magenta
        (50, 255, 255),     # Neon turkis
        (255, 175, 30)      # Kraftig oransje
    ]
    
    for alien_type in range(3):
        sprites[alien_type] = {}
        
        # For hver rad
        for row in range(max_rows):
            # Velg en farge basert på rad
            color = row_colors[row % len(row_colors)]
            
            # Opprett frames for denne alien-typen og raden
            frames = []
            
            for frame in range(2):
                # Opprett en tom overflate med transparens
                sprite = pygame.Surface((ALIEN_WIDTH, ALIEN_HEIGHT), pygame.SRCALPHA)
                
                if is_hd:
                    # HD sprite med detaljert grafikk
                    draw_hd_alien_shape(sprite, alien_type, color, (ALIEN_WIDTH, ALIEN_HEIGHT), frame)
                else:
                    # Enkel firkant for testing
                    padding = 4 if frame == 0 else 8
                    pygame.draw.rect(
                        sprite, 
                        color, 
                        (padding, padding, ALIEN_WIDTH - padding*2, ALIEN_HEIGHT - padding*2)
                    )
                
                frames.append(sprite)
            
            sprites[alien_type][row] = frames
    
    return sprites

def create_player_sprite(is_hd=True):
    """Oppretter player sprite"""
    # Opprett en tom overflate med transparens
    sprite = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
    
    if is_hd:
        # HD sprite med detaljert grafikk
        draw_hd_player_shape(sprite, GREEN, (PLAYER_WIDTH, PLAYER_HEIGHT))
    else:
        # Enkel trekant for testing
        pygame.draw.polygon(
            sprite, 
            GREEN, 
            [
                (PLAYER_WIDTH // 2, 0),                # Topp
                (0, PLAYER_HEIGHT),                    # Nederst til venstre
                (PLAYER_WIDTH, PLAYER_HEIGHT)          # Nederst til høyre
            ]
        )
    
    return sprite

def create_particle_effect(size, color=(255, 200, 100)):
    """Oppretter en partikkel-effekt overflate"""
    # Opprett en tom overflate med transparens
    sprite = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
    
    # Tegn en fylt sirkel for partikkelen
    pygame.draw.circle(sprite, color, (size, size), size)
    
    # Tegn en glødende effekt (lys i midten, mørkere ytterst)
    inner_color = list(color)
    for i in range(3):
        inner_color[i] = min(255, inner_color[i] + 50)  # Gjør sentrumet lysere
    
    pygame.draw.circle(sprite, inner_color, (size, size), size // 2)
    
    return sprite 