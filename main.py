import random
import pyxel
from utils import *
from constants import *


class Piece:
    def __init__(self, piece, x, y, rotation):
        self.x = x
        self.y = y
        self.piece = piece
        self.rotation = rotation

    def clone(self):
        return Piece(self.piece, self.x, self.y, self.rotation)

    def draw(self):
        tiles = self.piece[self.rotation]
        tiles_draw(tiles, GAME_TOP_TX + self.x, GAME_TOP_TY + self.y)

    def drop(self, game_tiles):
        old_y = self.y
        while self.is_position_valid(game_tiles):
            old_y = self.y
            self.y += 1
        self.y = old_y

    def move_down(self):
        modified = self.clone()
        modified.y += 1
        return modified

    def rotate_left(self):
        modified = self.clone()
        modified.rotation = (modified.rotation + 1) % len(modified.piece)
        return modified

    def rotate_right(self):
        modified = self.clone()
        modified.rotation = (modified.rotation - 1) % len(modified.piece)
        return modified

    def move_left(self):
        modified = self.clone()
        modified.x -= 1
        return modified

    def move_right(self):
        modified = self.clone()
        modified.x += 1
        return modified

    def is_position_valid(self, game_tiles):
        tiles = self.piece[self.rotation]
        (w, h) = tiles_dim(tiles)
        for py in range(h):
            for px in range(w):
                t = tiles[py][px]
                if t == 0:
                    continue
                tx = self.x + px
                ty = self.y + py
                if ty < 0:
                    continue  # To allow rotation of newly spawned pieces
                if tx < 0 or tx >= GAME_WIDTH:
                    return False
                if ty >= GAME_HEIGHT:
                    return False
                if game_tiles[ty][tx] != 0:
                    return False
        return True


class Game:
    def __init__(self, width, height, highscore):
        self.highscore = highscore
        self.width = width
        self.height = height
        self.tiles = tiles_init(width, height)
        self.piece = None
        self.next_piece_index = None
        self.stats = [0] * len(PIECES)
        self.score = 0
        self.lines = 0
        self.level = 1
        self.level_count_down = LINES_PER_LEVEL
        self.gameover = False

    def update(self):
        if pyxel.frame_count % max(1, (BASE_SPEED - LEVEL_SPEED_ADJUST * self.level)) == 0:
            modified = self.piece.move_down()
            if not modified.is_position_valid(self.tiles):
                self.place_piece()
                self.spawn_piece()
                pyxel.play(0, 0)
            else:
                self.piece = modified
        self.clear_complete_lines()

    def clear_complete_lines(self):
        cleared_lines = 0
        for ty in range(self.height):
            num_tiles = 0
            for tx in range(self.width):
                if self.tiles[ty][tx] != 0:
                    num_tiles += 1
            if num_tiles == GAME_WIDTH:
                self.clear_line(ty)
                cleared_lines += 1

        self.lines += cleared_lines
        self.score += pow(self.level, 2) * pow(cleared_lines, 3)

        if cleared_lines > 0:
            pyxel.play(0, 1)
            self.level_count_down -= 1
            if self.level_count_down == 0:
                self.level_count_down = LINES_PER_LEVEL
                self.level += 1

    def clear_line(self, line_to_clear):
        for ty in reversed(range(line_to_clear+1)):
            for tx in range(self.width):
                self.tiles[ty][tx] = 0 if ty == 0 else self.tiles[ty - 1][tx]

    def update_next_piece(self):
        self.next_piece_index = random.randint(0, len(PIECES) - 1)

    def spawn_piece(self):
        tile_data = PIECES[self.next_piece_index]
        (_, y0, _, _) = tiles_rect(tile_data[0])
        next_piece = Piece(tile_data, int(GAME_WIDTH / 2), -y0, 0)
        self.piece = next_piece
        self.stats[self.next_piece_index] += 1
        self.update_next_piece()
        if not self.piece.is_position_valid(self.tiles):
            self.gameover = True
            return

    def place_piece(self):
        tiles_copy(self.piece.piece[self.piece.rotation],
                   self.tiles, self.piece.x, self.piece.y)
        self.score += self.level

    def draw(self):
        tiles_draw(self.tiles, GAME_TOP_TX, GAME_TOP_TY)
        self.piece.draw()
        self.draw_stats()
        self.draw_scores()
        self.draw_next_piece()

    def draw_scores(self):
        x = 23 * TILE_SIZE + 4
        y = 8 * TILE_SIZE + 4

        pyxel.text(x, y, "Highscore", 8)
        draw_number(x, y + 6, max(self.score, self.highscore))
        y += TILE_SIZE * 3 + 4

        pyxel.text(x, y, "Score", 8)
        draw_number(x, y + 6, self.score)
        y += TILE_SIZE * 3 + 4

        pyxel.text(x, y, "Lines", 8)
        draw_number(x, y + 6, self.lines)
        y += TILE_SIZE * 3 + 4

        pyxel.text(x, y, "Level", 8)
        draw_number(x, y + 6, self.level)

    def draw_next_piece(self):
        tiles = PIECES[self.next_piece_index][0]
        (_, y0, _, _) = tiles_rect(tiles)
        tiles_draw(tiles, 24, 3 - y0)

    def draw_stats(self):
        offset_x = 1 + (1 / 8) * 5
        offset_y = (1 / 8) * 7
        tile_y = 2 + offset_y
        for s in range(len(PIECES)):
            tiles = PIECES[s][0]
            (_, y0, _, y1) = tiles_rect(tiles)
            tiles_draw(tiles, offset_x, tile_y - y0)
            num_y = tile_y + (y1 - y0) * 0.5 - 1
            draw_number(5 * TILE_SIZE + 6, num_y * TILE_SIZE, self.stats[s])
            tile_y += (y1 - y0) + offset_y

    def rotate_left(self):
        modified = self.piece.rotate_left()
        if modified.is_position_valid(self.tiles):
            self.piece = modified

    def rotate_right(self):
        modified = self.piece.rotate_right()
        if modified.is_position_valid(self.tiles):
            self.piece = modified

    def move_left(self):
        modified = self.piece.move_left()
        if modified.is_position_valid(self.tiles):
            self.piece = modified

    def move_right(self):
        modified = self.piece.move_right()
        if modified.is_position_valid(self.tiles):
            self.piece = modified

    def drop(self):
        self.piece.drop(self.tiles)
        self.place_piece()
        self.spawn_piece()
        pyxel.play(0, 0)


