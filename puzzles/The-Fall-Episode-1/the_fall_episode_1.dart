import 'dart:io';
import 'dart:math';


String readLineSync() {
  String? s = stdin.readLineSync();
  return s == null ? '' : s;
}

void logd(String aStr, [bool aNextLine=true]) {
  stderr.write(aStr+(aNextLine ? "\n" : ""));
}

class Direction {
  static final top    = Direction("TOP",    0,  -1);
  static final right  = Direction("RIGHT",  1, 0);
  static final bottom = Direction("BOTTOM", 0,  1);
  static final left   = Direction("LEFT",   -1, 0);
  
  Direction(this._str, this._dx, this._dy);

  String  get str => _str;
  int     get dx  => _dx;
  int     get dy  => _dy;

  final String _str;
  final int    _dx;
  final int    _dy;

  Direction get from {
    if (Direction.top == this ) { return Direction.bottom; }
    else if (Direction.right == this) { return Direction.left; }
    else if (Direction.bottom == this) { return Direction.top; }
    else if (Direction.left == this) { return Direction.right; }
    else { throw FormatException("Invalid direction");}
  }

  static Direction read(String aS) {
    switch(aS) {
      case "TOP"    : return Direction.top;
      case "RIGHT"  : return Direction.right;
      case "BOTTOM" : return Direction.bottom;
      case "LEFT"   : return Direction.left;
      default       : throw FormatException("Invalid direction: ${aS}");
    }
  }
}


class RoomInOut {
  final List<Direction> _ins;
  final List<Direction> _outs;

  List<Direction> get ins   => _ins;
  List<Direction> get outs  => _outs;

  RoomInOut(List<Direction> this._ins, List<Direction> this._outs) {}
}

typedef RoomType = int;

final ROOM_TYPES_TO_WAYOUT = <int, List<RoomInOut>> {
    0   : [],

    1   : [RoomInOut([Direction.top, Direction.right, Direction.left],
                     [Direction.bottom])],

    2   : [RoomInOut([Direction.right, Direction.left],
                     [Direction.right, Direction.left])],

    3   : [RoomInOut([Direction.top],
                     [Direction.bottom])],

    4   : [RoomInOut([Direction.top], [Direction.left]),
           RoomInOut([Direction.right], [Direction.bottom])],

    5   : [RoomInOut([Direction.top], [Direction.right]),
           RoomInOut([Direction.left], [Direction.bottom])],

    6   : [RoomInOut([Direction.right, Direction.left],
                     [Direction.right, Direction.left])],

    7   : [RoomInOut([Direction.top, Direction.right],
                     [Direction.bottom])],

    8   : [RoomInOut([Direction.right, Direction.left],
                     [Direction.bottom])],

    9   : [RoomInOut([Direction.top, Direction.left],
                     [Direction.bottom])],

    10  : [RoomInOut([Direction.top],
                     [Direction.left])],

    11  : [RoomInOut([Direction.top],
                     [Direction.right])],

    12  : [RoomInOut([Direction.right],
                     [Direction.bottom])],

    13  : [RoomInOut([Direction.left],
                     [Direction.bottom])],
};

class Pair {
  final int first;
  final int second;
  Pair(this.first, this.second){}
}

class IndiPos {
  final int _x;
  final int _y;
  final Direction _pos;

  IndiPos(this._x, this._y, this._pos) {}

  static IndiPos read() {
    final vInputs = readLineSync().split(' ');
    return IndiPos(int.parse(vInputs[0]),
                   int.parse(vInputs[1]),
                   Direction.read(vInputs[2]));
  }

  Pair    get xy    => Pair(_x, _y);
  String  get xyStr => "${_x} ${_y}";
    
  IndiPos move(Direction aDir) {
      return IndiPos(_x+aDir.dx, _y+aDir.dy, aDir.from);
  }
}



class Game {
  final int                   _w;
  final int                   _h;
  final List<List<RoomType>>  _lines;
  final int                   _ex;
  
  Game(this._w, this._h, this._lines, this._ex) {}

  RoomType roomAt(int aX, int aY) => _lines[aY][aX];


  void loop() {
    while (true) {
      final vIPos=IndiPos.read();
      logd("## x: ${vIPos._x}, y: ${vIPos._y}, pos: ${vIPos._pos.str}");
      print(action(vIPos));
    }
  }


  List<RoomInOut> possibleWayouts(int aRoom, Direction aPos) {
    String showPoss(List<Direction> aPoss) {
      return aPoss.map( (x) => x.str ).join(",");
      //  return aPoss.joinToString(transform={d: Direction -> d.str});
    }

    if (ROOM_TYPES_TO_WAYOUT.containsKey(aRoom)) {
        final vRoomsInOuts=ROOM_TYPES_TO_WAYOUT[aRoom]!;
        logd("# Room: ${aRoom}: ${vRoomsInOuts.length}");
        for (int i=0; i<vRoomsInOuts.length; ++i) {
          logd("#  ${i}: ${showPoss(vRoomsInOuts[i].ins)} -> ${showPoss(vRoomsInOuts[i].outs)}");
        }
        return vRoomsInOuts.where((x) => x._ins.contains(aPos)).toList();
    } else {
        throw Exception("Not a valid room type: ${aRoom}");
    }
  }


  String action(IndiPos aIPos) {
    final vRoom=roomAt(aIPos._x, aIPos._y);
    final vInOuts=possibleWayouts(vRoom, aIPos._pos);
    assert(vInOuts[0]._ins.contains(aIPos._pos));
    if (1 == vInOuts.length) {
      if(1 == vInOuts[0]._outs.length) {
        return aIPos.move(vInOuts[0]._outs[0]).xyStr;
      } else {
        // Exclude way in from way outs
        final vOuts=vInOuts[0]._outs.where((x) => x!=aIPos._pos).toList();
        if (1 == vOuts.length) {
          return aIPos.move(vOuts[0]).xyStr;
        } else {
          throw Exception("To be implemented 1");
        }
      }
    }else{
      throw Exception("To be implemented 2");
    }
  }

  static Game read() {
    List vInputs=readLineSync().split(' ');
    int vW = int.parse(vInputs[0]); // number of columns.
    int vH = int.parse(vInputs[1]); // number of rows.

    return Game(vW, vH,
                [for(var y=0; y<vH; ++y) readLineSync().split(" ").map( (x) => int.parse(x)).toList()],
                int.parse(readLineSync())); // the coordinate along the X axis of the exit (not useful for this first mission, but must be read).
  }

  Game logTunnel() {
    String format(int x) {
      return (x<10 ? " ": "")+x.toString();
    }

    logd("## Tunnel: ${_w}x${_h}");
    for (int iY=0; iY<_h; ++iY) {
      logd("## ${format(iY)}: ", false);
      for(int iX=0; iX<_w; ++iX) {
          logd("${format(_lines[iY][iX])} ", false);
      }
      logd("");
    }
    return this;
  }

}

void main() {
    Game vGame=Game.read();
    vGame.logTunnel();
    vGame.loop();
}
