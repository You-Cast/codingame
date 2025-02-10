import java.util.*
import java.io.*
import java.math.*

data class Pos(val x: Int, val y: Int)

class Game(aW: Int, aH: Int, aN: Int, aPos: Pos) {
    val _w: Int = aW;
    val _h: Int = aH;
    val _n: Int = aN;
    var _xmin: Int = 0;
    var _ymin: Int = 0;
    var _xmax: Int = _w-1;
    var _ymax: Int = _h-1;
    var _pos: Pos = aPos;


    fun dump() {
        System.err.println("Game: ${_w}x${_h}, ${_n}, ${_pos.x}+${_pos.y}");
    }

    fun loop(aIn: Scanner) {
        while (true) {
            val aBombDir = aIn.next() // the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
            System.err.println("Dir: ${aBombDir}");
            val aAction: Pos = action(aBombDir);
            println("${aAction.x} ${aAction.y}")
        }
    }

    fun action(aBombDir: String) : Pos {
        val vX2 : Int = when (aBombDir.last()) {
            'R' -> {
                _xmin = _pos.x + 1;
                _xmax + 1;
            }
        
            'L' -> {
                _xmax = _pos.x - 1;
                _xmin -1;
            }

            else -> {
                _xmin = _pos.x;
                _xmax = _pos.x;
                _pos.x;
            }
        }

        val vY2 : Int = when ( aBombDir.first() ) {
            'D' -> {
                _ymin = _pos.y + 1;
                _ymax + 1;
            }

            'U' -> {
                _ymax = _pos.y - 1;
                _ymin - 1;
            }

            else -> {
                _ymin = _pos.y;
                _ymax = _pos.y;
                _pos.y;
            }
        }

        _pos = Pos((_pos.x+vX2)/2, (_pos.y+vY2)/2);
        return _pos;
    }
    
}

fun readGame(aInput: Scanner) : Game {
    val vW = aInput.nextInt() // width of the building.
    val vH = aInput.nextInt() // height of the building.
    val vN = aInput.nextInt() // maximum number of turns before game over.
    val vX0 = aInput.nextInt()
    val vY0 = aInput.nextInt()
    return Game(vW, vH, vN, Pos(vX0, vY0));
}

fun main(args : Array<String>) {
    val vInput = Scanner(System.`in`)
    val vGame: Game = readGame(vInput);
    vGame.dump();
    vGame.loop(vInput);
}
