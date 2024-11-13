import pygame
from stuff.board import Board
from stuff.settings import TILE_SIZE

class Solo:
    def __init__(self, screen_width, screen_height):
        self.board = Board()
        self.board_x, self.board_y = screen_width//2, screen_height//2

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            self.board.handle_input(event.key)

    def update(self, screen, dt):
        screen.fill("#333333")

        screen.blit(self.board.render_board(), (self.board_x-5*TILE_SIZE, self.board_y-13*TILE_SIZE))
        screen.blit(self.board.render_next(), (self.board_x+6*TILE_SIZE, self.board_y-9*TILE_SIZE))
        screen.blit(self.board.render_garbage(), (self.board_x-6.5*TILE_SIZE, self.board_y-13*TILE_SIZE))
        screen.blit(self.board.render_hold(), (self.board_x-11*TILE_SIZE, self.board_y-9*TILE_SIZE))

        self.board.update(dt)
        self.board.handle_press(dt, pygame.key.get_pressed())