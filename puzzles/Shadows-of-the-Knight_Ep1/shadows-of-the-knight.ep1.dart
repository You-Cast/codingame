import 'dart:io';
import 'dart:math';

String readLineSync() {
  String? s = stdin.readLineSync();
  return s == null ? '' : s;
}

class Pos {
  int _x, _y;
  Pos(this._x, this._y);

  int get x => _x;
  int get y => _y;
}

class Game {
  int _w, _h, _n;
  Pos _pos;
  int _xmin, _xmax, _ymin, _ymax;

  Game(this._w, this._h, this._n, this._pos)
    : _xmin=0, _ymin=0, _xmax=_w-1, _ymax=_h-1 {
  }

  void dump() {
    stderr.writeln("Game: "+_w.toString()+"x"+_h.toString()+", "+_n.toString()+", +"+_pos.x.toString()+"+"+_pos.y.toString());
  }

  void loop() {
    while (true) {
        String vBombDir = readLineSync(); // the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
        Pos vAction=action(vBombDir);
        print(vAction.x.toString()+" "+vAction.y.toString());
    } 
  }

  Pos action(String aBombDir) {
    int vX2, vY2;
    switch (aBombDir[aBombDir.length-1]) {
      case 'R': {
        _xmin = _pos.x + 1;
        vX2 = _xmax + 1;
        break;
      }
        
      case 'L': {
        _xmax = _pos.x - 1;
        vX2 = _xmin -1;
        break;
      }

      default: {
        _xmin = _pos.x;
        _xmax = _pos.x;
        vX2 = _pos.x;
        break;
      }
    }

    switch( aBombDir[0] ) {
      case 'D': {
        _ymin = _pos.y + 1;
        vY2 = _ymax + 1;
        break;
      }

      case 'U': {
        _ymax = _pos.y - 1;
        vY2 = _ymin - 1;
        break;
      }

      default: {
        _ymin = _pos.y;
        _ymax = _pos.y;
        vY2 = _pos.y;
        break;
      }
    }
    _pos = Pos(((_pos.x+vX2)/2).round(), ((_pos.y+vY2)/2).round());
    return _pos;
  }

}


Game readGame() {
    List vInputs = readLineSync().split(' ');
    int vW = int.parse(vInputs[0]); // width of the building.
    int vH = int.parse(vInputs[1]); // height of the building.
    int vN = int.parse(readLineSync()); // maximum number of turns before game over.
    vInputs = readLineSync().split(' ');
    int vX0 = int.parse(vInputs[0]);
    int vY0 = int.parse(vInputs[1]);
    return Game(vW, vH, vN, Pos(vX0, vY0));
}




void main() {
  Game vGame=readGame();
  vGame.dump();
  vGame.loop();
}
