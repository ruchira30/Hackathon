import pygame
import random
import sys

# Initialize Pygame
pygame.init()
# Add sound
pygame.mixer.init()
sound = pygame.mixer.Sound("sound.mp3")
sound.set_volume(0.2)
sound.play()
# Set up the game window
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))

# Set up the font
font = pygame.font.SysFont(None, 100)

# Load the player, enemy, and bullet images
player_image = pygame.image.load("Spaceship_tut.png")
enemy_image = pygame.image.load("spaceship.png")
bullet_image = pygame.image.load("spr_bullet_strip02.png")

# Set up the player object
player_rect = player_image.get_rect()
player_rect.x = (window_width - player_rect.width) // 2
player_rect.y = window_height - player_rect.height
player_speed = 2

# Set up the bullets list
bullets = []
bullet_speed = 1

# Set up the enemies list
enemies = []
enemy_speed = 0.8

# Set up player lives
player_lives = 5

# Set up score
score = 0

# Set up the start button
button_width = 200
button_height = 100
button_x = (window_width - button_width) // 2
button_y = (window_height - button_height) // 2
start_button_image = pygame.image.load("play.png")
start_button_rect = start_button_image.get_rect()
start_button_rect.center = (button_x + button_width // 2, button_y + button_height // 2)

# Create a text surface
text_surface = font.render("Space Shooters", True, (0, 255, 255))

# Get the dimensions of the text surface
text_rect = text_surface.get_rect()

# Center the text surface on the screen
text_rect.center = (window_width // 2, 200)



# Game loop
show_start_screen = True
while show_start_screen:
# Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse was clicked inside the start button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(mouse_x, mouse_y):
             # Start the game
                show_start_screen = False

    # Draw graphics
    screen.fill((0, 0, 0))  # fill the screen with black color

    # Draw the "Space Shooters" text surface on the screen
    screen.blit(text_surface, text_rect)

    # Draw the start button image on the screen
    screen.blit(start_button_image, start_button_rect)

    # Update the display
    pygame.display.update()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Fire a bullet when the space bar is pressed
            bullet_rect = bullet_image.get_rect()

            bullet_rect.midbottom = player_rect.midtop
            bullets.append(bullet_rect)

    # Move the player based on keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    elif keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    elif keys[pygame.K_UP]:
        player_rect.y -= player_speed
    elif keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    # Keep the player within the screen boundaries
    if player_rect.left < 0:
        player_rect.left = 0
    elif player_rect.right > window_width:
        player_rect.right = window_width
    if player_rect.top < 0:
        player_rect.top = 0
    elif player_rect.bottom > window_height:
        player_rect.bottom = window_height

    # Move the bullets
    for bullet_rect in bullets:
        bullet_rect.y -= bullet_speed
    # Remove bullets that have gone offscreen
    bullets = [bullet_rect for bullet_rect in bullets if bullet_rect.bottom >= 0]

    # Add enemies randomly
    if len(enemies) < 20 and random.randint(0, 100) < 1:
        enemy_rect = enemy_image.get_rect()
        enemy_rect.x = random.randint(0, window_width - enemy_rect.width)
        enemy_rect.y = -enemy_rect.height
        enemies.append(enemy_rect)

    # Move the enemies and check for collisions with bullets
    for enemy_rect in enemies:
        enemy_rect.y += enemy_speed
        for bullet_rect in bullets:
            if enemy_rect.colliderect(bullet_rect):
                enemies.remove(enemy_rect)
                bullets.remove(bullet_rect)
                score += 1
                break
    # Check for collisions with player
    for enemy_rect in enemies:
        if enemy_rect.colliderect(player_rect):
            player_lives -= 1
            enemies.remove(enemy_rect)
            if player_lives <= 0:
                running = False

    # Draw graphics
    screen.fill((0, 0, 0))  # fill the screen with black color
    screen.blit(player_image, player_rect)
    for bullet_rect in bullets:
        screen.blit(bullet_image, bullet_rect)
    for enemy_rect in enemies:
        screen.blit(enemy_image, enemy_rect)

    # Draw lives
    font = pygame.font.SysFont(None, 30)
    lives_text = font.render("Lives: " + str(player_lives), True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    if player_lives <= 0:
        # display game over message
        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(window_width / 2, window_height / 2))
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(300)
    # Draw score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (window_width - score_text.get_width() - 10, 10))

    if score > 10:
        font = pygame.font.SysFont("Arial", 50)
        level_surface = font.render("Level 2", True, (255, 255, 255))
        level_rect = level_surface.get_rect()
        level_rect.center = (window_width // 2, 50)
        screen.blit(level_surface, level_rect)

    if score > 30:
        font = pygame.font.SysFont("Arial", 50)
        level_surface = font.render("Level 3", True, (255, 255, 255))
        level_rect = level_surface.get_rect()
        level_rect.center = (window_width // 2, 50)
        screen.blit(level_surface, level_rect)

        # Update the display again to show the change
        pygame.display.flip()

    # Update the display
    pygame.display.update()
