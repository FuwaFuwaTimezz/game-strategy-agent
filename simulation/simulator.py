"""Simulator：模拟动作执行，不修改原始状态。"""
from simulation.state import GameState
from simulation.rules import GameRules
from simulation.reward import GameResult


class IllegalActionError(Exception):
    """落子非法时抛出。"""


class GameOverError(Exception):
    """对局已结束仍尝试落子时抛出。"""


class Simulator:
    def __init__(self, rules=None):
        self.rules = rules or GameRules()

    def step(self, state: GameState, action: int) -> GameState:
        """给定 state + action，返回新 state；对局已结束或动作非法抛异常。"""
        if state.done:
            raise GameOverError()
        if not self.rules.is_legal(state, action):
            raise IllegalActionError(action)
        return self.rules.apply(state, action)

    def play_game(self, strategy_x, strategy_o) -> GameResult:
        """双方按各自策略下完一局，返回 GameResult。

        strategy 是 callable(state) -> action，是给未来 LLM 策略预留的
        最小接口，不定义任何 Strategy 基类。
        """
        state = GameState.empty()
        history = []
        while not state.done:
            strategy = strategy_x if state.turn == "X" else strategy_o
            state = self.step(state, strategy(state))
            history.append(state)
        return GameResult(final_state=state, history=history)
