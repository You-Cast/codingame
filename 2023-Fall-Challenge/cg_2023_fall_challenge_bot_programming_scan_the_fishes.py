from sys import stderr as sys_stderr
#import math
from collections import namedtuple

MIN_MOVE    = 0
MAX_MOVE    = 600
SINK_DIST   = 300
MAX_VIS_RAD     = 800
MAX_VISH_RAD    = 2000
WIDTH   = 10000
MIN_X   = 0
MAX_X   = WIDTH-1
HEIGHT  = 10000
MIN_Y   = 0
MAX_Y   = HEIGHT-1
DRONE_COUNT = 1



def main():
    (
        Game.read(input)
            .dump()
            .loop(input)
    )


def drone_strategy_screensaver(self, a_game, a_turn, a_last_action):
    def calc_xy_target(a_ctxt, a_label=""):
        v_x_target = self.x + MAX_MOVE*a_ctxt.dirx
        v_y_target = self.y + MAX_MOVE*a_ctxt.diry
        v_x_target = min(MAX_X, v_x_target)
        v_x_target = max(MIN_X, v_x_target)
        v_y_target = min(MAX_Y, v_y_target)
        v_y_target = max(MIN_Y, v_y_target)
        debug(f">>>> new target: {(a_label+':') if a_label else ''} "
              f"+{v_x_target}+{v_y_target}")
        return (v_x_target, v_y_target)

    v_label = ""
    v_light = True if self.battery>10 else False
    v_ctxt  = None
    if not a_last_action:
        # Initialisation
        v_label = "init: 90s screensaver"
        if self.x < WIDTH//2:
            v_ctxt = ActionContext.new(-1, +1)
        else:
            v_ctxt = ActionContext.new(+1, +1)


    else:
        if a_last_action.is_wait:
            assert(False)
            # Was waiting, then go to farest border
            if self.x < WIDTH//2:
                # go toward right border
                v_xy_target = (MAX_X, self.y)
                debug(f"Last action was wait: +{self.x}+{self.y} => moving right: {v_xy_target}")
                return Action.move(*v_xy_target)
            else:
                # go toward right border
                v_xy_target = (MIN_X, self.y) 
                debug(f"Last action was wait: +{self.x}+{self.y} => moving left: {v_xy_target}")
                return Action.move(*v_xy_target)
        
        else:
            assert(a_last_action.ctxt.dirx)
            assert(a_last_action.ctxt.diry)
            v_ctxt = a_last_action.ctxt
            if v_ctxt.dirx==-1 and self.x<MAX_VIS_RAD:
                debug(">> was moving left and reached left border => moving right")
                v_ctxt = v_ctxt.update_dirx(+1)

            elif v_ctxt.dirx==+1 and self.x+MAX_VIS_RAD > WIDTH:
                debug(">> was moving right and reached right border => moving left")
                v_ctxt = v_ctxt.update_dirx(-1)
            
            if -1==v_ctxt.diry and self.y < HEIGHT//3: #MAX_VIS_RAD:
                debug(">> was moving up and reached top => moving down")
                v_ctxt = v_ctxt.update_diry(+1)
            
            elif  +1==v_ctxt.diry and self.y+MAX_VIS_RAD > MAX_Y:
                debug(">> was moving down and reached bottom => moving up")
                v_ctxt = v_ctxt.update_diry(-1)

    return Action.move(*calc_xy_target(v_ctxt, v_label), a_ctxt=v_ctxt, a_light=v_light) 



_DroneActor = namedtuple("_DroneActor", [
    "status",
    "last_actions",
    "strategies"
])
class DroneActor(_DroneActor):
    def next_action(self, a_g, a_turn):
        debug("Thinking of next action: "
              f"  turn: {a_turn.num}\n  @+{self.x}+{self.y}, "
              f"E: {self.emergency}, B:{self.battery}")
        ret_action = self.strategies[-1](self, a_g, a_turn, self.last_action)
        self.last_actions.append(ret_action)
        return ret_action

    def update_status(self, a_status):
        return DroneActor(a_status, self.last_actions, self.strategies)

    @property
    def last_action(self): return self.last_actions[-1]

    @property
    def x(self): return self.status.x

    @property
    def y(self): return self.status.y

    @property
    def emergency(self): return self.status.emergency

    @property
    def battery(self): return self.status.battery


##== Drone
_Drone = namedtuple("Drone", [
    "id", "x", "y", "emergency", "battery",
])
class Drone(_Drone):
    @staticmethod
    def read(a_f_in):
        return Drone(*(int(x) for x in a_f_in().split()))

    def __str__(self):
        return f"id={self.id}, x={self.x}, y={self.y}"


##== Game
_Game = namedtuple("_Game", [
    "fish_count",
    "fishes"
])

class Game(_Game):
    @staticmethod
    def read(a_f_input):
        return Game(fish_count = sto(int(a_f_input())),
                    fishes     = [Fish.read(a_f_input)
                                   for _ in range(rcl())])

    def dump(self):
        debug(f"## Game: {self.fish_count} fishes")
        debug("\n".join(f"##  {n:2}: {fish}"
                        for n, fish in enumerate(self.fishes)))
        return self

    """ == Game loop == """
    def loop(self, a_f_input):
        v_turn_no = 0
        v_drone_actors = [DroneActor(None, [None], [drone_strategy_screensaver])
                          for _ in range(DRONE_COUNT)]
        while True:
            v_turn_no += 1
            v_turn = GameTurn.read(a_f_input, v_turn_no)
            for i_drone, i_drone_actor in zip(v_turn.my_drones, v_drone_actors):
                print(i_drone_actor.update_status(i_drone).next_action(self, v_turn))


