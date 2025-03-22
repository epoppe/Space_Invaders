import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Retro Space Invaders')

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 128)  # Brighter neon green
PURPLE = (180, 0, 255)  # Brighter purple
CYAN = (0, 255, 255)  # Bright cyan
NEON_RED = (255, 60, 60)  # Bright red
WHITE = (255, 255, 255)

# Sprite designs in pixel art style (using ASCII for visualization)
PLAYER_PIXELS = [
    "    ▲    ",
    "   ███   ",
    "  █████  ",
    " ███████ ",
    "█████████",
    " █ █ █ █ "
]

# First frame of animation
ALIEN1_PIXELS_FRAME1 = [
    "  ▄██▄  ",
    " ██████ ",
    "██ ██ ██",
    "████████",
    " █ ██ █ ",
    "█ █  █ █"
]

# Second frame of animation
ALIEN1_PIXELS_FRAME2 = [
    "  ▄██▄  ",
    " ██████ ",
    "██ ██ ██",
    "████████",
    "█ █  █ █",
    " █ ██ █ "
]

ALIEN2_PIXELS_FRAME1 = [
    " ╔════╗ ",
    "╔══██══╗",
    "║██████║",
    "╚══██══╝",
    "  ╚══╝  ",
    " ▀    ▀ "
]

ALIEN2_PIXELS_FRAME2 = [
    " ╔════╗ ",
    "╔══██══╗",
    "║██████║",
    "╚══██══╝",
    " ▀    ▀ ",
    "  ╚══╝  "
]

ALIEN3_PIXELS_FRAME1 = [
    "▄  ██  ▄",
    "███████",
    "██▄██▄██",
    "███████",
    " ▀ ██ ▀ ",
    "  ▀  ▀  "
]

ALIEN3_PIXELS_FRAME2 = [
    "▄  ██  ▄",
    "███████",
    "██▄██▄██",
    "███████",
    "  ▀  ▀  ",
    " ▀ ██ ▀ "
]

STAR_PIXELS = [
    "    ★    ",
    "  ★ ⭐ ★  ",
    "★⭐★★★⭐★",
    "  ★ ⭐ ★  ",
    "    ★    "
]

# Ny funksjon for å lage mer detaljerte sprites med anti-aliasing (glatting)
def create_hd_sprite(pixel_array, color, scale=3):
    # Beregner målstørrelsen basert på originalfigurene
    base_width = len(pixel_array[0])
    base_height = len(pixel_array)
    target_width = len(PLAYER_PIXELS[0]) * scale  # Bruk same bredde som standard figurer
    target_height = len(PLAYER_PIXELS) * scale    # Bruk same høyde som standard figurer
    
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

# Verbedrede sprite-design for HD-versjon
# Player med mer detaljert og organisk form
HD_PLAYER_PIXELS = [
    "     ▒▄▄▒     ",
    "    ▒█▀▀█▒    ",
    "   ▓█████▓   ",
    "  ▓███████▓  ",
    " ▓█████████▓ ",
    "███████████",
    "█ █ █ █ █ █"
]

# HD alien type 1 frame 1
HD_ALIEN1_PIXELS_FRAME1 = [
    "   ▒▄██▄▒   ",
    "  ▓██████▓  ",
    " ▓█▒█  █▒█▓ ",
    "▓███████████▓",
    " ▓█ ▓██▓ █▓ ",
    "  █▓ ▀▀ ▓█  ",
    " ▒█      █▒ "
]

# HD alien type 1 frame 2
HD_ALIEN1_PIXELS_FRAME2 = [
    "   ▒▄██▄▒   ",
    "  ▓██████▓  ",
    " ▓█▒█  █▒█▓ ",
    "▓███████████▓",
    "  █▓ ▀▀ ▓█  ",
    " ▓█ ▓██▓ █▓ ",
    "▒█        █▒"
]

# HD alien type 2 frame 1
HD_ALIEN2_PIXELS_FRAME1 = [
    "  ▒▄████▄▒  ",
    " ▓█▒▄██▄▒█▓ ",
    "▓█▓██████▓█▓",
    "███ █  █ ███",
    " ▓█▒████▒█▓ ",
    "  ▒▀▓██▓▀▒  ",
    "   ▀▒  ▒▀   "
]

# HD alien type 2 frame 2
HD_ALIEN2_PIXELS_FRAME2 = [
    "  ▒▄████▄▒  ",
    " ▓█▒▄██▄▒█▓ ",
    "▓█▓██████▓█▓",
    "███ █  █ ███",
    "  ▒▀▓██▓▀▒  ",
    " ▓█▒████▒█▓ ",
    "▀▒        ▒▀"
]

