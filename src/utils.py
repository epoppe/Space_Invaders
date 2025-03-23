import pygame
import random
import math
from src.constants import WHITE

# Hjelpefunksjoner for fargemanipulasjon
def lighten_color(color, amount=50):
    r, g, b = color[:3]
    r = min(255, r + amount)
    g = min(255, g + amount)
    b = min(255, b + amount)
    return (r, g, b) if len(color) == 3 else (r, g, b, color[3])

def darken_color(color, amount=50):
    r, g, b = color[:3]
    r = max(0, r - amount)
    g = max(0, g - amount)
    b = max(0, b - amount)
    return (r, g, b) if len(color) == 3 else (r, g, b, color[3])

# Hjelpefunksjon for å tegne avrundede rektangler
def draw_rounded_rect(surface, rect, color, radius=3):
    """Tegn en avrundet rektangel på surface."""
    if radius == 0:
        pygame.draw.rect(surface, color, rect)
        return
    
    # Begrens radius til halvparten av mindre dimensjon
    radius = min(radius, rect.height//2, rect.width//2)
    
    # Tegn hovedrektangel
    pygame.draw.rect(surface, color, rect.inflate(-radius*2, 0))
    pygame.draw.rect(surface, color, rect.inflate(0, -radius*2))
    
    # Tegn hjørnene
    pygame.draw.circle(surface, color, (rect.left + radius, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.right - radius, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.left + radius, rect.bottom - radius), radius)
    pygame.draw.circle(surface, color, (rect.right - radius, rect.bottom - radius), radius)

# Funksjon for å lage sprites
def create_sprite(pixel_array, color, scale=3):
    width = len(pixel_array[0]) * scale
    height = len(pixel_array) * scale
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for y, row in enumerate(pixel_array):
        for x, pixel in enumerate(row):
            if pixel != ' ':
                pygame.draw.rect(surface, color,
                               (x * scale, y * scale, scale, scale))
    return surface

# Funksjon for å lage mer detaljerte sprites med anti-aliasing (glatting)
def create_hd_sprite(pixel_array, color, scale=3):
    # Beregner målstørrelsen basert på originalfigurene
    base_width = len(pixel_array[0])
    base_height = len(pixel_array)
    target_width = base_width * scale
    target_height = base_height * scale
    
    # Beregn indre skaleringsfaktor for høyere oppløsning innenfor samme dimensjoner
    inner_scale_x = target_width / base_width
    inner_scale_y = target_height / base_height
    inner_scale = min(inner_scale_x, inner_scale_y)
    
    # Lag en overflate med samme størrelse som standard figurer
    surface = pygame.Surface((target_width, target_height), pygame.SRCALPHA)
    
    # Beregn sentrering for å holde figuren i midten
    offset_x = (target_width - base_width * inner_scale) / 2
    offset_y = (target_height - base_height * inner_scale) / 2
    
    # Tegn pikslene med glatting
    for y, row in enumerate(pixel_array):
        for x, pixel in enumerate(row):
            if pixel != ' ':
                # Bestem pikselfarge basert på tegn for mer detaljerte sprites
                pixel_color = color
                if pixel == '▄' or pixel == '▀':
                    # Lysere variant for høylys
                    pixel_color = lighten_color(color, 30)
                elif pixel == '█':
                    # Standard farge for hovedfylling
                    pixel_color = color
                elif pixel == '▓':
                    # Mørkere variant for skygge
                    pixel_color = darken_color(color, 30)
                elif pixel == '▒':
                    # Semi-transparent for glatting
                    pixel_color = (*color[:3], 180)  # Redusert alfa
                
                # Beregn pikselposisjon med høyere oppløsning men innenfor samme størrelse
                pixel_rect = pygame.Rect(
                    offset_x + x * inner_scale, 
                    offset_y + y * inner_scale, 
                    inner_scale, 
                    inner_scale
                )
                
                if pixel in ['▄', '▀', '▓', '▒']:
                    # Vanlig rektangel for kantpiksler
                    pygame.draw.rect(surface, pixel_color, pixel_rect)
                else:
                    # Avrundet rektangel for hoveddeler av spriten
                    draw_rounded_rect(surface, pixel_rect, pixel_color, min(inner_scale/4, 1))
    
    return surface

def random_color():
    """Genererer en tilfeldig lyssterk farge"""
    # Sørger for at minst én komponent er høy for å få lyse farger
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    
    # Gjør en av komponentene veldig høy
    bright_component = random.randint(0, 2)
    if bright_component == 0:
        r = 255
    elif bright_component == 1:
        g = 255
    else:
        b = 255
    
    return (r, g, b)

def create_button(text, color, size=(200, 50)):
    """Oppretter en knapp-overflate med tekst"""
    # Opprett en overflate med riktig størrelse
    button_surface = pygame.Surface(size)
    
    # Fyll overflaten med en mørkere farge
    button_surface.fill((50, 50, 50))
    
    # Tegn en ramme rundt knappen
    pygame.draw.rect(button_surface, color, button_surface.get_rect(), 2)
    
    # Opprett tekst
    font = pygame.font.Font(None, 28)
    text_surface = font.render(text, True, color)
    
    # Sentrer teksten på knappen
    text_rect = text_surface.get_rect(center=(size[0]/2, size[1]/2))
    button_surface.blit(text_surface, text_rect)
    
    return button_surface

def interpolate_color(color1, color2, fraction):
    """Interpolerer mellom to farger med en gitt brøk (0.0 til 1.0)"""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    r = int(r1 + (r2 - r1) * fraction)
    g = int(g1 + (g2 - g1) * fraction)
    b = int(b1 + (b2 - b1) * fraction)
    
    return (r, g, b)

def draw_hd_alien_shape(surface, alien_type, color, size, frame=0):
    """
    Tegner en HD alien-sprite på overflaten basert på gitt type, farge og størrelse.
    Støtter nå animasjonsrammer - frame 0 eller 1.
    Designet for å ligne på de klassiske Space Invaders-alienene, men mer finkornede og skumlere.
    """
    target_width, target_height = size
    
    # Aliens med mer detaljerte og fylte design
    if alien_type == 0:  # Standard alien (grønn) - skummel "squid"
        if frame == 0:
            pixel_art = [
                '     ██     ',
                '    ████    ',
                '   ██████   ',
                '  ████████  ',
                ' ██████████ ',
                '████████████',
                '██ ██████ ██',
                '█████  █████',
                '███ ████ ███',
                ' ██      ██ '
            ]
        else:
            pixel_art = [
                '     ██     ',
                '    ████    ',
                '   ██████   ',
                '  ████████  ',
                ' ██████████ ',
                '████████████',
                '██ ██████ ██',
                '███ █████ ██',
                '██ ██  ██ ██',
                '█ ██    ██ █'
            ]
    elif alien_type == 1:  # Speedy alien (cyan) - skummel "crab"
        if frame == 0:
            pixel_art = [
                '  ██    ██  ',
                '   ██████   ',
                '  ████████  ',
                ' ██ ████ ██ ',
                '████████████',
                '████████████',
                '███ ████ ███',
                '██ ██████ ██',
                '██ ██  ██ ██',
                '  ██    ██  '
            ]
        else:
            pixel_art = [
                ' ██      ██ ',
                '  ████████  ',
                '  ████████  ',
                ' ██ ████ ██ ',
                '████████████',
                '████████████',
                '███ ████ ███',
                '██ ██████ ██',
                '██ ██  ██ ██',
                ' ██      ██ '
            ]
    else:  # Tank alien (rød) - skummel "octopus"
        if frame == 0:
            pixel_art = [
                '    ████    ',
                '   ██████   ',
                '  ████████  ',
                ' ██████████ ',
                '████████████',
                '████████████',
                '████████████',
                '███ ████ ███',
                '██ ██████ ██',
                '█ ██    ██ █'
            ]
        else:
            pixel_art = [
                '    ████    ',
                '   ██████   ',
                '  ████████  ',
                ' ██████████ ',
                '████████████',
                '████████████',
                '████████████',
                '███ ████ ███',
                '██ ██████ ██',
                '█ ███  ███ █'
            ]
    
    # Bruk create_hd_sprite for å tegne alien-spriten med lavere skala
    sprite = create_hd_sprite(pixel_art, color, scale=1.5)  # Redusert fra 3 til 1.5
    
    # Kopier spriten til overflaten
    # Først, beregn hvor spriten skal plasseres for å være sentrert
    pos_x = (target_width - sprite.get_width()) // 2
    pos_y = (target_height - sprite.get_height()) // 2
    
    # Blit sprite til overflaten
    surface.blit(sprite, (pos_x, pos_y))

def draw_hd_player_shape(surface, color, size):
    """Tegner en mer detaljert spiller på den gitte overflaten"""
    width, height = size
    
    # Beregn en mindre region for å tegne figuren i
    scale_factor = 0.4  # Samme faktor som brukes for aliens (redusert fra 0.65 til 0.4)
    draw_width = width * scale_factor
    draw_height = height * scale_factor
    
    # Beregn offset for sentrering
    offset_x = (width - draw_width) / 2
    offset_y = (height - draw_height) / 2
    
    # Skroget
    pygame.draw.rect(surface, color, 
                    (offset_x + draw_width//4, 
                     offset_y + draw_height*2//3, 
                     draw_width//2, 
                     draw_height//3))
    pygame.draw.rect(surface, color, 
                    (offset_x + draw_width*3//8, 
                     offset_y + draw_height//2, 
                     draw_width//4, 
                     draw_height//4))
    
    # Kanon
    pygame.draw.rect(surface, color, 
                    (offset_x + draw_width*7//16, 
                     offset_y + draw_height//4, 
                     draw_width//8, 
                     draw_height//4))
    
    # Detaljer
    detail_color = interpolate_color(color, (255, 255, 255), 0.3)
    
    # Cockpit
    pygame.draw.ellipse(surface, detail_color, 
                       (offset_x + draw_width*3//8, 
                        offset_y + draw_height//2, 
                        draw_width//4, 
                        draw_height//8))
    
    # Motorer
    engine_color = (255, 100, 0)
    pygame.draw.rect(surface, engine_color, 
                    (offset_x + draw_width*5//16, 
                     offset_y + draw_height*7//8, 
                     draw_width//8, 
                     draw_height//16))
    pygame.draw.rect(surface, engine_color, 
                    (offset_x + draw_width*9//16, 
                     offset_y + draw_height*7//8, 
                     draw_width//8, 
                     draw_height//16))
    
    # Thruster-effekt
    flame_colors = [(255, 200, 0), (255, 150, 0), (255, 100, 0)]
    for i, flame_color in enumerate(flame_colors):
        flame_height = draw_height//12 * (3 - i)
        flame_width = draw_width//10 * (3 - i)
        
        # Venstre motor
        flame_rect1 = pygame.Rect(
            offset_x + draw_width*5//16 + draw_width//16 - flame_width//2, 
            offset_y + draw_height - flame_height,
            flame_width, 
            flame_height
        )
        pygame.draw.ellipse(surface, flame_color, flame_rect1)
        
        # Høyre motor
        flame_rect2 = pygame.Rect(
            offset_x + draw_width*9//16 + draw_width//16 - flame_width//2, 
            offset_y + draw_height - flame_height,
            flame_width, 
            flame_height
        )
        pygame.draw.ellipse(surface, flame_color, flame_rect2) 