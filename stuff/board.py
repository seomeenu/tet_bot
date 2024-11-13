import pygame
import random
import time
from stuff.mino import MINO_TYPES, MINO_COLORS, MINO_SHAPES, Mino
from stuff.settings import TILE_SIZE, CONTROLS
from stuff.settings import CONTROLS

GARBAGE = {
    0: 0,
    1: 0,
    2: 1,
    3: 2,
    4: 4,
}
T_SPIN_GARBAGE = {
    0: 0,
    1: 2,
    2: 4,
    3: 6,
}

class Board:
    def __init__(self):
        self.random = random.Random(round(time.time()))
        
        self.board = [["_"]*10 for _ in range(24)]
        self.next = []
        self.hold_mino = None
        self.can_hold = True
        self.mino = self.summon_mino()

        self.board_surface = pygame.Surface((10*TILE_SIZE+1, 24*TILE_SIZE+1))
        self.next_surface = pygame.Surface((4*TILE_SIZE, 15*TILE_SIZE))
        self.hold_surface = pygame.Surface((4*TILE_SIZE, 4*TILE_SIZE))
        self.garbage_surface = pygame.Surface((1*TILE_SIZE, 24*TILE_SIZE))
        self.board_surface.set_colorkey("#000000")
        self.next_surface.set_colorkey("#000000")
        self.hold_surface.set_colorkey("#000000")
        self.garbage_surface.set_colorkey("#000000")

        self.das_timer = 0
        self.arr_timer = 0
        self.sdarr_timer = 0
        self.das = 7
        self.arr = 0
        self.sdarr = 0

        self.opponent = None
        self.garbage = 0
        self.sending_garbages = []

    def handle_press(self, dt, keys):
        if keys[CONTROLS["left"]] or keys[CONTROLS["right"]]:
            self.das_timer += dt
        else:
            self.das_timer = 0
            self.arr_timer = 0
        if keys[CONTROLS["softdrop"]]:
            self.sdarr_timer += dt

        if self.das_timer >= self.das:
            self.arr_timer += dt
            if keys[CONTROLS["left"]]:
                for _ in range(10):
                    if self.arr_timer >= self.arr:
                        self.mino.move(-1, 0, self.board)
                        self.arr_timer -= self.arr*dt
                    else:
                        break
            if keys[CONTROLS["right"]]:
                for _ in range(10):
                    if self.arr_timer >= self.arr:
                        self.mino.move(1, 0, self.board)
                        self.arr_timer -= self.arr*dt
                    else:
                        break
        if keys[CONTROLS["softdrop"]]:
            for _ in range(24):
                if self.sdarr_timer >= self.sdarr:
                    self.mino.move(0, 1, self.board)
                    self.sdarr_timer -= self.sdarr*dt
                else:
                    break

    def handle_input(self, key):
        if key == CONTROLS["left"]:
            self.mino.move(-1, 0, self.board)
            self.das_timer = 0
        if key == CONTROLS["right"]:
            self.mino.move(1, 0, self.board)
            self.das_timer = 0
        if key == CONTROLS["rotate_cw"]:
            self.mino.rotate(1, self.board)
        if key == CONTROLS["rotate_ccw"]:
            self.mino.rotate(-1, self.board)
        if key == CONTROLS["rotate_180"]:
            self.mino.rotate(0, self.board)
        if key == CONTROLS["softdrop"]:
            self.mino.move(0, 1, self.board)
            self.sdarr_timer = 0
        if key == CONTROLS["harddrop"]:
            self.hard_drop(self.mino, self.board)
        if key == CONTROLS["hold"]:
            self.hold()
        # if key == CONTROLS["reset"]:
        #     self.reset()

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
        lines = self.clear_lines()
        self.calc_garbage(mino, lines)
        self.receive_garbage()
        self.mino = self.summon_mino()
        self.can_hold = True

    def receive_garbage(self):
        hole_pos = self.random.randint(0, 9)
        garbage_line = ["X"]*10
        garbage_line[hole_pos] = "_"
        for _ in range(self.garbage):
            self.board.pop(0)
            self.board.append(garbage_line.copy())
        self.garbage = 0

    def calc_garbage(self, mino, lines):
        garbage = 0
        if mino.type == "T" and mino.rotated:
            garbage = T_SPIN_GARBAGE[lines]
        else:
            garbage = GARBAGE[lines]
        pc = True
        for y in range(24):
            for x in range(10):
                if self.board[y][x] == "_":
                    pc = False
                    break
        if pc:
            garbage = 10
        self.garbage -= garbage
        if self.garbage < 0:
            self.sending_garbages.append([30, abs(self.garbage)])
            self.garbage = 0
            
    def clear_lines(self):
        lines = 0
        for y, row in enumerate(self.board):
            if "_" not in row:
                self.board.pop(y)
                self.board.insert(0, ["_"]*10)
                lines += 1
        return lines
    
    def make_bag(self):
        bag = MINO_TYPES.copy()
        self.random.shuffle(bag)
        return bag
            
    def summon_mino(self, type=None):
        if len(self.next) <= 5:
            self.next += self.make_bag()
        if not type:
            type = self.next.pop(0)
        return Mino(type, 3, 1)
    
    def update(self, dt):
        self.mino.update(dt)
        if self.opponent:
            for sending_garbage in self.sending_garbages.copy():
                sending_garbage[0] -= dt
                if sending_garbage[0] <= 0:
                    self.opponent.garbage += sending_garbage[1]
                    self.sending_garbages.remove(sending_garbage)

    def render_board(self):
        self.board_surface.fill("#000000")

        for x in range(10+1):
            pygame.draw.line(self.board_surface, MINO_COLORS["X"], (x*TILE_SIZE, 4*TILE_SIZE), (x*TILE_SIZE, 24*TILE_SIZE))
        for y in range(4, 24+1):
            pygame.draw.line(self.board_surface, MINO_COLORS["X"], (0, y*TILE_SIZE), (10*TILE_SIZE, y*TILE_SIZE))
                    
        # shadow 
        prev_y = self.mino.y
        for _ in range(24):
            self.mino.move(0, 1, self.board)
        for y, row in enumerate(self.mino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.board_surface, MINO_COLORS["H"], (round((x+self.mino.x)*TILE_SIZE), round((y+self.mino.y)*TILE_SIZE), TILE_SIZE, TILE_SIZE))
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

    def render_garbage(self):
        self.garbage_surface.fill("#000000")

        pygame.draw.rect(self.garbage_surface, MINO_COLORS["Z"], (0, (24-self.garbage)*TILE_SIZE, TILE_SIZE, self.garbage*TILE_SIZE))
        
        return self.garbage_surface

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