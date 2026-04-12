import pygame
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common")))

from colors import *
from constants import *

pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("calibri", 30)

base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/snake"))

bg = pygame.image.load(os.path.join(base,"bg.png"))
bg = pygame.transform.scale(bg,(width,height))

obstacle_img = pygame.image.load(os.path.join(base,"obstacle.png"))
obstacle_img = pygame.transform.scale(obstacle_img,(10,10))

snake = [(100,100)]
dx,dy = 10,0

grid = 10

obstacles = []
for _ in range(25):
    obstacles.append((
        random.randrange(0,width,grid),
        random.randrange(0,height,grid)
    ))

def place_food():
    while True:
        candidate = (
            random.randrange(0, width, grid),
            random.randrange(0, height, grid)
        )
        if candidate not in snake and candidate not in obstacles:
            return candidate

food = place_food()

speed = 8
score = 0
started = False
game_over = False

running = True
while running:
    screen.blit(bg,(0,0))

    panel = pygame.Surface((width-40, height-40), pygame.SRCALPHA)
    panel.fill((*BG_PANEL, 190))
    pygame.draw.rect(panel, (*BG_PANEL_LIGHT, 220), panel.get_rect(), border_radius=16, width=2)
    screen.blit(panel, (20,20))

    for x in range(20, width-20, grid):
        pygame.draw.line(screen, (*BG_SOFT, 40), (x,20), (x,height-20), 1)
    for y in range(20, height-20, grid):
        pygame.draw.line(screen, (*BG_SOFT, 40), (20,y), (width-20,y),1)
    for o in obstacles:
        screen.blit(obstacle_img,o)

    food_center = (food[0] + 5, food[1] + 5)
    pygame.draw.circle(screen, FOOD_ACCENT, food_center, 5)
    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (food_center[0] - 1, food_center[1] - 1),
        2
    )

    for segment in snake[:-1]:
        pygame.draw.rect(screen, SNAKE_BODY, pygame.Rect(segment[0], segment[1], grid, grid), border_radius=4)
    pygame.draw.rect(screen, SNAKE_HEAD, pygame.Rect(snake[0][0], snake[0][1], grid, grid), border_radius=4)

    text = font.render(f"Score: {score}", True, white)
    screen.blit(text,(width-120,10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -grid
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, grid
            elif event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -grid, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = grid, 0
            if not started:
                started = True
            if game_over and event.key == pygame.K_RETURN:
                snake = [(100, 100)]
                dx, dy = 10, 0
                score = 0
                started = False
                game_over = False
                food = place_food()

    if started and not game_over:
        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = place_food()
        else:
            snake.pop()

        if (
            new_head[0] < 20 or new_head[0] >= width-20 or
            new_head[1] < 20 or new_head[1] >= height-20 or
            new_head in snake[1:] or
            new_head in obstacles
        ):
            game_over = True

    if game_over:
        msg = font.render("Game over! Press Enter to restart", True, white)
        screen.blit(msg,(50,200))
    elif not started:
        msg = font.render("Press any key to start", True, white)
        screen.blit(msg,(180,180))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
