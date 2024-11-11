import pygame
from settings import CONTROLS

class Handle:
    def __init__(self):
        self.das_timer = 0
        self.arr_timer = 0
        self.sdarr_timer = 0

        self.das = 7
        self.arr = 0
        self.sdarr = 0

    def update(self, dt, board):
        keys = pygame.key.get_pressed()
        if keys[CONTROLS["left"]] or keys[CONTROLS["right"]]:
            self.das_timer += dt
        else:
            self.das_timer = 0
            self.arr_timer = 0
        if keys[CONTROLS["softdrop"]]:
            self.sdarr_timer += dt
        # print(self.das_timer, self.arr_timer, self.sdarr_timer)

        if self.das_timer >= self.das:
            self.arr_timer += dt
            if keys[CONTROLS["left"]]:
                for _ in range(10):
                    if self.arr_timer >= self.arr:
                        board.mino.move(-1, 0, board.board)
                        self.arr_timer -= self.arr*dt
                    else:
                        break
            if keys[CONTROLS["right"]]:
                for _ in range(10):
                    if self.arr_timer >= self.arr:
                        board.mino.move(1, 0, board.board)
                        self.arr_timer -= self.arr*dt
                    else:
                        break
        if keys[CONTROLS["softdrop"]]:
            for _ in range(24):
                if self.sdarr_timer >= self.sdarr:
                    board.mino.move(0, 1, board.board)
                    self.sdarr_timer -= self.sdarr*dt
                else:
                    break