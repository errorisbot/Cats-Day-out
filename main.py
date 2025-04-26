import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
TARGET_WIDTH, TARGET_HEIGHT = 1200, 720
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)  # New color for coins

# Calculate the ratio for resizing
WINDOW_RATIO = TARGET_WIDTH / TARGET_HEIGHT

# Load images
background_image = pygame.image.load("Nightsky.jpg")
background_image = pygame.transform.scale(background_image, (TARGET_WIDTH, TARGET_HEIGHT))

player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (100, 70))

obstacle_image = pygame.image.load("Obstacle.png")
obstacle_image = pygame.transform.scale(obstacle_image, (60, 60))

coin_image = pygame.image.load("coin.png")  # Replace "coin.png" with your actual coin image
coin_image = pygame.transform.scale(coin_image, (60, 60))

logo_image = pygame.image.load("game_logo(1).png")  # Replace "your_logo.png" with your actual logo image
logo_image = pygame.transform.scale(logo_image, (600, 400))

# Load sounds
jump_sound = pygame.mixer.Sound("jump_sound.mp3")
coin_sound = pygame.mixer.Sound("coin_sound.mp3")  # Add a sound for collecting coins

# Load background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.5)  # Adjust the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music indefinitely (-1)

# Player variables
player_pos = [50, TARGET_HEIGHT - 75]
player_speed = 10
player_jump = False
jump_count = 10

# Obstacle variables
obstacle_speed = 8
obstacles = []
obstacle_spawn_delay = 50
current_obstacle_delay = 0

# Coin variables
coin_speed = 5
coins = []
coin_spawn_delay = 20  # Halved the coin spawn delay for increased rate
current_coin_delay = 0

# Score variables
score = 0
score_speed = 1.75

# Timer variables
elapsed_seconds = 0

# Graphics Control
controls_image = pygame.image.load("controls.png")
controls_image = pygame.transform.scale(controls_image, (130, 70))

# Graphics Developer
developer_image = pygame.image.load("developer.png")
developer_image = pygame.transform.scale(developer_image, (150, 65))

# Function to display text
def draw_text(text, x, y, color=WHITE):
    font = pygame.font.SysFont(None, 36, bold=False)
    text_surface = font.render(text, True, color, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Function to check collision
def is_collision(player_pos, other_pos, size=30):
    return pygame.Rect(player_pos, (90, 60)).colliderect(pygame.Rect(other_pos, (size, size)))

# Function to display game over pop-up
def game_over_popup():
    popup_rect = pygame.Rect(TARGET_WIDTH // 4, TARGET_HEIGHT // 4, TARGET_WIDTH // 2, TARGET_HEIGHT // 2)
    pygame.draw.rect(screen, RED, popup_rect)

    draw_text("Game Over! :(", TARGET_WIDTH // 2 - 85, TARGET_HEIGHT // 4 + 80)
    draw_text(f"Your Score: {int(score)}", TARGET_WIDTH // 2 - 85, TARGET_HEIGHT // 4 + 120)

    retry_button_rect = pygame.Rect(TARGET_WIDTH // 2 - 75, TARGET_HEIGHT // 2, 150, 50)
    pygame.draw.rect(screen, GREEN, retry_button_rect)
    draw_text("Click to Retry", TARGET_WIDTH // 2 - 80, TARGET_HEIGHT // 2 + 17)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if retry_button_rect.collidepoint(mouse_x, mouse_y):
        if pygame.mouse.get_pressed()[0]:
            return True  # Retry button clicked

    return False

# Initialize screen
screen = pygame.display.set_mode((TARGET_WIDTH, TARGET_HEIGHT), RESIZABLE)
pygame.display.set_caption("Cats Day Out")

# Game start timer
logo_timer = 120  # 3 seconds at 60 FPS

# Game loop
clock = pygame.time.Clock()

running = True
game_active = False
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == VIDEORESIZE:
            # Adjust the window size while maintaining the ratio
            new_width = max(event.w, int(event.h * WINDOW_RATIO))
            new_height = max(event.h, int(event.w / WINDOW_RATIO))
            screen = pygame.display.set_mode((new_width, new_height), RESIZABLE)

        if not game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_active = True

        if game_active and not game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not player_jump:
                player_jump = True
                jump_sound.play()  # Play jump sound effect

    if not game_active:
        if logo_timer > 0:
            screen.blit(logo_image, (TARGET_WIDTH // 2 - 300, TARGET_HEIGHT // 2 - 200))
            logo_timer -= 1
        else:
            game_active = True

    if game_active:
        if not game_over:
            # Move player
            keys = pygame.key.get_pressed()
            player_pos[0] += keys[pygame.K_RIGHT] * player_speed
            player_pos[0] -= keys[pygame.K_LEFT] * player_speed

            # Jumping mechanic
            if player_jump:
                if jump_count >= -10:
                    neg = 1
                    if jump_count < 0:
                        neg = -1
                    player_pos[1] -= (jump_count ** 2) * 0.5 * neg
                    jump_count -= 1
                else:
                    player_jump = False
                    jump_count = 10

            # Move obstacles
            for obstacle in obstacles:
                obstacle[0] -= obstacle_speed

                if is_collision(player_pos, obstacle):
                    game_over = True

                # Remove obstacles that are off-screen
                if obstacle[0] < -30:
                    obstacles.remove(obstacle)

            # Move coins
            for coin in coins:
                coin[1] += coin_speed

                if is_collision(player_pos, coin, size=30):
                    coin_sound.play()  # Play coin collection sound
                    score += 1250
                    coins.remove(coin)

                # Remove coins that are off-screen
                if coin[1] > TARGET_HEIGHT:
                    coins.remove(coin)

            # Generate new obstacles and coins with a delay
            if current_obstacle_delay <= 0 and len(obstacles) < 2:
                obstacles.append([TARGET_WIDTH, TARGET_HEIGHT - 80])
                current_obstacle_delay = obstacle_spawn_delay

            if current_coin_delay <= 0 and len(coins) < 1:  # Adjust the number of coins as needed
                coins.append([random.randint(50, TARGET_WIDTH - 50), 0])
                current_coin_delay = coin_spawn_delay

            current_obstacle_delay -= 1
            current_coin_delay -= 1

            # Update the timer and score
            elapsed_seconds += 1 / FPS
            score += score_speed / FPS

        # Draw background
        screen.blit(background_image, (0, 0))

        # Draw ground
        pygame.draw.rect(screen, BLACK, [0, TARGET_HEIGHT - 50, TARGET_WIDTH, 50])

        # Draw player
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        # Draw obstacles
        for obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

        # Draw coins
        for coin in coins:
            screen.blit(coin_image, (coin[0], coin[1]))

        # Draw graphics control at top right
        screen.blit(controls_image, (TARGET_WIDTH - 670, 10))

        # Draw graphics developer at bottom right
        screen.blit(developer_image, (TARGET_WIDTH - 160, TARGET_HEIGHT - 60))

        # Game over screen
        if game_over:
            if game_over_popup():
                # Reset game variables
                player_pos = [50, TARGET_HEIGHT - 75]
                player_jump = False
                jump_count = 10
                obstacles = []
                coins = []
                score = 0
                elapsed_seconds = 0
                game_over = False

        # Draw score
        draw_text(f"Score: {int(score)}", 10, 10, YELLOW)

    pygame.display.flip()
    clock.tick(FPS)

pygame.mixer.music.stop()  # Stop the background music when exiting the game
pygame.quit()
sys.exit()