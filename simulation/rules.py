"""GameRules：井字棋规则。

职责：合法动作、胜负判断、结束判断、落子。全部是纯静态方法，
把游戏规则集中在一处，不散落到其他模块。
"""
from simulation.state import GameState


class GameRules:
    # 8 条获胜线：3 行 + 3 列 + 2 对角线
    WINNING_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]

    @staticmethod
    def legal_actions(state: GameState) -> list[int]:
        """当前所有合法落子位置（空位）。"""
        return [i for i, v in enumerate(state.board) if v == ""]

    @staticmethod
    def is_legal(state: GameState, cell: int) -> bool:
        """cell 是否为合法落子位置。"""
        return 0 <= cell < 9 and state.board[cell] == ""

    @staticmethod
    def winner_of(board) -> str | None:
        """返回赢家（"X"/"O"），无赢家返回 None。"""
        for a, b, c in GameRules.WINNING_LINES:
            if board[a] != "" and board[a] == board[b] == board[c]:
                return board[a]
        return None

    @staticmethod
    def is_done(board) -> bool:
        """是否结束：有赢家，或棋盘已满。"""
        return GameRules.winner_of(board) is not None or all(v != "" for v in board)

    @staticmethod
    def apply(state: GameState, cell: int) -> GameState:
        """在 cell 落子，返回新状态。调用方需保证 cell 合法。"""
        board = list(state.board)
        board[cell] = state.turn
        board = tuple(board)
        winner = GameRules.winner_of(board)
        done = winner is not None or all(v != "" for v in board)
        next_turn = "O" if state.turn == "X" else "X"
        return GameState(board=board, turn=next_turn, winner=winner, done=done)
