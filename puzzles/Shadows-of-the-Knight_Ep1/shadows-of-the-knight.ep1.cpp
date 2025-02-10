#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
 struct Pos {
    int x;
    int y;
};

struct Game {
    int w;
    int h;
    int n;
    Pos pos;
    int xmin;
    int ymin;
    int xmax;
    int ymax;

    static Game read() {
        Game ret_game;
        int w; // width of the building.
        int h; // height of the building.
        cin >> ret_game.w >> ret_game.h; cin.ignore();
        cin >> ret_game.n; cin.ignore();
        cin >> ret_game.pos.x >> ret_game.pos.y; cin.ignore();

        ret_game.xmin = ret_game.ymin = 0;
        ret_game.xmax = ret_game.w-1;
        ret_game.ymax = ret_game.h-1;
        return ret_game;
    }

    void dump() {
        cerr << "Game: " << this->w << "x" << this->h << ", " << this->n << ", +" << this->pos.x << "+" << this->pos.y << endl;         
    }

    Pos action(string const &a_bomb_dir) {
        int v_x2, v_y2;

        if ( "R" == a_bomb_dir || "UR"== a_bomb_dir || "DR"== a_bomb_dir ) {
            v_x2 = this->xmax + 1;
            this->xmin = this->pos.x + 1;
        
        } else if( "L" == a_bomb_dir || "UL" == a_bomb_dir || "DL" == a_bomb_dir ) {
            v_x2 = this->xmin -1;
            this->xmax = this->pos.x - 1;

        } else {
            v_x2 = this->pos.x;
            this->xmin = this->xmax = this->pos.x;
        }

        if ( "D" == a_bomb_dir || "DR" == a_bomb_dir || "DL" == a_bomb_dir ) {
            v_y2 = this->ymax + 1;
            this->ymin = this->pos.y + 1;

        } else if ( "U" == a_bomb_dir || "UR" == a_bomb_dir || "UL" == a_bomb_dir ) {
            v_y2 = this->ymin - 1;
            this->ymax = this->pos.y - 1;

        } else {
            v_y2 = this->pos.y;
            this->ymin = this->ymax = this->pos.y;
        }

        this->pos.x = ( this->pos.x + v_x2 )/2;
        this->pos.y = ( this->pos.y + v_y2 )/2;
        return this->pos;
    }
};

struct Dir {
    string  dir;
    Pos     pos;
};

Dir dirs[] = {
    {"UL",  { -1, -1 }},
    {"U",   { 0, -1 }},
    {"UR",  { +1, -1 }},
    {"R",   { +1, 0 }},
    {"DR",  { +1, +1 }},
    {"D",   { 0, +1 }},
    {"DL",  { -1, +1 }},
    {"L",   { -1, 0 }},
};


int main()
{
    Game v_game=Game::read();
    v_game.dump();

    // game loop
    while (1) {
        string v_bomb_dir; // the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
        cin >> v_bomb_dir; cin.ignore();
        cerr << "Dir: " << v_bomb_dir;
        Pos v_action=v_game.action(v_bomb_dir);
        cout << v_action.x << " " << v_action.y << endl;
    }
}
