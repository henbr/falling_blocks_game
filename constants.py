BASE_SPEED = 20  # Number of frames between moving the piece downward
LEVEL_SPEED_ADJUST = 1  # How much to increase speed for each level
LINES_PER_LEVEL = 10  # How many lines to clear to get to the next level

TILE_SIZE = 8
GAME_WIDTH = 10
GAME_HEIGHT = 20
GAME_TOP_TX = 11
GAME_TOP_TY = 2
GAME_TOP_X = TILE_SIZE * GAME_TOP_TX
GAME_TOP_Y = TILE_SIZE * GAME_TOP_TY

PIECES = [
    # J
    [[
        [0, 0, 0],
        [3, 3, 3],
        [0, 0, 3],
    ], [
        [0, 3, 0],
        [0, 3, 0],
        [3, 3, 0],
    ], [
        [3, 0, 0],
        [3, 3, 3],
        [0, 0, 0],
    ], [
        [0, 3, 3],
        [0, 3, 0],
        [0, 3, 0],
    ]],

    # L
    [[
        [0, 0, 0],
        [2, 2, 2],
        [2, 0, 0],
    ], [
        [2, 2, 0],
        [0, 2, 0],
        [0, 2, 0],
    ], [
        [0, 0, 2],
        [2, 2, 2],
        [0, 0, 0],
    ], [
        [0, 2, 0],
        [0, 2, 0],
        [0, 2, 2],
    ]],

    # T
    [[
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0],
    ], [
        [0, 1, 0],
        [1, 1, 0],
        [0, 1, 0],
    ], [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0],
    ], [
        [0, 1, 0],
        [0, 1, 1],
        [0, 1, 0],
    ]],

    # O
    [[
        [1, 1],
        [1, 1],
    ]],

    # I
    [[
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
    ], [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
    ]],

    # S
    [[
        [0, 0, 0],
        [0, 3, 3],
        [3, 3, 0],
    ], [
        [0, 3, 0],
        [0, 3, 3],
        [0, 0, 3],
    ]],

    # Z
    [[
        [0, 0, 0],
        [2, 2, 0],
        [0, 2, 2],
    ], [
        [0, 2, 0],
        [2, 2, 0],
        [2, 0, 0],
    ]]
]
