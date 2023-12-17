import sys
import math
from collections import namedtuple

def logd(aS): print(aS, file=sys.stderr)


_Direction = namedtuple("_Direction", [
    "str", "dx", "dy", "from_"
])

class Direction(_Direction):
    def read(aS):
        if "TOP" == aS:
            return Direction.TOP
        elif "RIGHT" == aS:
            return Direction.RIGHT
        elif "BOTTOM" == aS:
            return Direction.BOTTOM
        elif "LEFT" == aS:
            return Direction.LEFT
        else:
            raise ValueError(f"Invalid direction: {aS}")

Direction.TOP       = Direction("TOP",    0,  -1, "BOTTOM")
Direction.RIGHT     = Direction("RIGHT",  +1, 0,  "LEFT")
Direction.BOTTOM    = Direction("BOTTOM", 0,  +1, "TOP")
Direction.LEFT      = Direction("LEFT",   -1, 0,  "RIGHT")


RoomInOut = namedtuple("RoomInOut", [
    "ins",  # :: [Direction]
    "outs", # :: [Direction]
])

ROOM_TYPES_TO_WAYOUT = {
    0   : [],

    1   : [RoomInOut([Direction.TOP, Direction.RIGHT, Direction.LEFT],
                     [Direction.BOTTOM])],

    2   : [RoomInOut([Direction.RIGHT, Direction.LEFT],
                     [Direction.RIGHT, Direction.LEFT])],

    3   : [RoomInOut([Direction.TOP],
                     [Direction.BOTTOM])],

    4   : [RoomInOut([Direction.TOP], [Direction.LEFT]),
           RoomInOut([Direction.RIGHT], [Direction.BOTTOM])],

    5   : [RoomInOut([Direction.TOP], [Direction.RIGHT]),
           RoomInOut([Direction.LEFT], [Direction.BOTTOM])],

    6   : [RoomInOut([Direction.RIGHT, Direction.LEFT],
                     [Direction.RIGHT, Direction.LEFT])],

    7   : [RoomInOut([Direction.TOP, Direction.RIGHT],
                     [Direction.BOTTOM])],

    8   : [RoomInOut([Direction.RIGHT, Direction.LEFT],
                     [Direction.BOTTOM])],

    9   : [RoomInOut([Direction.TOP, Direction.LEFT],
                     [Direction.BOTTOM])],

    10  : [RoomInOut([Direction.TOP],
                     [Direction.LEFT])],

    11  : [RoomInOut([Direction.TOP],
                     [Direction.RIGHT])],

    12  : [RoomInOut([Direction.RIGHT],
                     [Direction.BOTTOM])],

    13  : [RoomInOut([Direction.LEFT],
                     [Direction.BOTTOM])],
}


_IndiPos = namedtuple("_IndiPos", [
    "x", "y", "pos"
])

class IndiPos(_IndiPos):
    def read():
        v_inputs = input().split()
        return IndiPos(x    = int(v_inputs[0]),
                       y    = int(v_inputs[1]),
                       pos  = Direction.read(v_inputs[2]))

    @property
    def xy(self):
        return (self.x, self.y)

    @property
    def xy_str(self):
        return f"{self.x} {self.y}"
    
    def move(self, a_dir):
        return IndiPos(self.x+a_dir.dx, self.y+a_dir.dy, a_dir.from_)
    

_Game = namedtuple("_Game", [
    "w", "h", "lines", "ex"
])

class Game(_Game):
    def read():
        vW, vH = (int(x) for x in input().split())
        return Game(w       = vW,
                    h       = vH,
                    lines   = [ [int(x) for x in input().split()]
                                for _ in range(vH)
                              ],
                    ex      = int(input())
        )
    def room_at(self, a_x, a_y):
        return self.lines[a_y][a_x]

    def logTunnel(self):
        logd(f"## Tunnel: {self.w}x{self.h}")
        logd("\n".join(f"##  {n:2}: "+" ".join(f"{x:2}" for x in line)
                       for n, line in enumerate(self.lines)))
        return self

    def loop(self):
        while True:
            vIPos = IndiPos.read()
            logd(f"## x: {vIPos.x}, y: {vIPos.y}, pos: {vIPos.pos.str} (from: {vIPos.pos.from_})")
            print(self.action(vIPos));

    def action(self, a_ipos):
        v_room = self.room_at(a_ipos.x, a_ipos.y)
        v_inouts = self.possibleWayouts(v_room, a_ipos.pos)
        assert(a_ipos.pos in v_inouts[0].ins)
        if 1 == len(v_inouts):
            if 1 == len(v_inouts[0].outs):
                return a_ipos.move(v_inouts[0].outs[0]).xy_str
            else:
                # Exclude way in from way outs
                v_outs = list(filter(lambda x: x!=a_ipos.pos, v_inouts[0].outs))
                if 1 == len(v_outs):
                    return a_ipos.move(v_outs[0]).xy_str
                else:
                    raise Exception("To be implemented 1")
        else:
            raise Exception("To be implemented 2")


    def possibleWayouts(self, a_room, a_pos):
        """ Returns: [RoomInOut] """
        def show_poss(a_poss):
            return ", ".join(d.str for d in a_poss)

        if a_room in ROOM_TYPES_TO_WAYOUT:
            v_rooms_inouts = ROOM_TYPES_TO_WAYOUT[a_room]
            logd("# Room: {a_room}: {len(v_rooms_inouts)}")
            for i in range(len(v_rooms_inouts)):
                logd(f"#  {i}: {show_poss(v_rooms_inouts[i].ins)} -> {show_poss(v_rooms_inouts[i].outs)}")
            return list(filter(lambda x: a_pos in x.ins, v_rooms_inouts))
        else:
            raise ValueError("Not a valid room type: {a_room}")



# Main
(
    Game.read()
        .logTunnel()
        .loop()
)
