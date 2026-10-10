"""Random Strategy：随机策略（策略基线）。

这是最基础的策略：给定当前状态，从所有空位里随机挑一个落子。
未来会逐步加入 Rule / Search / LLM 等更聪明的策略，各自独立成一个文件。
"""
import random


def random_strategy(state):
    """给定当前状态，从空位里随机返回一个落子位置（int）。

    参数 state：simulation.state.GameState（当前棋盘）
    返回：int，一个空位索引，例如 4
    """
    return random.choice(state.empty_cells)
