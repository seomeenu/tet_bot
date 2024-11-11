import pygame
import random
from mino import MINO_TYPES, MINO_COLORS, MINO_SHAPES, Mino
from settings import TILE_SIZE, CONTROLS
from handle import Handle

class Board:
    def __init__(self):
        self.board = [["_"]*10 for _ in range(24)]
        self.next = []
        self.hold_mino = None
        self.can_hold = True
        self.mino = self.summon_mino()

        self.board_surface = pygame.Surface((10*TILE_SIZE+1, 24*TILE_SIZE+1))
        self.next_surface = pygame.Surface((4*TILE_SIZE, 15*TILE_SIZE))
        self.hold_surface = pygame.Surface((4*TILE_SIZE, 4*TILE_SIZE))
        self.board_surface.set_colorkey("#000000")
        self.next_surface.set_colorkey("#000000")
        self.hold_surface.set_colorkey("#000000")

        self.handle = Handle()
        
    def handle_input(self, key):
        if key == CONTROLS["left"]:
            self.mino.move(-1, 0, self.board)
            self.handle.das_timer = 0
        if key == CONTROLS["right"]:
            self.mino.move(1, 0, self.board)
            self.handle.das_timer = 0
        if key == CONTROLS["rotate_cw"]:
            self.mino.rotate(1, self.board)
        if key == CONTROLS["rotate_ccw"]:
            self.mino.rotate(-1, self.board)
        if key == CONTROLS["rotate_180"]:
            self.mino.rotate(0, self.board)
        if key == CONTROLS["softdrop"]:
            self.mino.move(0, 1, self.board)
            self.handle.sdarr_timer = 0
        if key == CONTROLS["harddrop"]:
            self.hard_drop(self.mino, self.board)
        if key == CONTROLS["hold"]:
            self.hold()
        if key == CONTROLS["reset"]:
            self.reset()

    def reset(self):
        self.board = [["_"]*10 for _ in range(24)]
        self.next = []
        self.hold_mino = None 
        self.can_hold = True
        self.mino = self.summon_mino()

    def hold(self):
        if self.can_hold:
            if self.hold_mino:
                temp = self.hold_mino
                self.hold_mino = self.mino.type
                self.mino = self.summon_mino(temp)
            else:
                self.hold_mino = self.mino.type
                self.mino = self.summon_mino()

            self.can_hold = False

    def hard_drop(self, mino, board):
        while not mino.collides(board):
            mino.y += 1
        mino.y -= 1
        self.place(mino, board)

    def place(self, mino, board):
        for y, row in enumerate(mino.shape):
            for x, cell in enumerate(row):
                if cell:
                    board[y+mino.y][x+mino.x] = mino.type
        self.clear_lines()
        self.mino = self.summon_mino()
        self.can_hold = True
        
    def make_bag(self):
        bag = MINO_TYPES.copy()
        # bag = ["L"]*7
        random.shuffle(bag)
        return bag
            
    def summon_mino(self, type=None):
        if len(self.next) <= 5:
            self.next += self.make_bag()
        if not type:
            type = self.next.pop(0)
        return Mino(type, 3, 1)
    
    def clear_lines(self):
        lines = 0
        for y, row in enumerate(self.board):
            if "_" not in row:
                self.board.pop(y)
                self.board.insert(0, ["_"]*10)
                lines += 1
        return lines
    
    def update(self, dt):
        self.mino.update(dt)
        self.handle.update(dt, self)

    def render_board(self):
        self.board_surface.fill("#000000")

        for x in range(10+1):
            pygame.draw.line(self.board_surface, MINO_COLORS["X"], (x*TILE_SIZE, 4*TILE_SIZE), (x*TILE_SIZE, 24*TILE_SIZE))
        for y in range(4, 24+1):
            pygame.draw.line(self.board_surface, MINO_COLORS["X"], (0, y*TILE_SIZE), (10*TILE_SIZE, y*TILE_SIZE))
                    
        prev_y = self.mino.y
        for _ in range(24):
            self.mino.move(0, 1, self.board)
        for y, row in enumerate(self.mino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.board_surface, MINO_COLORS["X"], (round((x+self.mino.x)*TILE_SIZE), round((y+self.mino.y)*TILE_SIZE), TILE_SIZE, TILE_SIZE))
        self.mino.y = prev_y
        for y, row in enumerate(self.mino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.board_surface, MINO_COLORS[self.mino.type], (round((x+self.mino.sx)*TILE_SIZE), round((y+self.mino.sy)*TILE_SIZE), TILE_SIZE, TILE_SIZE))
    
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell != "_":
                    pygame.draw.rect(self.board_surface, MINO_COLORS[cell], (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return self.board_surface
    
    def render_next(self):
        self.next_surface.fill("#000000")
        for i, type in enumerate(self.next[:5]):
            ofs = 0
            if type == "I": ofs = -0.5
            for y, row in enumerate(MINO_SHAPES[type]["0"]):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.next_surface, MINO_COLORS[type], (x*TILE_SIZE, (y+i*3+ofs)*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return self.next_surface

    def render_hold(self):
        self.hold_surface.fill("#000000")
        if self.hold_mino:
            color = MINO_COLORS["X"]
            if self.can_hold:
                color = MINO_COLORS[self.hold_mino]
            ofs = 0
            if self.hold_mino == "I": ofs = -0.5
            for y, row in enumerate(MINO_SHAPES[self.hold_mino]["0"]):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.hold_surface, color, (x*TILE_SIZE, (y+ofs)*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return self.hold_surface