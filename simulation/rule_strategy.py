"""Rule Strategy：规则策略（确定性）。

优先级：
1. 立即获胜（自己补第三子）
2. 阻挡对手立即获胜
3. 占据中心
4. 固定顺序占角落
5. 固定顺序占边缘

与 random_strategy 同签名（state -> int），可直接接入 Simulator.play_game。
"""
from simulation.rules import GameRules


def rule_strategy(state):
    """给定当前状态，返回一个落子位置（int）。

    参数 state：simulation.state.GameState（当前棋盘，done 应为 False）
    返回：int，一个空位索引
    """
    board = state.board
    player = state.turn
    opponent = "O" if player == "X" else "X"
    empty = state.empty_cells

    # 1. 立即获胜
    for cell in empty:
        b = list(board)
        b[cell] = player
        if GameRules.winner_of(b) == player:
            return cell

    # 2. 阻挡对手
    for cell in empty:
        b = list(board)
        b[cell] = opponent
        if GameRules.winner_of(b) == opponent:
            return cell

    # 3. 中心
    if 4 in empty:
        return 4

    # 4. 角落（固定顺序）
    for cell in (0, 2, 6, 8):
        if cell in empty:
            return cell

    # 5. 边缘（固定顺序）
    for cell in (1, 3, 5, 7):
        if cell in empty:
            return cell

    # 6. 兜底：无合法落子（正常对局不会走到这里）
    raise ValueError("no legal move")
