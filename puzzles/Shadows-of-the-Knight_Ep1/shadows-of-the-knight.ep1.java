import java.util.*;
import java.io.*;
import java.math.*;
import static java.util.Map.entry;    
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
class Pos
{
    private int _x, _y;

    public Pos(int aX, int aY ) {
        _x = aX; 
        _y = aY;
    }

    public Pos(Pos aPos) {
        _x = aPos.getX();
        _y = aPos.getY();
    }

    public int getX() { return _x; }
    public int getY() { return _y; }
}


class Game
{
    private int _w, _h, _n;
    private Pos _pos;
    private int _xmin, _ymin;
    private int _xmax, _ymax;

    static final private Map<String, Pos> DIRS = Map.ofEntries(
        entry("UL",  new Pos(-1, -1)),
        entry("U",   new Pos(0, -1)),
        entry("UR",  new Pos(+1, -1)),
        entry("R",   new Pos(+1, 0)),
        entry("DR",  new Pos(+1, +1)),
        entry("D",   new Pos(0, +1)),
        entry("DL",  new Pos(-1, +1)),
        entry("L",   new Pos(-1, 0))
    );

    public Game(int a_w, int a_h, int a_n, Pos a_pos) {
        _w = a_w;
        _h = a_h;
        _n = a_n;
        _pos = new Pos(a_pos);
        _xmin = _ymin = 0;
        _xmax = _w -1;
        _ymax = _h -1;
    }

    public void dump() {
        System.err.println(String.format("Game: {%d}x{%d}, {%d}, +{%d}+{%d}", _w, _h, _n, _pos.getX(), _pos.getY()));
    }

    public void loop(Scanner aIn) {
        // game loop
        while (true) {
            String vBombDir = aIn.next(); // the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
            System.err.println(String.format("Dir: %s", vBombDir));
            Pos vAction=action(vBombDir);
            System.out.println(String.format("%d %d", vAction.getX(), vAction.getY()));
        }
    }

    Pos action(String aBombDir) {
        int v_x2, v_y2;
        switch ( aBombDir.charAt(aBombDir.length()-1) ) {
            case  'R':
                v_x2 = _xmax + 1;
                _xmin = _pos.getX() + 1;
                break;
        
            case 'L':
                v_x2 = _xmin -1;
                _xmax = _pos.getX() - 1;
                break;

            default:
                v_x2 = _pos.getX();
                _xmin = _xmax = _pos.getX();
                break;
        }

        switch ( aBombDir.charAt(0) ) {
            case 'D':
                v_y2 = _ymax + 1;
                _ymin = _pos.getY() + 1;
                break;

            case 'U':
                v_y2 = _ymin - 1;
                _ymax = _pos.getY() - 1;
                break;

            default:
                v_y2 = _pos.getY();
                _ymin = _ymax = _pos.getY();
                break;
        }

        _pos = new Pos((_pos.getX()+v_x2)/2, (_pos.getY()+v_y2)/2);
        return new Pos(_pos);
    }
}


class Reader
{
    static public Game readGame(Scanner aIn) {
        int v_w = aIn.nextInt(); // width of the building.
        int v_h = aIn.nextInt(); // height of the building.
        int v_n = aIn.nextInt(); // maximum number of turns before game over.
        int v_x0 = aIn.nextInt();
        int v_y0 = aIn.nextInt();
        return new Game(v_w, v_h, v_n, new Pos(v_x0, v_y0));
    }
}


class Player {

    public static void main(String args[]) {
        Scanner vIn = new Scanner(System.in);

        Game vGame=Reader.readGame(vIn);
        vGame.dump();
        vGame.loop(vIn);

        vIn.close();
    }
}
