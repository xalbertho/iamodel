import pygame
import sys
import time
import copy
from sudoku import make_puzzle, _valid, is_complete, solve

# ── constants ──────────────────────────────────────────────────────────────────
W, H = 720, 760
BOARD_SIZE = 540
CELL = BOARD_SIZE // 9
MARGIN = (W - BOARD_SIZE) // 2

WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
GRAY    = (200, 200, 200)
LIGHT   = (240, 240, 245)
BLUE    = (70,  130, 200)
BLUE_BG = (220, 235, 255)
RED     = (200, 50,  50)
GREEN   = (50,  160, 80)
DARK    = (40,  40,  40)
PANEL   = (245, 245, 250)


def blit_centered(surf, font, text, color, center):
    s = font.render(text, True, color)
    surf.blit(s, s.get_rect(center=center))


def blit_topleft(surf, font, text, color, topleft):
    s = font.render(text, True, color)
    surf.blit(s, topleft)


def blit_topright(surf, font, text, color, topright):
    s = font.render(text, True, color)
    r = s.get_rect()
    r.topright = topright
    surf.blit(s, r)


def draw_button(surf, fonts, rect, text, color, hover=False):
    shade = tuple(min(255, c + 20) for c in color) if hover else color
    pygame.draw.rect(surf, shade, rect, border_radius=8)
    pygame.draw.rect(surf, BLACK, rect, 2, border_radius=8)
    blit_centered(surf, fonts["btn"], text, WHITE, rect.center)


def draw_board(surf, fonts, board, original, selected, invalid_cells):
    pygame.draw.rect(surf, WHITE, (MARGIN, 80, BOARD_SIZE, BOARD_SIZE))

    for row in range(9):
        for col in range(9):
            x = MARGIN + col * CELL
            y = 80 + row * CELL
            rect = pygame.Rect(x, y, CELL, CELL)

            if selected == (row, col):
                pygame.draw.rect(surf, BLUE_BG, rect)
            elif original[row][col] != 0:
                pygame.draw.rect(surf, LIGHT, rect)
            else:
                pygame.draw.rect(surf, WHITE, rect)

            val = board[row][col]
            if val != 0:
                if (row, col) in invalid_cells:
                    color = RED
                elif original[row][col] != 0:
                    color = DARK
                else:
                    color = BLUE
                blit_centered(surf, fonts["num"], str(val), color, rect.center)

    for i in range(10):
        thick = 3 if i % 3 == 0 else 1
        color = BLACK if i % 3 == 0 else GRAY
        pygame.draw.line(surf, color,
                         (MARGIN + i * CELL, 80),
                         (MARGIN + i * CELL, 80 + BOARD_SIZE), thick)
        pygame.draw.line(surf, color,
                         (MARGIN, 80 + i * CELL),
                         (MARGIN + BOARD_SIZE, 80 + i * CELL), thick)


class Game:
    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty
        self.new_game()

    def new_game(self):
        puzzle, solution = make_puzzle(self.difficulty)
        self.board    = copy.deepcopy(puzzle)
        self.original = copy.deepcopy(puzzle)
        self.solution = solution
        self.selected = None
        self.start    = time.time()
        self.hints    = 0
        self.won      = False
        self.invalid  = set()

    def select(self, row, col):
        self.selected = (row, col)

    def place(self, n):
        if not self.selected or self.won:
            return
        r, c = self.selected
        if self.original[r][c] != 0:
            return
        self.board[r][c] = n
        self._check_invalid()
        if n != 0 and is_complete(self.board) and not self.invalid:
            self.won = True

    def hint(self):
        if self.won:
            return
        import random
        empties = [(r, c) for r in range(9) for c in range(9)
                   if self.board[r][c] == 0]
        if empties:
            r, c = random.choice(empties)
            self.board[r][c] = self.solution[r][c]
            self.hints += 1
            self._check_invalid()
            if is_complete(self.board) and not self.invalid:
                self.won = True

    def auto_solve(self):
        self.board = copy.deepcopy(self.solution)
        self.invalid.clear()
        self.won = True

    def _check_invalid(self):
        self.invalid.clear()
        for r in range(9):
            for c in range(9):
                v = self.board[r][c]
                if v == 0:
                    continue
                self.board[r][c] = 0
                if not _valid(self.board, r, c, v):
                    self.invalid.add((r, c))
                self.board[r][c] = v

    def elapsed(self):
        secs = int(time.time() - self.start)
        return f"{secs // 60:02d}:{secs % 60:02d}"


