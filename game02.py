import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake attributes
snake_block = 20
snake_speed = 15

# Initialize snake position and direction
snake_x = window_width / 2
snake_y = window_height / 2
snake_x_change = 0
snake_y_change = 0
snake_length = 1
snake_list = []

# Food attributes
food_x = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
food_y = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block

# Score
score = 0

# Font
font_style = pygame.font.SysFont(None, 50)

# Function to display score
def display_score(score):
    score_text = font_style.render("Score: " + str(score), True, BLACK)
    window.blit(score_text, [0, 0])

# Function to draw snake
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, GREEN, [x[0], x[1], snake_block, snake_block])

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_x_change = -snake_block
                snake_y_change = 0
            elif event.key == pygame.K_RIGHT:
                snake_x_change = snake_block
                snake_y_change = 0
            elif event.key == pygame.K_UP:
                snake_y_change = -snake_block
                snake_x_change = 0
            elif event.key == pygame.K_DOWN:
                snake_y_change = snake_block
                snake_x_change = 0

    # Update snake position
    snake_x += snake_x_change
    snake_y += snake_y_change

    # Check for collision with food
    if snake_x == food_x and snake_y == food_y:
        score += 1
        food_x = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
        food_y = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block
        snake_length += 1

    window.fill(WHITE)
    pygame.draw.rect(window, RED, [food_x, food_y, snake_block, snake_block])

    snake_head = []
    snake_head.append(snake_x)
    snake_head.append(snake_y)
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    for x in snake_list[:-1]:
        if x == snake_head:
            running = False

    draw_snake(snake_block, snake_list)
    display_score(score)

    pygame.display.update()

    # Set game speed
    clock.tick(snake_speed)

pygame.quit()
