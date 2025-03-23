import pygame
import random
import math
from src.utils import create_sprite, create_hd_sprite
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, STAR_PIXELS, HD_STAR_PIXELS, 
    WHITE, NEON_RED, BONUS_SPEED
)

# Star field for background
class Star:
    """En stjerne i bakgrunnen"""
    
    def __init__(self):
        """Initialiserer stjerne med tilfeldig posisjon og egenskaper"""
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.1, 0.5)
        self.brightness = random.randint(100, 255)
        self.size = random.randint(1, 3)
    
    def update(self):
        """Oppdaterer stjernens posisjon (beveger seg nedover)"""
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)
            self.brightness = random.randint(100, 255)
    
    def draw(self, surface):
        """Tegner stjerne på skjermen"""
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

# Particle class for effects
class Particle:
    """En partikkel for eksplosjoner og effekter"""
    
    def __init__(self, x, y, vx, vy, color, size, lifetime):
        """Initialiserer en partikkel"""
        self.x = x
        self.y = y
        self.vx = vx  # X-hastighet
        self.vy = vy  # Y-hastighet
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.original_lifetime = lifetime
    
    def update(self):
        """Oppdaterer partikkelens posisjon og levetid"""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        
        # Gradually slow down the particle
        self.vx *= 0.98
        self.vy *= 0.98
        
        # Apply a small gravity effect
        self.vy += 0.05
    
    def draw(self, surface):
        """Tegner partikkelen på skjermen"""
        # Fade out as lifetime decreases
        alpha = int(255 * (self.lifetime / self.original_lifetime))
        
        # Create a temporary surface with transparency
        temp_surface = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        
        # Calculate color with alpha
        r, g, b = self.color
        color_with_alpha = (r, g, b, alpha)
        
        # Draw particle on temporary surface
        pygame.draw.circle(temp_surface, color_with_alpha, (self.size, self.size), self.size)
        
        # Blit temporary surface onto the main surface
        surface.blit(temp_surface, (int(self.x - self.size), int(self.y - self.size)))

class BonusStar:
    """Bonusobjekt som spilleren kan samle"""
    
    def __init__(self):
        """Initialiserer en bonusstjerne"""
        self.x = -100  # Start utenfor skjermen
        self.y = 100
        self.size = 20
        self.active = False
        self.speed = BONUS_SPEED
        self.pulse_timer = 0
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    
    def activate(self):
        """Aktiverer bonusstjernen på en tilfeldig posisjon"""
        # Start from left or right side
        if random.random() > 0.5:
            self.x = -self.size
            self.speed = BONUS_SPEED
        else:
            self.x = SCREEN_WIDTH + self.size
            self.speed = -BONUS_SPEED
        
        self.y = random.randint(50, 200)
        self.active = True
        self.pulse_timer = 0
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
    
    def update(self):
        """Oppdaterer bonusstjernens posisjon og tilstand"""
        if not self.active:
            # Random chance to activate
            if random.random() < 0.001:
                self.activate()
            return
        
        # Move horizontally
        self.x += self.speed
        
        # Update rectangle position
        self.rect.x = int(self.x - self.size/2)
        self.rect.y = int(self.y - self.size/2)
        
        # Deactivate if off screen
        if (self.speed > 0 and self.x > SCREEN_WIDTH + self.size) or \
           (self.speed < 0 and self.x < -self.size):
            self.active = False
        
        # Update pulse timer
        self.pulse_timer += 0.1
    
    def draw(self, surface):
        """Tegner bonusstjernen på skjermen"""
        if not self.active:
            return
        
        # Pulsating size effect
        pulse = math.sin(self.pulse_timer) * 0.2 + 1.0
        current_size = int(self.size * pulse)
        
        # Draw star shape
        points = []
        for i in range(10):
            angle = math.pi/2 + i * math.pi/5
            radius = current_size if i % 2 == 0 else current_size/2
            px = self.x + radius * math.cos(angle)
            py = self.y + radius * math.sin(angle)
            points.append((px, py))
        
        # Gold color with pulsating brightness
        pulse_brightness = int(200 + 55 * math.sin(self.pulse_timer * 2))
        color = (pulse_brightness, pulse_brightness, 0)  # Gold color
        
        # Draw the star
        pygame.draw.polygon(surface, color, points)
        
        # Draw outline
        pygame.draw.polygon(surface, WHITE, points, 2)

class BonusText:
    """Tekst som vises når spilleren samler en bonus"""
    
    def __init__(self):
        """Initialiserer bonustekst"""
        self.x = 0
        self.y = 0
        self.text = ""
        self.active = False
        self.timer = 0
        self.duration = 60  # Frames teksten vises
        self.font = pygame.font.Font(None, 36)
        self.points = 0  # Poengverdien til bonusen
    
    def activate(self, x, y, text="BONUS!", points=50):
        """Aktiverer bonustekst på angitt posisjon"""
        self.x = x
        self.y = y
        self.text = text
        self.points = points
        self.active = True
        self.timer = self.duration
    
    def update(self):
        """Oppdaterer bonustekstens tilstand"""
        if not self.active:
            return
        
        # Count down the timer
        self.timer -= 1
        
        # Move text upward slowly
        self.y -= 0.5
        
        # Deactivate when timer runs out
        if self.timer <= 0:
            self.active = False
    
    def draw(self, surface):
        """Tegner bonusteksten på skjermen"""
        if not self.active:
            return
        
        # Fade out as timer decreases
        alpha = int(255 * (self.timer / self.duration))
        
        # Create text render
        text_render = self.font.render(self.text, True, WHITE)
        
        # Create a temporary surface with transparency
        temp_surface = pygame.Surface(text_render.get_size(), pygame.SRCALPHA)
        temp_surface.fill((255, 255, 255, alpha))
        
        # Use the text render as a mask
        text_render.set_colorkey((0, 0, 0))
        temp_surface.blit(text_render, (0, 0))
        
        # Draw the text
        surface.blit(temp_surface, (self.x - text_render.get_width()//2, self.y - text_render.get_height()//2))

class FireworkParticle:
    """Partikkel som simulerer en fyrverkerieffekt"""
    
    def __init__(self, x, y, vx, vy, color):
        """Initialiserer en fyrverkeripartikkel"""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.trail = []  # Liste med posisjonspunkter for halen
        self.max_trail_length = 20
        self.exploded = False
    
    def update(self):
        """Oppdaterer fyrverkeriets posisjon og fart"""
        # Add current position to trail
        self.trail.append((self.x, self.y, 255))  # x, y, alpha
        
        # Limit trail length
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Reduce alpha for each point in trail
        for i in range(len(self.trail)):
            x, y, alpha = self.trail[i]
            self.trail[i] = (x, y, max(0, alpha - 10))
        
        # Move rocket
        self.x += self.vx
        self.y += self.vy
        
        # Apply gravity
        self.vy += 0.1
    
    def draw(self, surface):
        """Tegner fyrverkeriet på skjermen"""
        # Draw the trail
        for i in range(len(self.trail) - 1):
            x1, y1, alpha1 = self.trail[i]
            x2, y2, alpha2 = self.trail[i + 1]
            
            if alpha1 <= 0 or alpha2 <= 0:
                continue
            
            # Calculate color with alpha
            r, g, b = self.color
            color1 = (r, g, b, alpha1)
            color2 = (r, g, b, alpha2)
            
            # Draw a fading line segment
            pygame.draw.line(
                surface, 
                color1, 
                (int(x1), int(y1)), 
                (int(x2), int(y2)), 
                2
            )
        
        # Draw the rocket head if not exploded
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3) 