import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Paddle settings
paddle_width = 15
paddle_height = 80
paddle_speed = 0.7
player1_y = HEIGHT // 2 - paddle_height // 2
player2_y = HEIGHT // 2 - paddle_height // 2

# Ball settings
ball_radius = 10
ball_x = WIDTH // 2 - ball_radius
ball_y = HEIGHT // 2 - ball_radius
ball_dx = random.choice([-0.2, 0.2])  # Initial random direction
ball_dy = random.choice([-0.2, 0.2]) 

# Score
player1_score = 0
player2_score = 0
font = pygame.font.SysFont(None, 48)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1_y -= paddle_speed
    if keys[pygame.K_s]:
        player1_y += paddle_speed
    if keys[pygame.K_UP]:
        player2_y -= paddle_speed
    if keys[pygame.K_DOWN]:
        player2_y += paddle_speed

    # Keep paddles on screen
    player1_y = max(0, min(player1_y, HEIGHT - paddle_height)) 
    player2_y = max(0, min(player2_y, HEIGHT - paddle_height)) 

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collisions (walls)
    if ball_y <= 0 or ball_y + ball_radius * 2 >= HEIGHT:
        ball_dy *= -1

    # Ball collisions (paddles)
    if (ball_x <= paddle_width and player1_y <= ball_y + ball_radius <= player1_y + paddle_height) or \
       (ball_x + ball_radius * 2 >= WIDTH - paddle_width and player2_y <= ball_y + ball_radius <= player2_y + paddle_height):
       ball_dx *= -1 

    # Scoring
    if ball_x < 0:
        player2_score += 1
        ball_x = WIDTH // 2 - ball_radius # Reset ball
        ball_y = HEIGHT // 2 - ball_radius
        ball_dx *= -1
    elif ball_x + ball_radius * 2 > WIDTH: 
        player1_score += 1
        ball_x = WIDTH // 2 - ball_radius  # Reset ball
        ball_y = HEIGHT // 2 - ball_radius
        ball_dx *= -1

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (0, player1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (WIDTH - paddle_width, player2_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

    # Score display
    score_text = font.render(f"{player1_score}    {player2_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10)) 

    pygame.display.update()

pygame.quit()