# HD alien type 3 frame 1
HD_ALIEN3_PIXELS_FRAME1 = [
    "▄▒  ▄██▄  ▒▄",
    "▓████████████▓",
    "█▓▒█▄██▄█▒▓█",
    "▓████████████▓",
    " ▓█ ▓  ▓ █▓ ",
    "  ▀▒ ██ ▒▀  ",
    "    ▀▀▀▀    "
]

# HD alien type 3 frame 2
HD_ALIEN3_PIXELS_FRAME2 = [
    "▄▒  ▄██▄  ▒▄",
    "▓████████████▓",
    "█▓▒█▄██▄█▒▓█",
    "▓████████████▓",
    "  ▀▒ ██ ▒▀  ",
    " ▓█ ▓  ▓ █▓ ",
    "   ▀▀  ▀▀   "
]

# HD bonusstjerne
HD_STAR_PIXELS = [
    "      ★       ",
    "     ⭐⭐⭐     ",
    "    ★ ✧ ★    ",
    "   ⭐✨✨✨⭐   ",
    "  ★✧✨⭐✨✧★  ",
    " ⭐✨⭐✨⭐✨⭐ ",
    "★✧✨✨⭐✨✨✧★",
    " ⭐✨⭐✨⭐✨⭐ ",
    "  ★✧✨⭐✨✧★  ",
    "   ⭐✨✨✨⭐   ",
    "    ★ ✧ ★    ",
    "     ⭐⭐⭐     ",
    "      ★       "
]

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

def create_alien_sprites(hd_mode=True):
    if hd_mode:
        return [
            # Type 1 aliens (purple)
            [create_hd_sprite(HD_ALIEN1_PIXELS_FRAME1, PURPLE),
             create_hd_sprite(HD_ALIEN1_PIXELS_FRAME2, PURPLE)],
            # Type 2 aliens (cyan)
            [create_hd_sprite(HD_ALIEN2_PIXELS_FRAME1, CYAN),
             create_hd_sprite(HD_ALIEN2_PIXELS_FRAME2, CYAN)],
            # Type 3 aliens (red)
            [create_hd_sprite(HD_ALIEN3_PIXELS_FRAME1, NEON_RED),
             create_hd_sprite(HD_ALIEN3_PIXELS_FRAME2, NEON_RED)]
        ]
    else:
        return [
            # Type 1 aliens (purple)
            [create_sprite(ALIEN1_PIXELS_FRAME1, PURPLE),
             create_sprite(ALIEN1_PIXELS_FRAME2, PURPLE)],
            # Type 2 aliens (cyan)
            [create_sprite(ALIEN2_PIXELS_FRAME1, CYAN),
             create_sprite(ALIEN2_PIXELS_FRAME2, CYAN)],
            # Type 3 aliens (red)
            [create_sprite(ALIEN3_PIXELS_FRAME1, NEON_RED),
             create_sprite(ALIEN3_PIXELS_FRAME2, NEON_RED)]
        ]

class BonusStar:
    def __init__(self, hd_mode=True):
        if hd_mode:
            self.sprite = create_hd_sprite(HD_STAR_PIXELS, (255, 215, 0))  # Gold color
        else:
            self.sprite = create_sprite(STAR_PIXELS, (255, 215, 0))  # Gold color
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.rect = pygame.Rect(0, 50, self.width, self.height)
        self.speed = 3
        self.direction = 1
        self.active = False
        self.points = 150
        
    def update(self):
        if self.active:
            self.rect.x += self.speed * self.direction
            if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
                self.direction *= -1
            
    def draw(self, surface):
        if self.active:
            surface.blit(self.sprite, self.rect)
            
    def activate(self):
        self.active = True
        self.rect.x = 0 if random.random() < 0.5 else SCREEN_WIDTH - self.width
        self.direction = 1 if self.rect.x == 0 else -1

