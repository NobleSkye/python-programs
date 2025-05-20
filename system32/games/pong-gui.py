import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED = 7
AI_SPEED = 6

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong vs AI')

# Game objects
player = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Ball speed
ball_speed_x = BALL_SPEED
ball_speed_y = BALL_SPEED

# Score
player_score = 0
ai_score = 0
font = pygame.font.Font(None, 74)

def reset_ball():
    ball.center = (WIDTH//2, HEIGHT//2)
    global ball_speed_x, ball_speed_y
    ball_speed_y = BALL_SPEED * random.choice([-1, 1])
    ball_speed_x = BALL_SPEED * random.choice([-1, 1])

def ai_movement():
    if ai.top < ball.y:
        ai.y += AI_SPEED
    if ai.bottom > ball.y:
        ai.y -= AI_SPEED
    
    # Keep AI paddle on screen
    if ai.top <= 0:
        ai.top = 0
    if ai.bottom >= HEIGHT:
        ai.bottom = HEIGHT

def draw_game():
    # Clear screen
    screen.fill(BLACK)
    
    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, ai)
    pygame.draw.ellipse(screen, WHITE, ball)
    
    # Draw center line
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    # Draw scores
    player_text = font.render(str(player_score), True, WHITE)
    ai_text = font.render(str(ai_score), True, WHITE)
    screen.blit(player_text, (WIDTH//4, 20))
    screen.blit(ai_text, (3*WIDTH//4, 20))

def main():
    global player_score, ai_score, ball_speed_x, ball_speed_y
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    # Reset game
                    player_score = 0
                    ai_score = 0
                    reset_ball()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += PADDLE_SPEED

        # AI movement
        ai_movement()

        # Ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with top and bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Ball collision with paddles
        if ball.colliderect(player) or ball.colliderect(ai):
            ball_speed_x *= -1
            # Add some randomness to ball direction after paddle hits
            ball_speed_y = random.randint(-BALL_SPEED, BALL_SPEED)

        # Scoring
        if ball.left <= 0:
            ai_score += 1
            reset_ball()
        elif ball.right >= WIDTH:
            player_score += 1
            reset_ball()

        # Draw everything
        draw_game()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