def cell_from_mouse(pos):
    x, y = pos
    if MARGIN <= x < MARGIN + BOARD_SIZE and 80 <= y < 80 + BOARD_SIZE:
        col = (x - MARGIN) // CELL
        row = (y - 80) // CELL
        return int(row), int(col)
    return None


def main():
    pygame.init()

    fonts = {
        "num":   pygame.font.SysFont("monospace", 32, bold=True),
        "small": pygame.font.SysFont("monospace", 20),
        "title": pygame.font.SysFont("monospace", 26, bold=True),
        "btn":   pygame.font.SysFont("monospace", 18, bold=True),
    }

    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()

    difficulty = "medium"
    game = Game(difficulty)

    btn_w, btn_h = 140, 38
    btn_new   = pygame.Rect(W//2 - 220, H - 100, btn_w, btn_h)
    btn_hint  = pygame.Rect(W//2 - 70,  H - 100, btn_w, btn_h)
    btn_solve = pygame.Rect(W//2 + 80,  H - 100, btn_w, btn_h)

    diff_btns = {
        "easy":   pygame.Rect(MARGIN,        H - 52, 110, 30),
        "medium": pygame.Rect(MARGIN + 120,  H - 52, 110, 30),
        "hard":   pygame.Rect(MARGIN + 240,  H - 52, 110, 30),
    }

    while True:
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                cell = cell_from_mouse(event.pos)
                if cell:
                    game.select(*cell)
                elif btn_new.collidepoint(event.pos):
                    game = Game(difficulty)
                elif btn_hint.collidepoint(event.pos):
                    game.hint()
                elif btn_solve.collidepoint(event.pos):
                    game.auto_solve()
                else:
                    for diff, rect in diff_btns.items():
                        if rect.collidepoint(event.pos):
                            difficulty = diff
                            game = Game(difficulty)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.selected = None
                elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                    game.place(0)
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    game.place(event.key - pygame.K_0)
                elif game.selected:
                    r, c = game.selected
                    if event.key == pygame.K_UP:    game.selected = (max(0, r-1), c)
                    elif event.key == pygame.K_DOWN:  game.selected = (min(8, r+1), c)
                    elif event.key == pygame.K_LEFT:  game.selected = (r, max(0, c-1))
                    elif event.key == pygame.K_RIGHT: game.selected = (r, min(8, c+1))

        # ── draw ──────────────────────────────────────────────────────────────
        screen.fill(PANEL)

        blit_centered(screen, fonts["title"], "S U D O K U", DARK, (W//2, 30))
        blit_topleft(screen, fonts["small"], game.elapsed(), DARK, (MARGIN, 55))
        blit_topright(screen, fonts["small"], f"hints: {game.hints}", DARK,
                      (MARGIN + BOARD_SIZE, 55))

        draw_board(screen, fonts, game.board, game.original, game.selected, game.invalid)

        draw_button(screen, fonts, btn_new,   "New Game",  GREEN,          btn_new.collidepoint(mx, my))
        draw_button(screen, fonts, btn_hint,  "  Hint  ",  BLUE,           btn_hint.collidepoint(mx, my))
        draw_button(screen, fonts, btn_solve, "  Solve  ", (150, 80, 180), btn_solve.collidepoint(mx, my))

        diff_colors = {"easy": (80,170,90), "medium": (200,140,40), "hard": (190,60,60)}
        for diff, rect in diff_btns.items():
            active = difficulty == diff
            color = diff_colors[diff]
            shade = tuple(max(0, c - 40) for c in color) if active else color
            pygame.draw.rect(screen, shade, rect, border_radius=6)
            if active:
                pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
            blit_centered(screen, fonts["small"], diff, WHITE, rect.center)

        if game.won:
            banner = pygame.Surface((420, 60), pygame.SRCALPHA)
            banner.fill((50, 200, 100, 210))
            blit_centered(banner, fonts["title"],
                          f"Solved!  {game.elapsed()}  hints:{game.hints}",
                          WHITE, (210, 30))
            screen.blit(banner, banner.get_rect(center=(W//2, H//2)))

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
