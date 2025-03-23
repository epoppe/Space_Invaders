import pygame
import random
import math
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, NEON_RED, GREEN,
    PLAYER_WIDTH, PLAYER_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT,
    ALIEN_BULLET_WIDTH, ALIEN_BULLET_HEIGHT, STATE_GAME_OVER
)

def draw_game_elements(screen, stars, player_x, player_y, bullets, alien_bullets, aliens, 
                       animation_frame, particles, score, high_score, current_level, current_wave,
                       bonus_star, bonus_text, alien_sprites, player_sprite):
    """Tegner alle spillelementer på skjermen"""
    # Clear screen
    screen.fill(BLACK)
    
    # Draw stars
    for star in stars:
        star.draw(screen)
    
    # Draw player
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    screen.blit(player_sprite, player_rect)
    
    # Draw player bullets
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet.x, bullet.y, BULLET_WIDTH // 2, BULLET_HEIGHT)
        pygame.draw.rect(screen, GREEN, bullet_rect)
    
    # Draw alien bullets
    for bullet in alien_bullets:
        bullet_rect = pygame.Rect(bullet.x, bullet.y, ALIEN_BULLET_WIDTH // 2, ALIEN_BULLET_HEIGHT)
        pygame.draw.rect(screen, NEON_RED, bullet_rect)
    
    # Draw aliens with animation
    for alien in aliens:
        alien_type = alien['type']
        frame = animation_frame
        row_index = alien.get('row_index', 0)  # Få rad-indeksen, standard til 0 hvis ikke satt
        
        # Hent sprite basert på type, rad og animasjonsramme
        try:
            alien_sprite = alien_sprites[alien_type][row_index][frame]
        except KeyError:
            # Fallback hvis vi ikke har en sprite for denne kombinasjonen
            alien_sprite = alien_sprites[alien_type][0][frame]
        
        # Tegn spriten på skjermen
        screen.blit(alien_sprite, alien['rect'])
    
    # Draw particles
    for particle in particles:
        particle.draw(screen)
    
    # Draw bonus star
    bonus_star.draw(screen)
    
    # Draw score and high score
    font = pygame.font.Font(None, 28)
    score_text = font.render(f'Score: {score}', True, WHITE)
    high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
    level_text = font.render(f'Level: {current_level}', True, WHITE)
    wave_text = font.render(f'Wave: {current_wave}', True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))
    screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))
    screen.blit(wave_text, (SCREEN_WIDTH - wave_text.get_width() - 10, 40))
    
    # Draw bonus text
    bonus_text.draw(screen)

def draw_game_over_screen(screen, score, high_score, restart_button, button_rect, 
                         flash_timer, flash_speed, font):
    """Tegner 'game over' skjermen"""
    # Flashing effect
    if flash_timer < flash_speed:
        screen.fill((50, 0, 0))  # Dark red flash
    elif flash_timer < flash_speed * 2:
        screen.fill(BLACK)
    
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
    
    return (flash_timer + 1) % (flash_speed * 2)  # Increment and wrap around

def draw_high_score_celebration(screen, celebration_timer, fireworks, explosion_particles, high_score_font):
    """Tegner feiringen av ny high score"""
    # Tegn alle fyrverkerieffekter
    for fw in fireworks:
        fw.draw(screen)
    for ep in explosion_particles:
        ep.draw(screen)
    
    # Tegn high score-tekst som pulserer
    pulse_scale = 1.0 + 0.1 * math.sin(pygame.time.get_ticks() / 200)
    
    # Stor gul tekst som feirer ny high score
    hs_text = high_score_font.render('Du går inn på topp 10', True, (255, 255, 0))  # Yellow
    hs_text_width = hs_text.get_width() * pulse_scale
    hs_text_height = hs_text.get_height() * pulse_scale
    hs_text_scaled = pygame.transform.scale(hs_text, (int(hs_text_width), int(hs_text_height)))
    hs_rect = hs_text_scaled.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150))
    screen.blit(hs_text_scaled, hs_rect)

