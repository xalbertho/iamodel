import argparse
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, random_split
from tqdm import trange, tqdm

from sudoku_model import SudokuNet


def load_data(data_dir: str):
    puzzles = torch.from_numpy(np.load(f"{data_dir}/puzzles.npy")).long()
    solutions = torch.from_numpy(np.load(f"{data_dir}/solutions.npy")).long()
    # targets: 0-8 (digit-1) for cross-entropy
    targets = solutions - 1
    return puzzles, targets


def accuracy_on_empty(logits, targets, puzzles):
    """Cell accuracy only for cells that were empty in the puzzle."""
    preds = logits.argmax(-1)           # (B, 81)
    mask = puzzles == 0                 # (B, 81) True where cell was empty
    if mask.sum() == 0:
        return 0.0
    correct = ((preds == targets) & mask).sum().item()
    return correct / mask.sum().item()


def train(args):
    device = torch.device("cpu")
    puzzles, targets = load_data(args.data)

    dataset = TensorDataset(puzzles, targets)
    val_size = int(len(dataset) * 0.1)
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size],
                                    generator=torch.Generator().manual_seed(42))

    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=0)
    val_dl = DataLoader(val_ds, batch_size=args.batch, shuffle=False, num_workers=0)

    model = SudokuNet(channels=128, n_blocks=4).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    criterion = nn.CrossEntropyLoss()

    best_val_acc = 0.0
    print(f"Training on {train_size} samples, validating on {val_size}")

    for epoch in trange(1, args.epochs + 1, desc="Epochs"):
        model.train()
        train_loss = 0.0
        for puz, tgt in tqdm(train_dl, desc=f"  Ep{epoch}", leave=False):
            puz, tgt = puz.to(device), tgt.to(device)
            logits = model(puz)                             # (B, 81, 9)
            loss = criterion(logits.view(-1, 9), tgt.view(-1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * puz.size(0)
        scheduler.step()
        train_loss /= train_size

        model.eval()
        val_loss, val_acc = 0.0, 0.0
        with torch.no_grad():
            for puz, tgt in val_dl:
                puz, tgt = puz.to(device), tgt.to(device)
                logits = model(puz)
                val_loss += criterion(logits.view(-1, 9), tgt.view(-1)).item() * puz.size(0)
                val_acc += accuracy_on_empty(logits, tgt, puz) * puz.size(0)
        val_loss /= val_size
        val_acc /= val_size

        tqdm.write(f"Ep {epoch:2d} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | empty_acc={val_acc:.3f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), args.out)

    print(f"\nBest empty-cell accuracy: {best_val_acc:.3f} — model saved to {args.out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch", type=int, default=256)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--out", default="model.pth")
    train(parser.parse_args())
