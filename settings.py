import pygame as pg
import math
import time

vec = pg.math.Vector2

FPS = 60
FIELD_COLOR = (33, 32, 53)
BG_COLOR = (26, 39, 83)
GRID_DOT_COLOR = (100, 100, 100)

SPRITE_DIR_PATH = 'assets/sprites'
FONT_PATH = 'assets/fonts/FREAKSOFNATUREMASSIVE.ttf'
MUSIC_PATH = 'assets/songs'

ANIM_TIME_INTERVAL = 175 # milliseconds
FAST_ANIM_TIME_INTERVAL = 40 # milliseconds
GAME_END_TIME_INTERVAL = 300 # milliseconds
DELAY_BETWEEN_TETROMINOS = 50 # time between block placed and next tetromino
LR_HI_FACTOR = 1.5
LEFT_RIGHT_HOLD_INTERVAL = math.floor(ANIM_TIME_INTERVAL / LR_HI_FACTOR) # time between movements of blocks to left/right if left/right keydown pressed
# SPEED_FACTOR = 1.3
SPEED_UP_EVERY = 1000
HARD_SKIP_INTERVAL = 1 # seconds

INTERVAL_BETWEEN_TETROMINOS = 200

LEVEL_SPEED = {
    1: ANIM_TIME_INTERVAL,
    2: 130,
    3: 110,
    4: 90,
    5: 75,
    6: 50,
    7: 40
}

POINTS_PER_LINES = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500, 5: 2500, 6: 4000}

TILE_SIZE = 40
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE
GRID_DOT_SIZE = 2

FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H

SMALL_SCALE_FACTOR = 2

SMALL_TILE_SIZE = math.floor(TILE_SIZE/SMALL_SCALE_FACTOR)

INIT_POS_OFFSET = vec(FIELD_W // 2 - 1, 0)
NEXT_POS_OFFSET = vec(FIELD_W * 1.3 * SMALL_SCALE_FACTOR, FIELD_H * 0.35 * SMALL_SCALE_FACTOR)
HOLD_POS_OFFSET = vec(FIELD_W * 1.3 * SMALL_SCALE_FACTOR, FIELD_H * 0.55 * SMALL_SCALE_FACTOR)
MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

TETROMINOS = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, 1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}