class App:
    def __init__(self):
        self.highscore = read_high_score()
        self.start_new_game()
        pyxel.init(256, 192, title="Falling Blocks Game")
        pyxel.load("blocks.pyxres")
        pyxel.run(self.update, self.draw)

    def start_new_game(self):
        self.game = Game(GAME_WIDTH, GAME_HEIGHT, self.highscore)
        self.game.update_next_piece()
        self.game.spawn_piece()
        self.state = "playing"

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_S):
            pyxel.screenshot()
        if self.state == "playing":
            self.update_playing()
        elif self.state == "gameover":
            self.update_gameover()
        elif self.state == "paused":
            self.update_paused()

    def update_paused(self):
        if pyxel.btnp(pyxel.KEY_P):
            self.state = "playing"
            pyxel.play(0, 2)

    def update_gameover(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.start_new_game()

    def update_playing(self):
        if pyxel.btnp(pyxel.KEY_P):
            self.state = "paused"
            pyxel.play(0, 3)
        if pyxel.btnp(pyxel.KEY_UP):
            self.game.rotate_left()
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.game.drop()
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.game.move_left()
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.game.move_right()

        self.game.update()

        if self.game.gameover:
            write_score(self.game.score)
            self.highscore = max(self.highscore, self.game.score)
            self.state = "gameover"
            pyxel.play(0, 4)

    def draw(self):
        pyxel.cls(0)
        if self.state == "playing":
            self.game.draw()
        elif self.state == "gameover":
            pyxel.text((GAME_TOP_TX + 3) * TILE_SIZE,
                       (GAME_TOP_TY + 7) * TILE_SIZE, "Game Over", 8)
            pyxel.text((GAME_TOP_TX + 3) * TILE_SIZE - 4,
                       (GAME_TOP_TY + 9) * TILE_SIZE, "Press Space", 8)
        elif self.state == "paused":
            pyxel.text((GAME_TOP_TX + 3) * TILE_SIZE + 6,
                       (GAME_TOP_TY + 7) * TILE_SIZE, "Paused", 8)
        pyxel.bltm(0, 0, 0, 0, 0, 32, 24, 0)


App()
