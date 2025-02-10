using System;
using System.Linq;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;

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

    public Pos(Pos a_pos) {
        _x = a_pos.x;
        _y = a_pos.y;
    }
    public int x { get => _x; }
    public int y { get => _y; }
}


class Game
{
    private int _w, _h, _n;
    private Pos _pos;
    private int _xmin, _ymin;
    private int _xmax, _ymax;

    static private Dictionary<string, Pos> DIRS = new Dictionary<string, Pos>{
        {"UL",  new Pos(-1, -1)},
        {"U",   new Pos(0, -1)},
        {"UR",  new Pos(+1, -1)},
        {"R",   new Pos(+1, 0)},
        {"DR",  new Pos(+1, +1)},
        {"D",   new Pos(0, +1)},
        {"DL",  new Pos(-1, +1)},
        {"L",   new Pos(-1, 0)},
    };

    public Game(int a_w, int a_h, int a_n, Pos a_pos) {
        _w = a_w;
        _h = a_h;
        _n = a_n;
        _pos = new Pos(a_pos);
        _xmin = _ymin = 0;
        _xmax = _w -1;
        _ymax = _h -1;
    }

    public void Dump() {
        Console.Error.WriteLine($"Game: {_w}x{_h}, {_n}, +{_pos.x}+{_pos.y}");
    }

    public void Loop() {
        // game loop
        while (true)
        {
            string vBombDir = Console.ReadLine(); // the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
            Console.Error.WriteLine($"Dir: {vBombDir}");
            Pos vAction=Action(vBombDir);

            Console.WriteLine($"{vAction.x} {vAction.y}");
        }

    }

    Pos Action(string aBombDir) {
        int v_x2, v_y2;
        switch ( aBombDir[aBombDir.Length-1] ) {
            case  'R':
                v_x2 = _xmax + 1;
                _xmin = _pos.x + 1;
                break;
        
            case 'L':
                v_x2 = _xmin -1;
                _xmax = _pos.x - 1;
                break;

            default:
                v_x2 = _pos.x;
                _xmin = _xmax = _pos.x;
                break;
        }

        switch ( aBombDir[0] ) {
            case 'D':
                v_y2 = _ymax + 1;
                _ymin = _pos.y + 1;
                break;

            case 'U':
                v_y2 = _ymin - 1;
                _ymax = _pos.y - 1;
                break;

            default:
                v_y2 = _pos.y;
                _ymin = _ymax = _pos.y;
                break;
        }

        _pos = new Pos((_pos.x+v_x2)/2, (_pos.y+v_y2)/2);
        return new Pos(_pos);
    }
}


class Reader
{
    static public Game ReadGame() {
        string[] v_inputs;
        v_inputs = Console.ReadLine().Split(' ');
        int v_w = int.Parse(v_inputs[0]); // width of the building.
        int v_h = int.Parse(v_inputs[1]); // height of the building.
        int v_n = int.Parse(Console.ReadLine()); // maximum number of turns before game over.
        v_inputs = Console.ReadLine().Split(' ');
        int v_x0 = int.Parse(v_inputs[0]);
        int v_y0 = int.Parse(v_inputs[1]);
        return new Game(v_w, v_h, v_n, new Pos(v_x0, v_y0));
    }
}
class Player
{
    static void Main(string[] args)
    {
        Game v_game=Reader.ReadGame();
        v_game.Dump();
        v_game.Loop();
    }
}