class BonusText:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.duration = 60  # 60 frames = 1 second at 60 FPS
        self.flash_speed = 5  # Lower = faster flashing
        self.points = 500
        self.font = pygame.font.Font(None, 48)  # Larger font for bonus text
        
    def activate(self, x, y):
        self.active = True
        self.timer = self.duration
        self.x = x
        self.y = y
        
    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False
                
    def draw(self, surface):
        if self.active:
            if (self.timer // self.flash_speed) % 2:  # Flash effect
                text = self.font.render(f'BONUS {self.points}!', True, (255, 255, 0))  # Yellow color
                text_rect = text.get_rect(center=(self.x, self.y))
                surface.blit(text, text_rect)

# Bruk HD-grafikk
USE_HD_GRAPHICS = True

# Create sprites with HD mode
player_sprite = create_hd_sprite(HD_PLAYER_PIXELS, GREEN) if USE_HD_GRAPHICS else create_sprite(PLAYER_PIXELS, GREEN)
alien_sprites = create_alien_sprites(USE_HD_GRAPHICS)
bonus_star = BonusStar(USE_HD_GRAPHICS)
bonus_text = BonusText()

# Add animation timer
animation_frame = 0
animation_speed = 30  # Lower number = faster animation
animation_counter = 0

# Particle system for explosions
particles = []

# Player settings
PLAYER_WIDTH = player_sprite.get_width()
PLAYER_HEIGHT = player_sprite.get_height()
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 60
player_speed = 5

# Bullet settings
BULLET_WIDTH = 4
BULLET_HEIGHT = 12
bullets = []
BULLET_SPEED = 8

# Alien settings
ALIEN_SPEED = 0.5  # Slower horizontal movement
VERTICAL_STEP = 10  # Smaller vertical step (was 20)
aliens = []
alien_direction = 1
DIVE_SPEED = 0.8  # Reduced from 1.5 to 0.8 for slower diving
DIVE_CHANCE = 0.001
SWAY_AMPLITUDE = 60
MAX_DIVERS = 2
SWAY_SPEED = 600  # Increased from 400 to 600 for slower swaying motion
ALIEN_SHOOT_CHANCE = 0.001  # Reduced from 0.002 to 0.001 (50% less frequent)
ALIEN_BULLET_SPEED = 3
alien_bullets = []  # List to store alien bullets
DESCENT_SPEED = 0.8  # Speed for smooth descent - Økt fra 0.5 til 0.8 for raskere nedstigning
DESCENT_TARGET = 0  # Target Y position for smooth descent

# Add wave progression and last score
SPEED_INCREASE = 1.15  # 15% speed increase per wave
base_alien_speed = 0.5  # Store original speed
current_wave = 1
last_score = 0

# Level definitions
class LevelConfigs:
    def __init__(self):
        self.levels = [
            # Level 1 - Standard grid formation
            {
                "name": "Standard Invaders",
                "pattern": "grid",
                "rows": 5,
                "cols": 11,
                "row_spacing": 40,
                "col_spacing": 50,
                "start_x": 100,
                "start_y": 50,
                "alien_types": [0, 0, 1, 1, 2],  # Type pattern from top to bottom
                "bonus_chance": 0.005,
                "shoot_chance": 0.001,
                "dive_chance": 0.0,  # Ingen dykking på nivå 1
                "max_divers": 0,     # Ingen dykkere tillatt på nivå 1
                "speed_multiplier": 2.0,  # Økt fra 1.5 til 2.0 for raskere horisontal bevegelse
                "classic_movement": True,  # Flag for klassisk bevegelse (side til side + nedover ved kant)
                "descent_step": 20,   # Normal nedstegningsstørrelse
                "descent_speed_multiplier": 1.5  # Økt fra 1.0 til 1.5 for raskere nedstigning
            },
            # Level 2 - Raskere nedstigning
            {
                "name": "Advancing Invaders",
                "pattern": "grid",
                "rows": 5,
                "cols": 11,
                "row_spacing": 40,
                "col_spacing": 50,
                "start_x": 100,
                "start_y": 50,
                "alien_types": [0, 0, 1, 1, 2],  # Samme mønster som nivå 1
                "bonus_chance": 0.007,
                "shoot_chance": 0.0012,
                "dive_chance": 0.0,  # Fortsatt ingen dykking
                "max_divers": 0,     
                "speed_multiplier": 2.3,  # Økt fra 1.7 til 2.3 for raskere horisontal bevegelse
                "classic_movement": True,  
                "descent_step": 40,   # Dobbelt så stor nedstegning når de snur
                "descent_speed_multiplier": 3.0  # Beholder den høye hastigheten for nedstigning
            },
            # Level 3 - V-formation (tidligere level 2)
            {
                "name": "V-Formation",
                "pattern": "v_shape",
                "rows": 5, 
                "cols": 11,
                "row_spacing": 40,
                "col_spacing": 50,
                "start_x": 100,
                "start_y": 50,
                "alien_types": [2, 1, 1, 0, 0],  # Reversed pattern
                "bonus_chance": 0.008,
                "shoot_chance": 0.0015,
                "dive_chance": 0.0015,
                "max_divers": 3,
                "speed_multiplier": 1.2,
                "classic_movement": False,  # Normal bevegelse for andre nivåer
                "descent_step": 10,
                "descent_speed_multiplier": 1.0
            },
            # Level 4 - Diamond formation (tidligere level 3)
            {
                "name": "Diamond Attack",
                "pattern": "diamond",
                "rows": 7,
                "cols": 7,
                "row_spacing": 40,
                "col_spacing": 60,
                "start_x": 150,
                "start_y": 50,
                "alien_types": [0, 1, 2, 2, 2, 1, 0],  # Center-heavy pattern
                "bonus_chance": 0.01,
                "shoot_chance": 0.002,
                "dive_chance": 0.002,
                "max_divers": 4,
                "speed_multiplier": 1.4,
                "classic_movement": False,
                "descent_step": 10,
                "descent_speed_multiplier": 1.0
            },
            # Level 5 - Spiral formation (tidligere level 4)
            {
                "name": "Spiral Invasion",
                "pattern": "spiral",
                "alien_count": 30,
                "start_x": SCREEN_WIDTH // 2,
                "start_y": 120,
                "spiral_spacing": 30,
                "alien_types": [0, 1, 2],  # Mix of all types
                "bonus_chance": 0.012,
                "shoot_chance": 0.0025,
                "dive_chance": 0.0025,
                "max_divers": 5,
                "speed_multiplier": 1.6,
                "classic_movement": False,
                "descent_step": 10,
                "descent_speed_multiplier": 1.0
            },
            # Level 6 - Random scattered formation (tidligere level 5)
            {
                "name": "Scattered Assault",
                "pattern": "random",
                "alien_count": 35,
                "start_x": 80,
                "start_y": 50,
                "width_range": SCREEN_WIDTH - 160,
                "height_range": 200,
                "alien_types": [0, 1, 2],
                "bonus_chance": 0.015,
                "shoot_chance": 0.003,
                "dive_chance": 0.003,
                "max_divers": 6,
                "speed_multiplier": 1.8,
                "classic_movement": False,
                "descent_step": 10,
                "descent_speed_multiplier": 1.0
            },
            # Level 7 - Enhanced classic (tidligere level 6)
            {
                "name": "Elite Invaders",
                "pattern": "grid",
                "rows": 6,
                "cols": 12,
                "row_spacing": 35,
                "col_spacing": 45,
                "start_x": 85,
                "start_y": 40,
                "alien_types": [2, 2, 1, 1, 0, 0],  # Tøffere aliens foran
                "bonus_chance": 0.02,
                "shoot_chance": 0.004,
                "dive_chance": 0.0,  # Fortsatt ingen dykkere
                "max_divers": 0,
                "speed_multiplier": 2.0,  # Dobbel hastighet i forhold til nivå 1
                "classic_movement": True,
                "descent_step": 30,
                "descent_speed_multiplier": 2.5  # Rask nedstigning
            }
        ]
        self.max_level = len(self.levels)
    
    def get_level(self, level_num):
        # Get level configuration with wraparound for continuous play
        level_index = (level_num - 1) % self.max_level
        config = self.levels[level_index].copy()
        
        # Apply difficulty scaling for repeated levels
        if level_num > self.max_level:
            cycle = (level_num - 1) // self.max_level
            # Increase speed multiplier by 10% for each cycle through all levels
            config["speed_multiplier"] *= (1.1 ** cycle)
            
            # Increase shooting and diving chances
            config["shoot_chance"] *= (1.1 ** cycle)
            config["dive_chance"] *= (1.1 ** cycle)
            
            # Cap the max divers to a reasonable number
            config["max_divers"] = min(config["max_divers"] + cycle, 10)
        
        return config

# Create level configuration instance
level_configs = LevelConfigs()
current_level = 1

def create_aliens():
    global DESCENT_TARGET, ALIEN_SHOOT_CHANCE, DIVE_CHANCE, MAX_DIVERS, alien_direction
    aliens.clear()
    DESCENT_TARGET = 0  # Reset descent target when creating new aliens
    
    # Get the configuration for the current level
    config = level_configs.get_level(current_level)
    
    # Update global settings based on level config
    ALIEN_SHOOT_CHANCE = config["shoot_chance"]
    DIVE_CHANCE = config["dive_chance"]
    MAX_DIVERS = config["max_divers"]
    
    # Create aliens based on the pattern
    if config["pattern"] == "grid":
        # Standard grid formation
        for row in range(config["rows"]):
            for col in range(config["cols"]):
                alien_type = config["alien_types"][row % len(config["alien_types"])]
                alien = {
                    'rect': pygame.Rect(
                        config["start_x"] + col * config["col_spacing"], 
                        config["start_y"] + row * config["row_spacing"], 
                        30, 30
                    ),
                    'type': alien_type,
                    'diving': False,
                    'dive_speed': DIVE_SPEED,
                    'original_x': config["start_x"] + col * config["col_spacing"],
                    'can_shoot': col % 4 == 0  # Only every fourth alien can shoot
                }
                aliens.append(alien)
    
    elif config["pattern"] == "v_shape":
        # V-formation
        center_col = config["cols"] // 2
        for row in range(config["rows"]):
            for col in range(config["cols"]):
                # Skip positions to create V shape
                offset = abs(col - center_col)
                if offset > row:
                    continue
                
                alien_type = config["alien_types"][row % len(config["alien_types"])]
                alien = {
                    'rect': pygame.Rect(
                        config["start_x"] + col * config["col_spacing"], 
                        config["start_y"] + row * config["row_spacing"], 
                        30, 30
                    ),
                    'type': alien_type,
                    'diving': False,
                    'dive_speed': DIVE_SPEED,
                    'original_x': config["start_x"] + col * config["col_spacing"],
                    'can_shoot': col % 3 == 0  # Increased shooting frequency
                }
                aliens.append(alien)
    
    elif config["pattern"] == "diamond":
        # Diamond formation
        center_row = config["rows"] // 2
        center_col = config["cols"] // 2
        
        for row in range(config["rows"]):
            for col in range(config["cols"]):
                # Skip positions to create diamond shape
                row_offset = abs(row - center_row)
                col_offset = abs(col - center_col)
                if row_offset + col_offset > center_row:
                    continue
                
                alien_type = config["alien_types"][row % len(config["alien_types"])]
                alien = {
                    'rect': pygame.Rect(
                        config["start_x"] + col * config["col_spacing"], 
                        config["start_y"] + row * config["row_spacing"], 
                        30, 30
                    ),
                    'type': alien_type,
                    'diving': False,
                    'dive_speed': DIVE_SPEED,
                    'original_x': config["start_x"] + col * config["col_spacing"],
                    'can_shoot': (row_offset + col_offset < 2)  # Center aliens shoot more
                }
                aliens.append(alien)
    
    elif config["pattern"] == "spiral":
        # Spiral formation
        center_x = config["start_x"]
        center_y = config["start_y"]
        radius = 0
        angle_step = 0.5  # Adjust for tighter/looser spiral
        
        for i in range(config["alien_count"]):
            angle = i * angle_step
            radius = i * config["spiral_spacing"] / 10
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            alien_type = config["alien_types"][i % len(config["alien_types"])]
            alien = {
                'rect': pygame.Rect(int(x), int(y), 30, 30),
                'type': alien_type,
                'diving': False,
                'dive_speed': DIVE_SPEED,
                'original_x': x,
                'can_shoot': i % 3 == 0
            }
            aliens.append(alien)
    
    elif config["pattern"] == "random":
        # Random scattered formation
        for i in range(config["alien_count"]):
            x = config["start_x"] + random.randint(0, config["width_range"])
            y = config["start_y"] + random.randint(0, config["height_range"])
            
            # Make sure aliens aren't too close together
            while any(abs(x - a['rect'].x) < 30 and abs(y - a['rect'].y) < 30 for a in aliens):
                x = config["start_x"] + random.randint(0, config["width_range"])
                y = config["start_y"] + random.randint(0, config["height_range"])
            
            alien_type = random.choice(config["alien_types"])
            alien = {
                'rect': pygame.Rect(int(x), int(y), 30, 30),
                'type': alien_type,
                'diving': False,
                'dive_speed': DIVE_SPEED * (1 + random.random() * 0.5),  # Randomized dive speed
                'original_x': x,
                'can_shoot': random.random() < 0.25  # 25% chance an alien can shoot
            }
            aliens.append(alien)
    
    # Ensure random direction on new level
    alien_direction = random.choice([-1, 1])
    
    # Update bonus star chance
    if random.random() < config["bonus_chance"]:
        bonus_star.activate()

def update_aliens():
    global alien_direction, DESCENT_TARGET
    
    # Get current level config
    config = level_configs.get_level(current_level)
    
    # Calculate current speed based on level config
    current_speed = base_alien_speed * config["speed_multiplier"] * (SPEED_INCREASE ** (current_wave - 1))
    
    # Hent nedstegningsstørrelse fra nivåkonfigurasjon, med standard fallback
    descent_step = config.get("descent_step", VERTICAL_STEP)
    
    # Check edges before moving
    should_change_direction = False
    
    if config.get("classic_movement", False):
        # For klassisk bevegelse - finn ytterste fiende på hver side
        left_most = min((alien['rect'].x for alien in aliens if not alien['diving']), default=SCREEN_WIDTH)
        right_most = max((alien['rect'].x + alien['rect'].width for alien in aliens if not alien['diving']), default=0)
        
        # Sjekk om ytterste fiender treffer kanten
        if (left_most + current_speed * alien_direction <= 30) or (right_most + current_speed * alien_direction >= SCREEN_WIDTH - 30):
            should_change_direction = True
    else:
        # Standard sjekk for ikke-klassisk bevegelse
        for alien in aliens:
            if not alien['diving']:
                next_x = alien['rect'].x + (current_speed * alien_direction)
                if next_x + alien['rect'].width >= SCREEN_WIDTH - 10 or next_x <= 10:
                    should_change_direction = True
                    break
    
    # Change direction if needed
    if should_change_direction:
        alien_direction *= -1  # Reverse direction
        
        # I stedet for å bruke en gjennomsnittlig posisjon, sett individuelle mål for hver fiende
        if config.get("classic_movement", False):
            # For klassisk bevegelse, flytt alle fiender nedover med samme beløp
            for alien in aliens:
                if not alien['diving']:
                    # Sett individuelt mål for hver fiende basert på dens nåværende posisjon
                    alien['descent_target'] = alien['rect'].y + descent_step
        else:
            DESCENT_TARGET += VERTICAL_STEP
    
    # Move all aliens
    for alien in aliens:
        if not alien['diving']:
            # Move horizontally
            alien['rect'].x += current_speed * alien_direction
            alien['original_x'] = alien['rect'].x  # Update original position
            
            # Smooth descent movement - nå for både klassisk og moderne bevegelse
            if config.get("classic_movement", False):
                # For klassisk bevegelse, sjekk om fienden har et nedstigningmål
                if 'descent_target' in alien and alien['rect'].y < alien['descent_target']:
                    # Hent hastighetsmultiplikator for nedstigning fra konfigurasjon
                    descent_speed_mult = config.get("descent_speed_multiplier", 1.0)
                    
                    # Beregn faktisk nedstegningshastighet basert på konfigurasjonen
                    base_descent_speed = DESCENT_SPEED * descent_speed_mult
                    
                    # Avstandsbasert hastighet - jo lengre fra målet, jo raskere beveger de seg
                    distance_to_target = alien['descent_target'] - alien['rect'].y
                    
                    # For klassisk bevegelse, bruk en jevnere akselerasjon
                    # Start sakte og øk gradvis hastigheten
                    progress = min(1.0, distance_to_target / descent_step)
                    
                    # Kvadratisk akselerasjon for jevnere start og raskere slutt
                    speed_factor = progress * progress * 3.0
                    
                    # Sikre minimum hastighet
                    speed_factor = max(0.2, speed_factor)
                    
                    # Bruk justert hastighet
                    actual_descent_speed = base_descent_speed * speed_factor
                    
                    # Begrens maksimal hastighet for å unngå for rask bevegelse
                    actual_descent_speed = min(actual_descent_speed, descent_step / 10)
                    
                    alien['rect'].y += actual_descent_speed
            else:
                # For moderne bevegelse, bruk global DESCENT_TARGET
                if alien['rect'].y < DESCENT_TARGET:
                    # Hent hastighetsmultiplikator for nedstigning fra konfigurasjon
                    descent_speed_mult = config.get("descent_speed_multiplier", 1.0)
                    
                    # Beregn faktisk nedstegningshastighet basert på konfigurasjonen
                    base_descent_speed = DESCENT_SPEED * descent_speed_mult
                    
                    # Avstandsbasert hastighet med boost ved større avstander
                    distance_to_target = DESCENT_TARGET - alien['rect'].y
                    if distance_to_target > 30:
                        boost_factor = min(distance_to_target / 20, 4.0)  # Maks 4x boost
                        alien['rect'].y += base_descent_speed * boost_factor
                    else:
                        alien['rect'].y += base_descent_speed
            
            # Shooting logic for non-diving aliens
            if alien['can_shoot'] and random.random() < ALIEN_SHOOT_CHANCE:
                bullet = pygame.Rect(
                    alien['rect'].centerx - BULLET_WIDTH // 2,
                    alien['rect'].bottom,
                    BULLET_WIDTH,
                    BULLET_HEIGHT
                )
                alien_bullets.append(bullet)
            
            # Only allow new diver if we're under the maximum and diving is enabled
            if config.get("dive_chance", 0) > 0:
                diving_count = sum(1 for alien in aliens if alien['diving'])
                if diving_count < MAX_DIVERS and random.random() < DIVE_CHANCE:
                    alien['diving'] = True
                    diving_count += 1
        else:
            # Diving movement - combine downward motion with a gentler sine wave
            alien['rect'].y += alien['dive_speed']
            time_offset = pygame.time.get_ticks() / SWAY_SPEED
            sway_x = alien['original_x'] + math.sin(time_offset) * SWAY_AMPLITUDE
            alien['rect'].x = sway_x
            
            # Reset if alien goes off screen
            if alien['rect'].top > SCREEN_HEIGHT:
                alien['rect'].y = 0
                alien['diving'] = False
                alien['rect'].x = alien['original_x']
                diving_count -= 1

def create_explosion(x, y, color):
    for _ in range(20):
        particles.append(Particle(x, y, color))

def create_bonus_explosion(x, y):
    colors = [(255, 215, 0), (255, 255, 0), (255, 165, 0)]  # Gold, Yellow, Orange
    for _ in range(30):  # More particles for bonus explosion
        color = random.choice(colors)
        particles.append(Particle(x, y, color))

# Star field for background
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.5, 2.0)
        self.brightness = random.randint(50, 255)
        self.size = random.randint(1, 3)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, surface):
        color = (self.brightness,) * 3
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

