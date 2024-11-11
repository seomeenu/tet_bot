I_OFFSETS = {
    "01": [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    "10": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    "12": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    "21": [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    "23": [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    "32": [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    "30": [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    "03": [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    "00": [(0, 0)],
    "11": [(0, 0)],
    "22": [(0, 0)],
    "33": [(0, 0)],
}

JLTSZ_OFFSETS = {
    "01": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "10": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    "12": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    "21": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "23": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    "32": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "30": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "03": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    "00": [(0, 0)],
    "11": [(0, 0)],
    "22": [(0, 0)],
    "33": [(0, 0)],
}

MINO_TYPES = ["I", "O", "T", "S", "Z", "J", "L"]
MINO_COLORS = {
    "I": "#42AFE1",
    "J": "#1165B5",
    "L": "#F38927",
    "O": "#F6D03C",
    "S": "#51B84D",
    "T": "#B94BC6",
    "Z": "#EB4F65",
    "X": "#555555",
}
MINO_SHAPES = {
    "I": {
        "0": (
            (0, 0, 0, 0),
            (1, 1, 1, 1),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
        ),
        "1": (
            (0, 0, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 1, 0),
        ),
        "2": (
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 1, 1, 1),
            (0, 0, 0, 0),
        ),
        "3": (
            (0, 1, 0, 0),
            (0, 1, 0, 0),
            (0, 1, 0, 0),
            (0, 1, 0, 0),
        ),
    },
    "O": {
        "0": (
            (0, 1, 1, 0),
            (0, 1, 1, 0),
        ),
        "1": (
            (0, 1, 1, 0),
            (0, 1, 1, 0),
        ),
        "2": (
            (0, 1, 1, 0),
            (0, 1, 1, 0),
        ),
        "3": (
            (0, 1, 1, 0),
            (0, 1, 1, 0),
        ),
    },
    "T": {
        "0": (
            (0, 1, 0),
            (1, 1, 1),
            (0, 0, 0),
        ),
        "1": (
            (0, 1, 0),
            (0, 1, 1),
            (0, 1, 0),
        ),
        "2": (
            (0, 0, 0),
            (1, 1, 1),
            (0, 1, 0),
        ),
        "3": (
            (0, 1, 0),
            (1, 1, 0),
            (0, 1, 0),
        ),
    },
    "S": {
        "0": (
            (0, 1, 1),
            (1, 1, 0),
            (0, 0, 0),
        ),
        "1": (
            (0, 1, 0),
            (0, 1, 1),
            (0, 0, 1),
        ),
        "2": (
            (0, 0, 0),
            (0, 1, 1),
            (1, 1, 0),
        ),
        "3": (
            (1, 0, 0),
            (1, 1, 0),
            (0, 1, 0),
        ),
    },
    "Z": {
        "0": (
            (1, 1, 0),
            (0, 1, 1),
            (0, 0, 0),
        ),
        "1": (
            (0, 0, 1),
            (0, 1, 1),
            (0, 1, 0),
        ),
        "2": (
            (0, 0, 0),
            (1, 1, 0),
            (0, 1, 1),
        ),
        "3": (
            (0, 1, 0),
            (1, 1, 0),
            (1, 0, 0),
        ),
    },
    "J": {
        "0": (
            (1, 0, 0),
            (1, 1, 1),
            (0, 0, 0),
        ),
        "1": (
            (0, 1, 1),
            (0, 1, 0),
            (0, 1, 0),
        ),
        "2": (
            (0, 0, 0),
            (1, 1, 1),
            (0, 0, 1),
        ),
        "3": (
            (0, 1, 0),
            (0, 1, 0),
            (1, 1, 0),
        ),
    },
    "L": {
        "0": (
            (0, 0, 1),
            (1, 1, 1),
            (0, 0, 0),
        ),
        "1": (
            (0, 1, 0),
            (0, 1, 0),
            (0, 1, 1),
        ),
        "2": (
            (0, 0, 0),
            (1, 1, 1),
            (1, 0, 0),
        ),
        "3": (
            (1, 1, 0),
            (0, 1, 0),
            (0, 1, 0),
        ),
    },
}

class Mino:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.sx = x
        self.sy = y
        self.rotation = 0
        self.shape = MINO_SHAPES[type][str(self.rotation)]
    
    def update(self, dt):
        # self.sx = self.x
        # self.sy = self.y
        self.sx += (self.x-self.sx)/1.2*dt
        self.sy += (self.y-self.sy)/1.2*dt

    def move(self, dx, dy, board):
        self.x += dx
        self.y += dy
        if self.collides(board):
            self.x -= dx
            self.y -= dy

    def rotate(self, dr, board):
        # 180 spin
        if dr:
            if dr == 0:
                self.rotation = (self.rotation+2)%4
                self.shape = MINO_SHAPES[self.type][str(self.rotation)]
                if not self.collides(board):
                    return
                self.rotation = (self.rotation-2)%4
                self.shape = MINO_SHAPES[self.type][str(self.rotation)]
            else:
                prev_rotation = self.rotation 
                self.rotation = (self.rotation+dr)%4
                self.shape = MINO_SHAPES[self.type][str(self.rotation)]
                offsets = JLTSZ_OFFSETS
                if self.type == "I": offsets = I_OFFSETS
                for offset in offsets[f"{prev_rotation}{self.rotation}"]:
                    ox, oy = offset
                    self.x += ox
                    self.y -= oy
                    if not self.collides(board):
                        break
                    self.x -= ox
                    self.y += oy
                else:
                    self.rotation = (self.rotation-dr)%4
                    self.shape = MINO_SHAPES[self.type][str(self.rotation)]

    def collides(self, board):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    if 24 > self.y+y >= 0 and 10 > self.x+x >= 0:
                        if board[self.y+y][self.x+x] != "_":
                            return True
                    else:
                        return True
        return False