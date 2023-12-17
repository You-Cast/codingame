import java.util.*
import java.io.*
import java.math.*

fun logd(aStr: String, aNextLine: Boolean=true) {
    if (aNextLine) {
        System.err.println(aStr);
    } else {
        System.err.print(aStr);
    }
}

 enum class Direction(val str:String, val dx: Int, val dy: Int) {
    TOP     ("TOP",     0,  -1),
    RIGHT   ("RIGHT",   +1, 0),
    BOTTOM  ("BOTTOM",  0, +1),
    LEFT    ("LEFT",    -1, 0);

    val from: Direction get() = when (this) {
        TOP     -> BOTTOM
        RIGHT   -> LEFT
        BOTTOM  -> TOP
        LEFT    -> RIGHT
        else    -> { throw Exception("Invalid direction: ${this}")}
    }

    companion object {
        fun read(aDir: String) : Direction {
            return when (aDir) {
                "TOP"       -> Direction.TOP
                "LEFT"      -> Direction.LEFT
                "RIGHT"     -> Direction.RIGHT
                "BOTTOM"    -> Direction.BOTTOM
                else    -> throw Exception("Invalid pos: ${aDir}");
            }
        }
    }
 }

typealias RoomType = Int;
data class RoomInOut(val _ins: Array<Direction>, val _outs: Array<Direction>) {}


val ROOM_TYPES_TO_WAYOUT: Map<Int, Array<RoomInOut>> = mapOf(
    0  to emptyArray(),
    1  to arrayOf(RoomInOut(arrayOf(Direction.TOP, Direction.RIGHT, Direction.LEFT),
                            arrayOf(Direction.BOTTOM))),

    2  to arrayOf(RoomInOut(arrayOf(Direction.RIGHT, Direction.LEFT),
                            arrayOf(Direction.RIGHT, Direction.LEFT))),

    3  to arrayOf(RoomInOut(arrayOf(Direction.TOP),
                            arrayOf(Direction.BOTTOM))),

    4  to arrayOf(RoomInOut(arrayOf(Direction.TOP),
                            arrayOf(Direction.LEFT)),
                  RoomInOut(arrayOf(Direction.RIGHT),
                            arrayOf(Direction.BOTTOM))),

    5  to arrayOf(RoomInOut(arrayOf(Direction.TOP),
                            arrayOf(Direction.RIGHT)),
                  RoomInOut(arrayOf(Direction.LEFT),
                            arrayOf(Direction.BOTTOM))),

    6  to arrayOf(RoomInOut(arrayOf(Direction.RIGHT, Direction.LEFT),
                            arrayOf(Direction.RIGHT, Direction.LEFT))),

    7  to arrayOf(RoomInOut(arrayOf(Direction.TOP, Direction.RIGHT),
                            arrayOf(Direction.BOTTOM))),

    8  to arrayOf(RoomInOut(arrayOf(Direction.RIGHT, Direction.LEFT),
                            arrayOf(Direction.BOTTOM))),

    9  to arrayOf(RoomInOut(arrayOf(Direction.TOP, Direction.LEFT),
                            arrayOf(Direction.BOTTOM))),

    10 to arrayOf(RoomInOut(arrayOf(Direction.TOP),
                            arrayOf(Direction.LEFT))),

    11 to arrayOf(RoomInOut(arrayOf(Direction.TOP),
                            arrayOf(Direction.RIGHT))),

    12 to arrayOf(RoomInOut(arrayOf(Direction.RIGHT),
                            arrayOf(Direction.BOTTOM))),

    13 to arrayOf(RoomInOut(arrayOf(Direction.LEFT),
                            arrayOf(Direction.BOTTOM))),

)

data class IndiPos(val _x: Int, val _y: Int, val _pos: Direction) {
    companion object {
        fun read(aInput: Scanner) : IndiPos {
            return IndiPos(aInput.nextInt(),
                           aInput.nextInt(),
                           Direction.read(aInput.next()));
        }
    }

    val xy      : Pair<Int, Int> get()  = Pair(_x, _y);
    val xyStr   : String         get()  = "${_x} ${_y}";
    
    fun move(aDir: Direction) : IndiPos {
        return IndiPos(_x+aDir.dx, _y+aDir.dy, aDir.from)
    }
}


class Game(val _w: Int, val _h: Int, val _lines: Array<Array<RoomType>>, val _ex: Int ) {
    fun roomAt(aX: Int, aY: Int) : RoomType {
        return _lines[aY][aX];
    }


    fun loop(aInput: Scanner) {
        while (true) {
            val vIPos=IndiPos.read(aInput);
            logd("## x: ${vIPos._x}, y: ${vIPos._y}, pos: ${vIPos._pos}")
            println(action(vIPos));
        }
    }


    fun possibleWayouts(aRoom: Int, aPos: Direction) : List<RoomInOut> {
        fun showPoss(aPoss: Array<Direction>) : String {
            return aPoss.joinToString(transform={d: Direction -> d.str});
        }
        if (ROOM_TYPES_TO_WAYOUT.contains(aRoom)) {
            val vRoomsInOuts: Array<RoomInOut> =ROOM_TYPES_TO_WAYOUT[aRoom]!!;
            logd("# Room: ${aRoom}: ${vRoomsInOuts.count()}")
            vRoomsInOuts.forEachIndexed{n, x -> logd("#  ${n}: ${showPoss(x._ins)} -> ${showPoss(x._outs)}")};
            return vRoomsInOuts.filter({it._ins.contains(aPos)});
        } else {
            throw Exception("Not a valid room type: ${aRoom}")
        }
    }


    fun action(aIPos: IndiPos) : String {
        val vRoom=roomAt(aIPos._x, aIPos._y);
        val vInOuts: List<RoomInOut> = possibleWayouts(vRoom, aIPos._pos);
        assert(vInOuts[0]._ins.contains(aIPos._pos));
        if (1 == vInOuts.count()) {
            if(1 == vInOuts[0]._outs.count()) {
                return aIPos.move(vInOuts[0]._outs[0]).xyStr;
            } else {
                // Exclude way in from way outs
                val vOuts=vInOuts[0]._outs.filter{it!=aIPos._pos}
                if (1 == vOuts.count()) {
                    return aIPos.move(vOuts[0]).xyStr;
                } else {
                    throw Exception("To be implemented 1");
                }
            }
        }else{
            throw Exception("To be implemented 2");
        }
    }
    companion object {
        fun read(aInput: Scanner) : Game {
            val vW = aInput.nextInt() // number of columns.
            val vH = aInput.nextInt() // number of rows.
            if (aInput.hasNextLine()) {
                aInput.nextLine()
            }
            return Game(vW, vH,
                        Array(vH){_ -> aInput.nextLine().split(" ").map{Integer.parseInt(it)}.toTypedArray()},
                        aInput.nextInt()); // the coordinate along the X axis of the exit (not useful for this first mission, but must be read).
        }
    }

    fun logTunnel() : Game {
        logd("## Tunnel: ${_w}x${_h}")
        for (iY in 0 until _h) {
            logd("## ${"%2d".format(iY)}: ", false);
            for(iX in 0 until _w) {
                logd("${"%2d".format(_lines[iY][iX])} ", false);
            }
            logd("");
        }
        return this;
    }

}


fun main(args : Array<String>) {
    val input = Scanner(System.`in`)
    Game.read(input)
        .logTunnel()
        .loop(input);
}
