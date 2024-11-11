import random
from collections import deque
from mino import Mino

ROTATIONS = {
    "I": [None, 1],
    "J": [None, 0, -1, 1],
    "L": [None, 0, -1, 1],
    "O": [None],
    "S": [None, 1],
    "T": [None, 0, -1, 1],
    "Z": [None, 1],
}

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

MOVE = ((1, 0), (-1, 0), (0, 1), (0, -1))

class Bot:
    def __init__(self, board, move_time=3, think_time=3, place_time=3):
        self.board = board
        self.dx = 0
        self.dr = 0
        self.hold = 0 

        self.move_time = move_time
        self.move_timer = 0
        self.rotate_time = move_time
        self.rotate_timer = 0
        self.think_time = think_time
        self.think_timer = 0
        self.place_time = place_time
        self.place_timer = 0
        self.rotated = False
        self.moved = False 

        self.get_moves()
    
    def manual_drop(self):
        if self.hold:
            self.board.hold()
        self.board.mino.rotate(self.dr, self.board.board)
        for _ in range(abs(self.dx)):
            self.board.mino.move(sign(self.dx), 0, self.board.board)
        self.board.hard_drop(self.board.mino, self.board.board)
        self.get_moves()

    # def update2(self, dt):
    #     self.think_timer += dt
    #     if self.think_timer >= self.think_time:
    #         self.manual_drop()
    #         self.think_timer = 0

    def update(self, dt):
        self.think_timer += dt*random.randint(5, 10)/10
        if self.think_timer >= self.think_time:
            self.rotate_timer += dt*random.randint(5, 10)/10
            if self.rotate_timer >= self.rotate_time:
                if not self.rotated:
                    if self.hold:
                        self.board.hold()
                    self.board.mino.rotate(self.dr, self.board.board)
                    self.rotated = True
                
        if self.rotated:
            if self.dx:
                self.move_timer += dt*random.randint(5, 10)/10
                if self.move_timer >= self.move_time:
                    self.board.mino.move(sign(self.dx), 0, self.board.board)
                    self.move_timer = 0
                    self.dx -= sign(self.dx)
            else:
                self.moved = True

        if self.moved:
            self.place_timer += dt*random.randint(5, 10)/10
            if self.place_timer >= self.place_time:
                self.board.hard_drop(self.board.mino, self.board.board)
                self.place_timer = 0
                self.rotated = False
                self.moved = False
                self.think_timer = 0
                self.rotate_timer = 0
                self.get_moves()

    def get_moves(self):
        h = self.board.hold_mino
        if not h:
            h = self.board.next[0]
        self.hold, self.dx, self.dr, _ = self.find_moves(self.board.mino.type, h)

    def find_moves(self, type, hold_type):
        moves = []
        for i, t in enumerate([type, hold_type]):
            for dr in ROTATIONS[t]:
                for dx in range(-5, 5):
                    temp_board = [row.copy() for row in self.board.board.copy()]
                    temp_mino = Mino(t, 3, 1)
                    temp_mino.rotate(dr, temp_board)
                    for _ in range(abs(dx)): 
                        temp_mino.move(sign(dx), 0, temp_board)
                    self.drop_place(temp_mino, temp_board)
                    
                    lines = self.get_lines(temp_board)*3.1
                    gaps = -self.get_gaps(temp_board, temp_mino)*1.1
                    change_rate = -self.get_change_rate(temp_board)*1.7
                    adj = self.get_adj(temp_board, temp_mino)/20


                    # print("--------")
                    # print(lines, gaps, change_rate)
                    # for row in temp_board:
                    #     print(*row)
                        
                    score = lines+gaps+change_rate+adj
                    moves.append((i, dx, dr, score))
        
        moves.sort(key=lambda x: x[3])
        return moves[-1]

    def drop_place(self, mino, board):
        while not mino.collides(board):
            mino.y += 1
        mino.y -= 1
        for y, row in enumerate(mino.shape):
            for x, cell in enumerate(row):
                if cell:
                    board[y+mino.y][x+mino.x] = mino.type

    def get_lines(self, board):
        lines = 0
        for y, row in enumerate(board):
            if "_" not in row:
                board.pop(y)
                board.insert(0, ["_"]*10)
                lines += 1
        return lines

    def get_gaps(self, board, mino):
        gaps = 0
        for y, row in enumerate(mino.shape):
            for x, cell in enumerate(row):
                if cell:
                    for dy in range(y+mino.y, min(24, y+mino.y+6)):
                        if board[dy][x+mino.x] == "_":
                            gaps += 1
        return gaps
        
    def get_adj(self, board, mino):
        adj = 0
        for y, row in enumerate(mino.shape):
            for x, cell in enumerate(row):
                if cell:
                    for dy, dx in MOVE:
                        if 0 <= y+mino.y+dy < 24 and 0 <= x+mino.x+dx < 10:
                            if board[y+mino.y+dy][x+mino.x+dx] != "_":
                                adj += 1
        return adj

    def get_change_rate(self, board):
        diffs = []
        heights = []
        for x in range(10):
            for y in range(24):
                if board[y][x] != "_":
                    break
            heights.append(y)
        for i in range(9):
            diffs.append(abs(heights[i]-heights[i+1]))
        change_rate = sum(diffs)/10
        return change_rate