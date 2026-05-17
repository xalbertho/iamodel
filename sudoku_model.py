import torch
import torch.nn as nn
import torch.nn.functional as F


class ResBlock(nn.Module):
    def __init__(self, channels: int):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        return F.relu(out + x)


class SudokuNet(nn.Module):
    """
    Input:  (B, 81) int64 values 0-9  (0 = empty cell)
    Output: (B, 81, 9) logits for digits 1-9
    """

    def __init__(self, channels: int = 128, n_blocks: int = 4):
        super().__init__()
        self.embed = nn.Conv2d(10, channels, 1)
        self.blocks = nn.Sequential(*[ResBlock(channels) for _ in range(n_blocks)])
        self.head = nn.Conv2d(channels, 9, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.view(-1, 9, 9)
        x = F.one_hot(x.long(), 10).permute(0, 3, 1, 2).float()  # (B, 10, 9, 9)
        x = F.relu(self.embed(x))                                  # (B, C, 9, 9)
        x = self.blocks(x)
        x = self.head(x)                                           # (B, 9, 9, 9)
        return x.permute(0, 2, 3, 1).reshape(-1, 81, 9)           # (B, 81, 9)
