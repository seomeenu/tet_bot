import pygame
import sys
from board import Board
from bot import Bot
from settings import TILE_SIZE

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

board = Board()
bot = Bot(board)

while True:
    screen.fill("#333333")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # pass
            # board.handle_input(event.key)
            if event.key == pygame.K_SPACE:
                bot.manual_drop()
                
    screen.blit(board.render_board(), (screen_width//2-5*TILE_SIZE, screen_height//2-13*TILE_SIZE))
    screen.blit(board.render_next(), (screen_width//2+6*TILE_SIZE, screen_height//2-9*TILE_SIZE))
    screen.blit(board.render_hold(), (screen_width//2-10*TILE_SIZE, screen_height//2-9*TILE_SIZE))

    dt = clock.tick(120)/(1000/60)
    board.update(dt)
    # bot.update2(dt)

    pygame.display.update()