def draw_text_input_screen(screen, initials, cursor_pos):
    """Tegner skjermen for å registrere initialer ved ny high score"""
    screen.fill(BLACK)
    
    # Create fonts
    title_font = pygame.font.Font(None, 48)
    text_font = pygame.font.Font(None, 36)
    initial_font = pygame.font.Font(None, 72)  # Larger font for initials
    
    # Create text
    title_text = title_font.render('New High Score!', True, WHITE)
    instruction_text = text_font.render('Enter your initials (3 letters):', True, WHITE)
    
    # Calculate total width of initials and spaces
    LETTER_WIDTH = 50
    SPACE_WIDTH = 10
    total_width = 3 * LETTER_WIDTH + 2 * SPACE_WIDTH
    
    # Position initial boxes
    start_x = SCREEN_WIDTH//2 - total_width//2
    letters_y = 250
    
    # Draw title and instructions
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))
    screen.blit(instruction_text, (SCREEN_WIDTH//2 - instruction_text.get_width()//2, 180))
    
    # Draw each initial box and letter
    for i in range(3):
        # Box position
        box_x = start_x + i * (LETTER_WIDTH + SPACE_WIDTH)
        
        # Draw the box
        box_color = (80, 80, 80)  # Gray
        box_rect = pygame.Rect(box_x, letters_y, LETTER_WIDTH, LETTER_WIDTH)
        pygame.draw.rect(screen, box_color, box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 2)  # Draw white border
        
        # Draw the letter if it exists
        if i < len(initials):
            letter = initials[i]
            letter_surf = initial_font.render(letter, True, WHITE)
            letter_rect = letter_surf.get_rect(center=(box_x + LETTER_WIDTH//2, letters_y + LETTER_WIDTH//2))
            screen.blit(letter_surf, letter_rect)
        
        # Draw cursor at current position
        if i == cursor_pos:
            # Flashing cursor
            if (pygame.time.get_ticks() // 500) % 2 == 0:  # Flash every 500ms
                cursor_height = 30
                cursor_y = letters_y + LETTER_WIDTH - cursor_height - 5
                pygame.draw.rect(screen, WHITE, (box_x + 5, cursor_y, LETTER_WIDTH - 10, cursor_height), 2)
    
    # Draw "press Enter to continue" text
    continue_text = text_font.render("Press Enter when complete", True, WHITE)
    screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, 380))

def draw_highscore_list(screen, highscore_manager):
    """Tegner high score-listen"""
    screen.fill(BLACK)
    
    # Fonts
    title_font = pygame.font.Font(None, 48)
    text_font = pygame.font.Font(None, 28)  # Redusert fra 36 til 28
    
    # Title
    title_text = title_font.render('Poengliste', True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
    
    # Get high scores
    highscores = highscore_manager.get_highscores()
    
    if not highscores:
        # No high scores yet
        no_scores_text = text_font.render('Ingen highscores ennå!', True, WHITE)
        screen.blit(no_scores_text, (SCREEN_WIDTH//2 - no_scores_text.get_width()//2, 200))
    else:
        # Draw column headers med norske navn
        header_rank = text_font.render('Plass', True, WHITE)
        header_initials = text_font.render('Initialer', True, WHITE)
        header_score = text_font.render('Poeng', True, WHITE)
        
        # Position headers
        rank_x = 100
        initials_x = SCREEN_WIDTH // 2 - 50
        score_x = SCREEN_WIDTH - 200
        
        # Draw headers
        screen.blit(header_rank, (rank_x, 120))
        screen.blit(header_initials, (initials_x, 120))
        screen.blit(header_score, (score_x, 120))
        
        # Draw separator line
        pygame.draw.line(screen, (100, 100, 100), (100, 150), (SCREEN_WIDTH - 100, 150), 2)
        
        # Draw each high score entry
        y_start = 180
        line_height = 30  # Redusert fra 40 til 30 for å passe med mindre fontstørrelse
        
        for i, entry in enumerate(highscores):
            # Rank
            rank_text = text_font.render(f"{i+1}.", True, WHITE)
            screen.blit(rank_text, (rank_x, y_start + i * line_height))
            
            # Initials
            initials_text = text_font.render(entry["initials"], True, WHITE)
            screen.blit(initials_text, (initials_x, y_start + i * line_height))
            
            # Score
            score_text = text_font.render(f"{entry['score']}", True, WHITE)
            screen.blit(score_text, (score_x, y_start + i * line_height))
    
    # Tegn en skillelinje mellom high score-listen og instruksjonen
    separator_y = SCREEN_HEIGHT - 130
    pygame.draw.line(screen, (100, 100, 100), (100, separator_y), (SCREEN_WIDTH - 100, separator_y), 2)
    
    # Draw instruction under skillelinjen
    instruction_text = text_font.render("Trykk Enter for å starte et nytt spill", True, WHITE)
    screen.blit(instruction_text, (SCREEN_WIDTH//2 - instruction_text.get_width()//2, SCREEN_HEIGHT - 80))

def draw_level_message(screen, level_message, level_message_timer, level_message_duration, level_message_font):
    """Tegner nivåbytte-melding"""
    if level_message_timer > 0:
        # Bruk en mindre tekst, men fortsatt stor nok til å være synlig
        pulse_alpha = min(255, int(255 * (level_message_timer / level_message_duration) * 1.5))
        level_text_surface = level_message_font.render(level_message, True, (255, 255, 255))
        level_text_surface.set_alpha(pulse_alpha)
        
        # Tegn teksten sentrert på skjermen
        text_rect = level_text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
        screen.blit(level_text_surface, text_rect) 