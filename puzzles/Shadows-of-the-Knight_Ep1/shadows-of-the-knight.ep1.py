import sys
import math
from collections import namedtuple

class Pos(namedtuple("_Pos", ("x", "y"))):
    def add(self, a_pos):
        return Pos(*(u+v for (u, v) in zip(self, a_pos)))

class Area(namedtuple("_Area", ("top_left", "bottom_right"))):
    pass

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the building.
# h: height of the building.
DIR_XY = {
    "UL"    : Pos(-1, -1),
    "U"     : Pos(0, -1),
    "UR"    : Pos(+1, -1),
    "R"     : Pos(+1, 0),
    "DR"    : Pos(+1, +1),
    "D"     : Pos(0, +1),
    "DL"    : Pos(-1, +1),
    "L"     : Pos(-1, 0),
}

class Building:
    def __init__(self, a_w, a_h):
        self._windows = [[None for _ in range(a_w)]
                         for __ in range(a_h)      ]
    
    def at(self, a_x, a_y):
        return self._windows[a_y][a_x]


class Game:
    @staticmethod
    def read():
        ret_game = Game()
        ret_game.w, ret_game.h = [int(i) for i in input().split()]
        ret_game.n = int(input())  # maximum number of turns before game over.
        ret_game.pos= Pos(*(int(i) for i in input().split()))
        ret_game.xmin, ret_game.ymin = 0, 0
        ret_game.xmax, ret_game.ymax = ret_game.w-1, ret_game.h-1
        return ret_game

    def dump(self):
        debug(f"Game: {self.w}x{self.h}, "
              f"{self.n}, +{self.pos.x}+{self.pos.y}")
        return self

    def loop(self):
        # game loop
        while True:
            v_bomb_dir = input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
            debug(f"bomb dir: {v_bomb_dir}")

            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr, flush=True)
            v_action = self.action(v_bomb_dir)

            # the location of the next window Batman should jump to.
            print(" ".join(str(x) for x in v_action))

    def action(self, a_bomb_dir):
        if a_bomb_dir in ("R", "UR", "DR"):
            v_x2 = self.xmax + 1
            self.xmin = self.pos.x + 1
        elif a_bomb_dir in ("L", "UL", "DL"):
            v_x2 = self.xmin -1
            self.xmax = self.pos.x - 1
        else:
            v_x2 = self.pos.x
            self.xmin = self.xmax = self.pos.x

        if a_bomb_dir in ("D", "DR", "DL"):
            v_y2 = self.ymax + 1
            self.ymin = self.pos.y + 1
        elif a_bomb_dir in ("U", "UR", "UL"):
            v_y2 = self.ymin - 1
            self.ymax = self.pos.y - 1
        else:
            v_y2 = self.pos.y
            self.ymin = self.ymax = self.pos.y

        self.pos = Pos((self.pos.x+v_x2)//2, (self.pos.y+v_y2)//2)
        ret_action = self.pos
        return ret_action


def debug(a_t):
    print(a_t, file=sys.stderr)

Game.read().dump().loop()
