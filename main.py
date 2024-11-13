import pygame
import sys
# from scenes.solo import Solo
from scenes.battle import Battle

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

game = Battle(screen_width, screen_height)

while True:
    screen.fill("#333333")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            game.event(event)

    dt = clock.tick(120)/(1000/60)
    game.update(screen, dt)

    pygame.display.update()