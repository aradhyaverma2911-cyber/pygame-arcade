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
font = pygame.font.Font("calibri",30)

base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/snake"))

bg = pygame.image.load(os.path.join(base,"bg.png"))
bg = pygame.transform.scale(bg,(width,height))

obstacle_img = pygame.image.load(os.path.join(base,"obstacle.png"))
obstacle_img = pygame.transform.scale(obstacle_img,(10,10))

snake = [(100,100)]
dx,dy = 10,0

grid = 10

food = (
    random.randrange(0,width,grid),
    random.randrange(0,height,grid)
)

obstacles = []
for _ in range(25):
    obstacles.append((
        random.randrange(0,width,grid),
        random.randrange(0,height,grid)
    ))

speed = 8
score = 0
started = False

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
        pygame.draw.line(screen, (*BG_SOFT, 40), (20,y), (width-20,y), 1)

    vignette = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(vignette, (0, 0, 0, 70), (0, 0, width, 20))
    pygame.draw.rect(vignette, (0, 0, 0, 70), (0, height-20, width, 20))
    screen.blit(vignette, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            started = True
            if event.key == pygame.K_UP and dy != 10:
                dx,dy = 0,-10
            if event.key == pygame.K_DOWN and dy != -10:
                dx,dy = 0,10
            if event.key == pygame.K_LEFT and dx != 10:
                dx,dy = -10,0
            if event.key == pygame.K_RIGHT and dx != -10:
                dx,dy = 10,0

    if started:
        head = (snake[0][0]+dx, snake[0][1]+dy)
        snake.insert(0, head)

        if head == food:
            score += 1
            food = (
                random.randrange(0,width,grid),
                random.randrange(0,height,grid)
            )
        else:
            snake.pop()

        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            running = False

        if head in obstacles:
            running = False

        body = snake.copy()
        body.pop(0)
        if head in body:
            running = False

    for s in snake:
        pygame.draw.rect(screen, green, (*s,10,10))

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

    text = font.render(f"Score: {score}", True, white)
    screen.blit(text,(width-120,10))

    if not started:
        msg = font.render("Press any key to start", True, white)
        screen.blit(msg,(180,180))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()