"""Evaluation：多局实验的整体表现（胜/平/负、胜率）。"""
from dataclasses import dataclass


@dataclass
class Evaluation:
    wins: int = 0
    draws: int = 0
    losses: int = 0

    @property
    def total(self) -> int:
        return self.wins + self.draws + self.losses

    @property
    def win_rate(self) -> float:
        return self.wins / self.total if self.total else 0.0

    def record(self, reward: float):
        """根据单局 reward（+1/0/-1）累计胜平负。"""
        if reward > 0:
            self.wins += 1
        elif reward < 0:
            self.losses += 1
        else:
            self.draws += 1
