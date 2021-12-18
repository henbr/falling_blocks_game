import math
import pyxel
from constants import *


def tiles_init(width, height):
    return [[0] * width for _ in range(height)]


def tiles_dim(tiles):
    height = len(tiles)
    width = len(tiles[0])
    return (width, height)


def tiles_rect(tiles):
    (w, h) = tiles_dim(tiles)
    x0 = w - 1
    y0 = h - 1
    x1 = 0
    y1 = 0
    for py in range(h):
        for px in range(w):
            t = tiles[py][px]
            if t != 0:
                x0 = min(x0, px)
                y0 = min(y0, py)
                x1 = max(x1, px + 1)
                y1 = max(y1, py + 1)
    return (x0, y0, x1, y1)


def tiles_copy(src, dst, dx, dy):
    (w, h) = tiles_dim(src)
    for y in range(h):
        for x in range(w):
            if src[y][x] == 0:
                continue
            dst[dy + y][dx + x] = src[y][x]


def tiles_draw(tiles, x, y):
    (w, h) = tiles_dim(tiles)
    for py in range(h):
        for px in range(w):
            t = tiles[py][px]
            if t != 0:
                tx = (x + px) * TILE_SIZE
                ty = (y + py) * TILE_SIZE
                pyxel.blt(tx, ty, 0, t * TILE_SIZE, 0,
                          TILE_SIZE, TILE_SIZE, None)


def draw_number(x, y, number):
    zero_x = 0
    zero_y = 6
    digit_x = x
    for i in reversed(range(5)):
        divider = pow(10, i)
        if number < divider and i > 0:
            continue
        digit = math.floor(number / divider) % 10
        pyxel.blt(digit_x, y, 0, (zero_x + digit) * TILE_SIZE,
                  zero_y * TILE_SIZE, TILE_SIZE, TILE_SIZE, None)
        pyxel.blt(digit_x, y + TILE_SIZE, 0, (zero_x + digit) * TILE_SIZE,
                  (zero_y + 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE, None)
        digit_x += TILE_SIZE


def write_score(score):
    if score == 0:
        return
    with open("highscore.txt", "a") as file:
        file.write(f"{score}\n")


def read_high_score():
    highscore = 0
    try:
        with open("highscore.txt", "r") as file:
            for line in file.readlines():
                highscore = max(highscore, int(line))
    except:
        pass
    return highscore
