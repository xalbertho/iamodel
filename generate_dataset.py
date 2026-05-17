import random
import numpy as np
from tqdm import trange
from sudoku import generate_full_board


def generate_dataset(n_samples: int, empty_min: int = 20, empty_max: int = 50) -> tuple:
    puzzles = np.zeros((n_samples, 81), dtype=np.int8)
    solutions = np.zeros((n_samples, 81), dtype=np.int8)
    for i in trange(n_samples, desc="Generating"):
        full = generate_full_board()
        sol = np.array(full, dtype=np.int8).flatten()
        puz = sol.copy()
        n_empty = random.randint(empty_min, empty_max)
        puz[random.sample(range(81), n_empty)] = 0
        puzzles[i] = puz
        solutions[i] = sol
    return puzzles, solutions


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=20_000)
    parser.add_argument("--out", type=str, default="data")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    puzzles, solutions = generate_dataset(args.n)
    np.save(f"{args.out}/puzzles.npy", puzzles)
    np.save(f"{args.out}/solutions.npy", solutions)
    print(f"Saved {args.n} samples to {args.out}/")