# Create stars
stars = [Star() for _ in range(100)]

# Game settings
clock = pygame.time.Clock()
score = 0
high_score = 0
font = pygame.font.Font(None, 36)

def create_button(text, width=200, height=50):
    surface = pygame.Surface((width, height))
    surface.fill((50, 50, 50))  # Dark gray background
    pygame.draw.rect(surface, WHITE, surface.get_rect(), 2)  # White border
    
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(width/2, height/2))
    surface.blit(text_surface, text_rect)
    return surface

def draw_game_elements():
    # Draw stars
    for star in stars:
        star.draw(screen)

    # Draw bonus star
    bonus_star.draw(screen)

    # Draw player
    screen.blit(player_sprite, (player_x, player_y))

    # Draw aliens with animation
    for alien in aliens:
        screen.blit(alien_sprites[alien['type']][animation_frame], alien['rect'])

    # Draw player bullets
    for bullet in bullets:
        pygame.draw.rect(screen, GREEN, bullet)

    # Draw alien bullets
    for bullet in alien_bullets:
        pygame.draw.rect(screen, (255, 0, 0), bullet)

    # Draw particles
    for particle in particles:
        particle.draw(screen)

    # Draw score on left
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw high score and last score on right
    high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
    last_score_text = font.render(f'Last Score: {last_score}', True, WHITE)
    
    high_score_rect = high_score_text.get_rect()
    last_score_rect = last_score_text.get_rect()
    
    high_score_rect.topright = (SCREEN_WIDTH - 10, 10)
    last_score_rect.topright = (SCREEN_WIDTH - 10, 40)  # Position below high score
    
    screen.blit(high_score_text, high_score_rect)
    screen.blit(last_score_text, last_score_rect)
    
    # Draw level info
    level_config = level_configs.get_level(current_level)
    level_text = font.render(f'Level {current_level}: {level_config["name"]}', True, WHITE)
    level_rect = level_text.get_rect(midtop=(SCREEN_WIDTH/2, 10))
    screen.blit(level_text, level_rect)

