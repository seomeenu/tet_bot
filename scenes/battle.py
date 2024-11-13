# import pygame
from stuff.board import Board
from stuff.bot import Bot
from stuff.settings import TILE_SIZE

class Battle:
    def __init__(self, screen_width, screen_height):
        self.board_1 = Board()
        self.board_1_x, self.board_1_y = screen_width//4+TILE_SIZE*2, screen_height//2
        self.bot_1 = Bot(self.board_1, 5, 5, 5)

        self.board_2 = Board()
        self.board_2_x, self.board_2_y = 3*screen_width//4-TILE_SIZE*2, screen_height//2
        self.bot_2 = Bot(self.board_2, 5, 5, 5)

        self.board_1.opponent = self.board_2
        self.board_2.opponent = self.board_1

    def event(self, event):
        pass
        # if event.type == pygame.KEYDOWN:
        #     self.board.handle_input(event.key)

    def update(self, screen, dt):
        screen.fill("#333333")

        screen.blit(self.board_1.render_board(), (self.board_1_x-5*TILE_SIZE, self.board_1_y-13*TILE_SIZE))
        screen.blit(self.board_1.render_next(), (self.board_1_x+6*TILE_SIZE, self.board_1_y-9*TILE_SIZE))
        screen.blit(self.board_1.render_garbage(), (self.board_1_x-6.5*TILE_SIZE, self.board_1_y-13*TILE_SIZE))
        screen.blit(self.board_1.render_hold(), (self.board_1_x-11*TILE_SIZE, self.board_1_y-9*TILE_SIZE))

        screen.blit(self.board_2.render_board(), (self.board_2_x-5*TILE_SIZE, self.board_2_y-13*TILE_SIZE))
        screen.blit(self.board_2.render_next(), (self.board_2_x+6*TILE_SIZE, self.board_2_y-9*TILE_SIZE))
        screen.blit(self.board_2.render_garbage(), (self.board_2_x-6.5*TILE_SIZE, self.board_2_y-13*TILE_SIZE))
        screen.blit(self.board_2.render_hold(), (self.board_2_x-11*TILE_SIZE, self.board_2_y-9*TILE_SIZE))

        self.board_1.update(dt)
        self.bot_1.update(dt)
        
        self.board_2.update(dt)
        self.bot_2.update(dt)