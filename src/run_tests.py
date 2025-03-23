"""
Test-script for Space Invaders komponenter
------------------------------------------
Dette skriptet tester ulike komponenter i spillet for å sikre at de fungerer riktig.
"""

import sys
import os
import unittest
import pygame
import random

# Importer komponentene som skal testes
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities import Star, Particle, BonusStar, BonusText, FireworkParticle
from src.sprites import create_alien_sprites, create_player_sprite
from src.utils import random_color, create_button, interpolate_color
from src.managers import HighscoreManager, LevelConfigs
from src.game import (
    create_aliens, create_grid_pattern, create_v_shape_pattern, 
    create_diamond_pattern, create_spiral_pattern, create_random_pattern
)

# Test-klasser
class EntityTests(unittest.TestCase):
    """Tester for spillentiteter"""
    
    def setUp(self):
        """Oppsett før hver test"""
        pygame.init()
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def tearDown(self):
        """Opprydding etter hver test"""
        pygame.quit()
    
    def test_star_creation(self):
        """Test at stjerner opprettes med gyldige verdier"""
        star = Star()
        self.assertTrue(0 <= star.x <= SCREEN_WIDTH)
        self.assertTrue(0 <= star.y <= SCREEN_HEIGHT)
        self.assertTrue(0 < star.speed <= 1)
        self.assertTrue(100 <= star.brightness <= 255)
        self.assertTrue(1 <= star.size <= 3)
    
    def test_star_update(self):
        """Test at stjernens posisjon oppdateres korrekt"""
        star = Star()
        initial_y = star.y
        star.update()
        # Stjerner skal bevege seg nedover
        self.assertGreater(star.y, initial_y)
    
    def test_particle_update(self):
        """Test at partikler beveger seg og reduserer levetid"""
        particle = Particle(100, 100, 1, -1, (255, 0, 0), 3, 30)
        initial_x, initial_y = particle.x, particle.y
        initial_lifetime = particle.lifetime
        
        particle.update()
        
        self.assertNotEqual(particle.x, initial_x)
        self.assertNotEqual(particle.y, initial_y)
        self.assertLess(particle.lifetime, initial_lifetime)
    
    def test_bonus_star_activation(self):
        """Test at bonusstjernen aktiveres korrekt"""
        bonus = BonusStar()
        self.assertFalse(bonus.active)
        
        bonus.activate()
        self.assertTrue(bonus.active)
    
    def test_bonus_text_activation(self):
        """Test at bonusteksten aktiveres korrekt"""
        bonus_text = BonusText()
        self.assertFalse(bonus_text.active)
        
        bonus_text.activate(100, 100, "+100")
        self.assertTrue(bonus_text.active)
        self.assertEqual(bonus_text.text, "+100")
    
    def test_firework_particle(self):
        """Test at fyrverkeripartikkelen fungerer"""
        firework = FireworkParticle(100, 100, 2, -5, (255, 0, 0))
        self.assertEqual(len(firework.trail), 0)
        
        firework.update()
        self.assertEqual(len(firework.trail), 1)
        self.assertEqual(firework.x, 102)  # 100 + 2
        self.assertLess(firework.y, 100)  # Should have moved up

class ManagerTests(unittest.TestCase):
    """Tester for managers"""
    
    def setUp(self):
        """Oppsett før hver test"""
        # Slett eventuell eksisterende highscore-fil for testing
        if os.path.exists("highscores.json"):
            os.rename("highscores.json", "highscores.json.bak")
    
    def tearDown(self):
        """Opprydning etter hver test"""
        # Gjenopprett original highscore-fil
        if os.path.exists("highscores.json.bak"):
            if os.path.exists("highscores.json"):
                os.remove("highscores.json")
            os.rename("highscores.json.bak", "highscores.json")
    
    def test_highscore_manager(self):
        """Test at highscore manager lagrer og laster scores"""
        manager = HighscoreManager()
        self.assertEqual(len(manager.get_highscores()), 0)
        
        # Legg til en score
        manager.add_score({'initials': 'AAA', 'score': 1000, 'date': '2023-01-01'})
        self.assertEqual(len(manager.get_highscores()), 1)
        
        # Test at highest_score fungerer
        self.assertEqual(manager.get_highest_score(), 1000)
        
        # Test at is_high_score fungerer
        self.assertTrue(manager.is_high_score(500))  # Mindre enn 10 scores
    
    def test_level_configs(self):
        """Test at level configurations fungerer"""
        configs = LevelConfigs()
        
        # Test første nivå
        level1 = configs.get_level(1)
        self.assertEqual(level1['name'], "Level 1 - Arrival")
        
        # Test gjentatte nivåer med økt vanskelighetsgrad
        level8 = configs.get_level(8)  # Første nivå i andre syklus
        self.assertIn("Cycle 2", level8['name'])
        
        # Test at shoot_chance øker med nivå
        self.assertGreater(level8['shoot_chance'], level1['shoot_chance'])

