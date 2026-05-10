import random
import copy
import time


def generate_full_board():
    board = [[0] * 9 for _ in range(9)]
    _fill(board)
    return board


def _fill(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for n in nums:
                    if _valid(board, row, col, n):
                        board[row][col] = n
                        if _fill(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def _valid(board, row, col, n):
    if n in board[row]:
        return False
    if n in [board[r][col] for r in range(9)]:
        return False
    br, bc = (row // 3) * 3, (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if board[r][c] == n:
                return False
    return True


def _count_solutions(board, limit=2):
    count = [0]

    def solve(b):
        if count[0] >= limit:
            return
        for r in range(9):
            for c in range(9):
                if b[r][c] == 0:
                    for n in range(1, 10):
                        if _valid(b, r, c, n):
                            b[r][c] = n
                            solve(b)
                            b[r][c] = 0
                    return
        count[0] += 1

    solve([row[:] for row in board])
    return count[0]


CLUES = {"easy": 45, "medium": 35, "hard": 25}


def make_puzzle(difficulty="medium"):
    full = generate_full_board()
    puzzle = copy.deepcopy(full)
    cells = list(range(81))
    random.shuffle(cells)
    target_clues = CLUES.get(difficulty, 35)
    removed = 0
    for idx in cells:
        r, c = divmod(idx, 9)
        backup = puzzle[r][c]
        puzzle[r][c] = 0
        if _count_solutions(puzzle) == 1:
            removed += 1
            if 81 - removed <= target_clues:
                break
        else:
            puzzle[r][c] = backup
    return puzzle, full


def print_board(board, original=None):
    print()
    print("    1 2 3   4 5 6   7 8 9")
    print("  +" + "-------+" * 3)
    for r in range(9):
        row_str = f"{r+1} |"
        for c in range(9):
            val = board[r][c]
            if val == 0:
                ch = "."
            elif original and original[r][c] != 0:
                ch = str(val)
            else:
                ch = f"\033[94m{val}\033[0m"  # blue for player entries
            row_str += f" {ch}"
            if c in (2, 5):
                row_str += " |"
        row_str += " |"
        print(row_str)
        if r in (2, 5, 8):
            print("  +" + "-------+" * 3)
    print()


def solve(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                for n in range(1, 10):
                    if _valid(board, r, c, n):
                        board[r][c] = n
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True


def is_complete(board):
    return all(board[r][c] != 0 for r in range(9) for c in range(9))


def play():
    print("\n=== SUDOKU ===")
    difficulty = input("Difficulty (easy / medium / hard) [medium]: ").strip().lower() or "medium"
    if difficulty not in CLUES:
        difficulty = "medium"

    puzzle, solution = make_puzzle(difficulty)
    original = copy.deepcopy(puzzle)
    current = copy.deepcopy(puzzle)
    start = time.time()

    print(f"\nGenerating {difficulty} puzzle...")
    print_board(current, original)
    print("Commands: '<row> <col> <num>'  |  'hint'  |  'solve'  |  'restart'  |  'quit'")

    hints_used = 0

    while True:
        cmd = input("> ").strip().lower()

        if cmd == "quit":
            print("Bye!")
            break

        elif cmd == "restart":
            current = copy.deepcopy(puzzle)
            print_board(current, original)

        elif cmd == "hint":
            empties = [(r, c) for r in range(9) for c in range(9) if current[r][c] == 0]
            if not empties:
                print("Board is already full.")
            else:
                r, c = random.choice(empties)
                current[r][c] = solution[r][c]
                hints_used += 1
                print(f"Hint: row {r+1}, col {c+1} = {solution[r][c]}")
                print_board(current, original)
                if is_complete(current):
                    elapsed = int(time.time() - start)
                    print(f"Solved! Time: {elapsed}s | Hints used: {hints_used}")
                    break

        elif cmd == "solve":
            current = copy.deepcopy(solution)
            print_board(current, original)
            print("Board auto-solved.")
            break

        else:
            parts = cmd.split()
            if len(parts) != 3:
                print("Enter: <row> <col> <num>  (e.g. '3 5 7')")
                continue
            try:
                r, c, n = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
            except ValueError:
                print("Use numbers only.")
                continue
            if not (0 <= r < 9 and 0 <= c < 9 and 1 <= n <= 9):
                print("Row and col must be 1-9, number must be 1-9.")
                continue
            if original[r][c] != 0:
                print("That cell is fixed (part of the original puzzle).")
                continue
            if n != 0 and not _valid(current, r, c, n):
                print(f"{n} is not valid there.")
                continue
            current[r][c] = n
            print_board(current, original)
            if is_complete(current):
                elapsed = int(time.time() - start)
                print(f"Puzzle complete! Time: {elapsed}s | Hints used: {hints_used}")
                break


if __name__ == "__main__":
    play()
