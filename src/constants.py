import pygame

# Skjerminnstillinger
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Farger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
NEON_RED = (255, 50, 50)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Spiller
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
PLAYER_SPEED = 8

# Bullets
BULLET_WIDTH = 8
BULLET_HEIGHT = 20
BULLET_SPEED = 12
ALIEN_BULLET_WIDTH = 6
ALIEN_BULLET_HEIGHT = 15
ALIEN_BULLET_SPEED = 8

# Aliens
ALIEN_WIDTH = 48
ALIEN_HEIGHT = 48
BASE_ALIEN_SPEED = 2
SPEED_INCREASE = 1.1  # Økning i hastighet for hver bølge

# Alien-typer
ALIEN_TYPE_STANDARD = 0
ALIEN_TYPE_SPEEDY = 1
ALIEN_TYPE_TANK = 2

# Alien-bevegelse
VERTICAL_STEP = 20  # Hvor langt aliens beveger seg nedover når de treffer kanten
SWAY_SPEED = 1000   # Hvor fort aliens svinger frem og tilbake når de dykker
SWAY_AMPLITUDE = 50 # Hvor langt aliens svinger fra side til side når de dykker

# Alien-oppførsel
DIVE_CHANCE = 0.01  # Sjansen for at en alien begynner å dykke på et tidspunkt
DIVE_SPEED = 5      # Hvor fort aliens dykker nedover
MAX_DIVERS = 3      # Maksimalt antall aliens som kan dykke samtidig
ALIEN_SHOOT_CHANCE = 0.02  # Sjansen for at en alien skyter på et tidspunkt

# Stjerner
NUM_STARS = 100     # Antall stjerner i bakgrunnen

# Spill-tilstander
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_NEW_HIGH_SCORE = 3
STATE_HIGH_SCORE_INPUT = 4
STATE_SHOW_HIGH_SCORES = 5

# Filstier
HIGHSCORE_FILE = "highscores.json"

# Lyd
VOLUME_SHOOT = 0.2
VOLUME_EXPLOSION = 0.3
VOLUME_ALIEN_SHOOT = 0.2
VOLUME_BONUS = 0.4

# Bonus
BONUS_CHANCE = 0.02  # Sjansen for at en bonusstjerne dukker opp
BONUS_SPEED = 3      # Hvor fort bonusstjernen beveger seg
BONUS_POINTS = [50, 100, 150, 200]  # Mulige poengsummer for bonusstjerne

# Game over
FLASH_SPEED = 10  # Hastighet på blinkingen på game over-skjermen

# Level-melding
LEVEL_MESSAGE_DURATION = 120  # Antall frames meldingen vises (2 sekunder med 60 FPS)

# High score-feiring
CELEBRATION_DURATION = 180  # Antall frames feiringen varer (3 sekunder med 60 FPS)

# Skjerminnstillinger
CAPTION = 'Retro Space Invaders'

# Farger
GREEN = (0, 255, 128)  # Brighter neon green
PURPLE = (180, 0, 255)  # Brighter purple
CYAN = (0, 255, 255)  # Bright cyan
WHITE = (255, 255, 255)

# Spillinnstillinger og konstanter
PLAYER_Y = SCREEN_HEIGHT - 60

# Alien-konstanter
ALIEN_DIVE_SPEED = 5

# Spillkonfigurasjoner
MAX_DIVERS = 3
DIVE_CHANCE = 0.002
DIVE_SPEED = 2

# Sprite designs i pixel art stil (using ASCII for visualization)
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

# HD versjon
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

# HD-modus
HD_MODE = True 