class AlienTests(unittest.TestCase):
    """Tester for alien-relaterte funksjoner"""
    
    def test_alien_patterns(self):
        """Test at alien-mønstrene genererer posisjoner"""
        # Test grid-mønster
        grid = create_grid_pattern(3, 5, 50, 50)
        self.assertEqual(len(grid), 15)  # 3 rader * 5 kolonner
        
        # Test V-formet mønster
        v_shape = create_v_shape_pattern(3, 5, 50, 50)
        self.assertEqual(len(v_shape), 15)
        
        # Test diamantmønster
        diamond = create_diamond_pattern(5, 5, 50, 50)
        self.assertGreater(len(diamond), 0)
        
        # Test spiralmønster
        spiral = create_spiral_pattern(20, 50, 50)
        self.assertEqual(len(spiral), 20)
        
        # Test tilfeldig mønster
        random = create_random_pattern(20, 50, 50)
        self.assertEqual(len(random), 20)
    
    def test_create_aliens(self):
        """Test at alien-oppretting fungerer"""
        # Lag en enkel level config
        config = {
            'pattern': 'grid',
            'rows': 3,
            'cols': 4,
            'spacing_x': 50,
            'spacing_y': 50,
            'alien_types': [0],
            'dive_chance': 0.5,
            'shoot_chance': 0.5,
            'max_bullets': 5
        }
        
        aliens = create_aliens(config)
        self.assertEqual(len(aliens), 12)  # 3 rader * 4 kolonner
        
        # Sjekk at alle aliens har de nødvendige egenskapene
        for alien in aliens:
            self.assertIn('rect', alien)
            self.assertIn('type', alien)
            self.assertIn('direction', alien)
            self.assertIn('can_shoot', alien)
            self.assertIn('can_dive', alien)
            self.assertIn('health', alien)

class UtilsTests(unittest.TestCase):
    """Tester for hjelpefunksjoner"""
    
    def setUp(self):
        """Oppsett før hver test"""
        pygame.init()
    
    def tearDown(self):
        """Opprydning etter hver test"""
        pygame.quit()
    
    def test_random_color(self):
        """Test at random_color genererer gyldige farger"""
        for _ in range(10):
            color = random_color()
            self.assertEqual(len(color), 3)
            for component in color:
                self.assertTrue(0 <= component <= 255)
    
    def test_create_button(self):
        """Test at knapper opprettes riktig"""
        button = create_button("Test", (255, 255, 255))
        self.assertIsInstance(button, pygame.Surface)
    
    def test_interpolate_color(self):
        """Test at fargeinterpolering fungerer"""
        color1 = (0, 0, 0)
        color2 = (255, 255, 255)
        
        # Halvveis mellom svart og hvit bør være grå
        mid_color = interpolate_color(color1, color2, 0.5)
        self.assertEqual(mid_color, (127, 127, 127))
        
        # Start farge ved 0
        start_color = interpolate_color(color1, color2, 0)
        self.assertEqual(start_color, color1)
        
        # Slutt farge ved 1
        end_color = interpolate_color(color1, color2, 1)
        self.assertEqual(end_color, color2)

def run_tests():
    """Kjør alle tester"""
    test_suite = unittest.TestSuite()
    
    # Legg til test-klassene
    test_suite.addTest(unittest.makeSuite(EntityTests))
    test_suite.addTest(unittest.makeSuite(ManagerTests))
    test_suite.addTest(unittest.makeSuite(AlienTests))
    test_suite.addTest(unittest.makeSuite(UtilsTests))
    
    # Kjør testene
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 