##== GameTurn
_GameTurn = namedtuple("_GameTurn", [
    "num",
    "my_score",
    "foe_score",
    "my_scan_fishes",    # :: [fish-id]
    "foe_scan_fishes",   # :: [fish-id]  
    "my_drones",
    "foe_drones",
    "drone_scans",
    "visible_fishes",
    "radar_blips"
])

class GameTurn(_GameTurn):
    @property
    def my_scan_count(self): return len(self.my_scan_fishes)
    @property
    def foe_scan_count(self): return len(self.foe_scan_fishes)
    @property
    def my_drone_count(self): return len(self.my_drones)
    @property
    def foe_drone_count(self): return len(self.foe_drones)
    @property
    def drone_scan_count(self): return len(self.drone_scans)
    @property
    def visible_fish_count(self): return len(self.visible_fishes)
    @property
    def radar_blip_count(self): return len(self.radar_blips)

    @staticmethod
    def read(a_f_in, a_turn_num):
        readn = lambda: int(a_f_in())
        return GameTurn(a_turn_num,
                        my_score        = readn(),
                        foe_score       = readn(),
                        my_scan_fishes  = [readn() for _ in range(readn())],
                        foe_scan_fishes = [readn() for _ in range(readn())],
                        my_drones       = [Drone.read(a_f_in) for _ in range(readn())],
                        foe_drones      = [Drone.read(a_f_in) for _ in range(readn())],
                        drone_scans     = [ScanResult.read(a_f_in) for _ in range(readn())],
                        visible_fishes  = [VisibleFish.read(a_f_in) for _ in range(readn())],
                        radar_blips     = [RadarBlip.read(a_f_in) for _ in range(readn())],
        )

    def dump(self):
        debug(f"## GameTurn: {self.num}")
        debug(f"##   score: me: {self.my_score}, foe: {self.foe_score}")
        debug(f"##   my scans : {self.my_scan_count} : {self.my_scan_fishes}")
        debug(f"##   foe scans: {self.foe_scan_count}: {self.foe_scan_fishes}")
        debug(f"##   my drones: {self.my_drone_count}")
        debug(f"##     {self.my_drones}")
        debug(f"##   foe drones: {self.foe_drone_count}")
        debug(f"##     {self.foe_drones}")
        debug(f"##   drone scans: {self.drone_scan_count}")
        debug(f"##     results: {self.drone_scans}")
        debug(f"##   visible fishes: {self.visible_fish_count}")
        debug(f"##     {self.visible_fishes}")
        debug(f"##   radar blips: {self.radar_blip_count}")
        debug(f"##     {self.radar_blips}")
        return self


##== Creatures
_Fish = namedtuple("_Fish", [
    "id", "color", "type"
])

class Fish(_Fish):
    @staticmethod
    def read(a_f_in):
        return Fish(*(int (x) for x in a_f_in().split()))


##== Scan result
_ScanResult = namedtuple("_ScanResult", [
    "drone_id", "creature_id"
])
class ScanResult(_ScanResult):
    @staticmethod
    def read(a_f_in):
        return ScanResult(*(int(x) for x in a_f_in().split()))


##== Visible fish
_VisibleFish = namedtuple("_VisibleFish", [
    "id", "x", "y", "vx", "vy"
])

class VisibleFish(_VisibleFish):
    def read(a_f_in):
        return VisibleFish(*(x for x in a_f_in().split()))


##== Radar blip
_RadarBlip = namedtuple("_RadarBlip", [
    "drone_id", "creature_id", "radar"
])

class RadarBlip(_RadarBlip):
    @staticmethod
    def read(a_f_in):
        v_inputs = a_f_in().split()
        return RadarBlip(drone_id      = int(v_inputs[0]),
                         creature_id   = int(v_inputs[1]),
                         radar         = v_inputs[2])

##== Sto/rcl
class Last:
    _last = None
       
def rcl():
    return Last._last
    
def sto(a):
    Last._last = a
    return rcl()


##== Action
_ActionContext = namedtuple("_ActionContext", [
    "dirx", "diry", "x_min", "y_min", "x_max", "y_max"
])

class ActionContext(_ActionContext):
    new = lambda a_dirx, a_diry: ActionContext(a_dirx, a_diry, MIN_X, MIN_Y, MAX_X, MAX_Y)
    update_dirx = lambda self, a_dx: ActionContext.new(a_dx, self.diry)
    update_diry = lambda self, a_dy: ActionContext.new(self.dirx, a_dy)


_Action = namedtuple("_Action", [
    "kind", "light", "x", "y", "ctxt"
])

class Action(_Action):
    MOVE = "MOVE"
    WAIT = "WAIT"

    @staticmethod
    def wait(*, a_ctxt=None, a_light=False):
        return Action(Action.WAIT, None, None, a_light, a_ctxt)
    
    @staticmethod
    def move(a_x, a_y, *, a_ctxt=None, a_light=False):
        return Action(Action.MOVE, a_light, a_x, a_y, a_ctxt)

    @property
    def is_wait(self): return Action.WAIT == self.kind
    
    @property
    def is_move(self): return Action.MOVE == self.kind

    def __str__(self):
        if self.is_wait:
            return f"WAIT {1 if self.light else 0}"
        else:
            return f"MOVE {self.x} {self.y} {1 if self.light else 0}"


def debug(a_s, a_flush=False):
    print(a_s, file=sys_stderr, flush=a_flush)




main() if "__main__" == __name__ else None