def main():
    global player_x, score, alien_direction, animation_frame, animation_counter, high_score, current_wave, current_level

    # Create restart button
    restart_button = create_button("Play Again")
    button_rect = restart_button.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100))

    create_aliens()
    running = True
    game_over = False
    flash_timer = 0
    flash_speed = 15  # Lower number = faster flashing

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_pos):
                        game_over = False
                        reset_game()
                        player_x = SCREEN_WIDTH // 2
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_over = False
                    reset_game()
                    player_x = SCREEN_WIDTH // 2
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(
                        player_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2,
                        player_y,
                        BULLET_WIDTH,
                        BULLET_HEIGHT
                    )
                    bullets.append(bullet)

        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
                player_x += player_speed

            # Update stars
            for star in stars:
                star.update()

            # Update bonus star
            bonus_star.update()

            # Move player bullets
            for bullet in bullets[:]:
                bullet.y -= BULLET_SPEED
                if bullet.y < 0:
                    bullets.remove(bullet)

            # Move alien bullets
            for bullet in alien_bullets[:]:
                bullet.y += ALIEN_BULLET_SPEED
                if bullet.y > SCREEN_HEIGHT:
                    alien_bullets.remove(bullet)
                # Check if alien bullet hits player
                player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
                if bullet.colliderect(player_rect):
                    game_over = True
                    break

            # Update aliens with new movement pattern
            update_aliens()

            # Update animation
            animation_counter += 1
            if animation_counter >= animation_speed:
                animation_frame = (animation_frame + 1) % 2
                animation_counter = 0

            # Update particles
            particles[:] = [p for p in particles if p.update()]

            # Update bonus text
            bonus_text.update()

            # Collision detection for player bullets
            for bullet in bullets[:]:
                # Check bonus star collision
                if bonus_star.active and bullet.colliderect(bonus_star.rect):
                    create_bonus_explosion(bonus_star.rect.centerx, bonus_star.rect.centery)
                    score += bonus_text.points  # Use points from bonus_text
                    bonus_text.activate(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)  # Activate bonus text
                    bonus_star.active = False
                    bullets.remove(bullet)
                    continue

                for alien in aliens[:]:
                    if bullet.colliderect(alien['rect']):
                        create_explosion(alien['rect'].centerx, alien['rect'].centery,
                                      alien_sprites[alien['type']][0].get_at((0, 0)))
                        if bullet in bullets:
                            bullets.remove(bullet)
                        aliens.remove(alien)
                        score += 10 + (20 if alien['diving'] else 0)
                        break

            # Game over conditions
            if not aliens:
                current_wave += 1  # Increment wave counter
                current_level += 1  # Gå til neste nivå for hver gang alle fiendene er skutt
                
                bonus_star.activate()
                create_aliens()
                alien_direction = 1
            
            if any(alien['rect'].bottom >= player_y for alien in aliens):
                game_over = True

        # Drawing
        screen.fill(BLACK)
        
        if game_over:
            # Update high score when game ends
            high_score = max(high_score, score)
            
            # Flashing effect
            flash_timer += 1
            if flash_timer < flash_speed:
                screen.fill((50, 0, 0))  # Dark red flash
            elif flash_timer < flash_speed * 2:
                screen.fill(BLACK)
            else:
                flash_timer = 0
            
            # Draw game over text
            game_over_text = font.render('Game Over! Press Enter to Restart', True, WHITE)
            final_score_text = font.render(f'Final Score: {score}', True, WHITE)
            
            screen.blit(game_over_text, 
                       (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                        SCREEN_HEIGHT//2 - 50))
            screen.blit(final_score_text,
                       (SCREEN_WIDTH//2 - final_score_text.get_width()//2,
                        SCREEN_HEIGHT//2))
            
            # Draw restart button
            screen.blit(restart_button, button_rect)
        else:
            draw_game_elements()
            # Draw bonus text on top of everything
            bonus_text.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def reset_game():
    global score, aliens, bullets, alien_bullets, particles, alien_direction, current_wave, last_score, current_level
    last_score = score  # Store last score before resetting
    score = 0
    aliens = []
    bullets = []
    alien_bullets = []
    particles = []
    alien_direction = 1
    current_wave = 1  # Reset wave counter
    current_level = 1  # Reset level counter
    create_aliens()
    bonus_star.active = False

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 4)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.lifetime = random.randint(20, 40)
        # HD-partikkeleffekter
        self.glow = USE_HD_GRAPHICS
        self.glow_size = self.size * 2 if USE_HD_GRAPHICS else self.size
        self.glow_alpha = 120 if USE_HD_GRAPHICS else 0

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)
        if self.glow:
            self.glow_size = max(0, self.glow_size - 0.2)
            self.glow_alpha = max(0, self.glow_alpha - 3)
        return self.lifetime > 0

    def draw(self, surface):
        # Tegn glød først (bak partikkelen)
        if self.glow and self.glow_alpha > 0:
            glow_color = lighten_color(self.color, 50)
            glow_color = (*glow_color[:3], self.glow_alpha)
            glow_surf = pygame.Surface((int(self.glow_size*2), int(self.glow_size*2)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, glow_color, (int(self.glow_size), int(self.glow_size)), int(self.glow_size))
            surface.blit(glow_surf, (int(self.x-self.glow_size), int(self.y-self.glow_size)), special_flags=pygame.BLEND_ADD)
        
        # Tegn hovedpartikkel
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

if __name__ == '__main__':
    main()
