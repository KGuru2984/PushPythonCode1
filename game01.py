import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 400
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Flappy Bird Game (Python)")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Bird attributes
bird_width = 50
bird_height = 50
bird_x = 50
bird_y = window_height // 2
bird_speed_y = 0
gravity = 0.5
jump_power = -10

# Pipe attributes
pipe_width = 50
pipe_gap = 150
pipe_speed = 3
pipes = []

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Function to draw bird
def draw_bird(x, y):
    pygame.draw.rect(window, BLUE, (x, y, bird_width, bird_height))

# Function to generate pipes
def generate_pipes():
    top_pipe_height = random.randint(100, window_height - pipe_gap - 100)
    bottom_pipe_height = window_height - top_pipe_height - pipe_gap
    pipes.append([window_width, 0, pipe_width, top_pipe_height])
    pipes.append([window_width, window_height - bottom_pipe_height, pipe_width, bottom_pipe_height])

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed_y = jump_power

    # Move bird
    bird_speed_y += gravity
    bird_y += bird_speed_y

    # Generate pipes
    if len(pipes) == 0 or pipes[-1][0] <= window_width - 200:
        generate_pipes()

    # Move pipes
    for pipe in pipes:
        pipe[0] -= pipe_speed

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe[0] + pipe[2] > 0]

    # Check collision with pipes
    for pipe in pipes:
        if bird_x + bird_width > pipe[0] and bird_x < pipe[0] + pipe[2]:
            if bird_y < pipe[1] + pipe[3] or bird_y + bird_height > pipe[1] + pipe_gap:
                running = False

        if pipe[0] + pipe[2] == bird_x:
            score += 1

    # Draw everything
    window.fill(WHITE)
    draw_bird(bird_x, bird_y)
    for pipe in pipes:
        pygame.draw.rect(window, BLUE, pipe)
    text = font.render("Score: " + str(score), True, BLUE)
    window.blit(text, (10, 10))
    pygame.display.flip()

    # Set game speed
    clock.tick(30)

pygame.quit()
