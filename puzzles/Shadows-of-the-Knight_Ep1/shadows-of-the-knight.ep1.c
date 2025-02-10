#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

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
    struct Pos pos;
    int xmin;
    int ymin;
    int xmax;
    int ymax;
};

struct Dir {
    char        dir[3];
    struct Pos  pos;
};

struct Dir dirs[] = {
    {"UL",  { -1, -1 }},
    {"U",   { 0, -1 }},
    {"UR",  { +1, -1 }},
    {"R",   { +1, 0 }},
    {"DR",  { +1, +1 }},
    {"D",   { 0, +1 }},
    {"DL",  { -1, +1 }},
    {"L",   { -1, 0 }},

};


void readGame(struct Game *aGame) {
    scanf("%d%d", &aGame->w, &aGame->h);
    scanf("%d", &aGame->n);
    scanf("%d%d", &aGame->pos.x, &aGame->pos.y);

    aGame->xmin = aGame->ymin = 0;
    aGame->xmax = aGame->w-1;
    aGame->ymax = aGame->h-1;
}

void dumpGame(struct Game *a_game) {
    fprintf(stderr, "Game: %dx%d, %d, +%d+%d\n", a_game->w, a_game->h, a_game->n, a_game->pos.x, a_game->pos.y);
}

struct Pos action(struct Game *a_game, char *a_bomb_dir) {
    int v_x2, v_y2;

    if ( 0==strcmp(a_bomb_dir, "R") || 0==strcmp(a_bomb_dir, "UR") || 0==strcmp(a_bomb_dir, "DR") ) {
        v_x2 = a_game->xmax + 1;
        a_game->xmin = a_game->pos.x + 1;
    
    } else if( 0==strcmp(a_bomb_dir, "L") || 0==strcmp(a_bomb_dir, "UL") || 0==strcmp(a_bomb_dir, "DL") ) {
        v_x2 = a_game->xmin -1;
        a_game->xmax = a_game->pos.x - 1;

    } else {
        v_x2 = a_game->pos.x;
        a_game->xmin = a_game->xmax = a_game->pos.x;
    }

    if ( 0==strcmp(a_bomb_dir, "D") || 0==strcmp(a_bomb_dir, "DR") || 0==strcmp(a_bomb_dir, "DL") ) {
        v_y2 = a_game->ymax + 1;
        a_game->ymin = a_game->pos.y + 1;

    } else if ( 0==strcmp(a_bomb_dir, "U") || 0==strcmp(a_bomb_dir, "UR") || 0==strcmp(a_bomb_dir, "UL") ) {
        v_y2 = a_game->ymin - 1;
        a_game->ymax = a_game->pos.y - 1;

    } else {
        v_y2 = a_game->pos.y;
        a_game->ymin = a_game->ymax = a_game->pos.y;
    }

    a_game->pos.x = ( a_game->pos.x + v_x2 )/2;
    a_game->pos.y = ( a_game->pos.y + v_y2 )/2;
    return a_game->pos;
}

void loop(struct Game *a_game) {
    while (1) {
        // the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
        char v_bomb_dir[4];
        struct Pos v_action;
        scanf("%s", v_bomb_dir);
        fprintf(stderr, "Dir: %s\n", v_bomb_dir);
        v_action = action(a_game, v_bomb_dir);

        printf("%d %d\n", v_action.x, v_action.y);
    }
}



int main() { 
    struct Game vGame;
    readGame(&vGame);
    dumpGame(&vGame);
    loop(&vGame);
    return 0;
}
