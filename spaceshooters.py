import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))

# Load the player, enemy, and bullet images
player_image = pygame.image.load("Spaceship_tut.png")
enemy_image = pygame.image.load("spaceship.png")
bullet_image = pygame.image.load("spr_bullet_strip02.png")

# Set up the player object
player_rect = player_image.get_rect()
player_rect.x = (window_width - player_rect.width) // 2
player_rect.y = window_height - player_rect.height
player_speed = 1

# Set up the bullets list
bullets = []
bullet_speed = 5

# Set up the enemies list
enemies = []
enemy_speed = 1

# Set up player lives
player_lives = 5
 
# Set up score
score = 0

# Game loop
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
    if len(enemies) < 50 and random.randint(0, 100) < 1:
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
               \

    # Draw graphics
    screen.fill((0, 0, 0))  # fill the screen with black color
    screen.blit(player_image, player_rect)
    for bullet_rect in bullets:
        screen.blit(bullet_image, bullet_rect)
    for enemy_rect in enemies:
        screen.blit(enemy_image, enemy_rect)

    # Draw lives
    font = pygame.font.SysFont(None, 24)
    lives_text = font.render("Lives: " + str(player_lives), True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

      # Draw score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (window_width - score_text.get_width() - 10, 10))

    # Update the display
    pygame.display.update()


