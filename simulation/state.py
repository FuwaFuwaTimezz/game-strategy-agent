"""GameState：井字棋状态快照（不可变）。

用 frozen dataclass + tuple 保证不可变，这样 Simulator 反复模拟时
不会改动原始状态。
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    board: tuple             # 9 元素，"" 表示空位，索引 0~8
    turn: str                # "X" / "O"
    winner: str | None       # "X" / "O" / None（平局时 None 且 done=True）
    done: bool               # 是否结束

    @classmethod
    def empty(cls) -> "GameState":
        """初始空盘，X 先手。"""
        return cls(board=("",) * 9, turn="X", winner=None, done=False)

    @property
    def empty_cells(self) -> list[int]:
        """当前所有空位索引。"""
        return [i for i, v in enumerate(self.board) if v == ""]
