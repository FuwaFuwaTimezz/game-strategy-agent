"""Result / Reward：由游戏结果直接确定的客观奖励。

Win = +1，Draw = 0，Loss = -1。不加入任何人为策略偏好。
"""
from dataclasses import dataclass

from simulation.state import GameState


@dataclass(frozen=True)
class GameResult:
    """一局结束后的结果：终局状态 + 每手之后的状态序列。"""

    final_state: GameState
    history: list

    def reward_for(self, player: str) -> float:
        """从 player 视角的奖励。"""
        return reward_for(self.final_state, player)


def reward_for(state: GameState, player: str) -> float:
    """从 player 视角计算奖励：胜 +1 / 平 0 / 负 -1。"""
    if state.winner is None:
        return 0.0
    return 1.0 if state.winner == player else -1.0
