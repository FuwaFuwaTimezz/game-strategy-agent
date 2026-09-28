"""程序内部模拟实验环境（供未来 LLM 策略做实验）。

模块职责：
    GameState   —— 当前游戏状态（不可变快照）
    GameRules   —— 游戏规则（合法动作 / 胜负 / 结束）
    Simulator   —— 模拟动作执行、跑完整局
    Reward      —— 单局客观结果（Win +1 / Draw 0 / Loss -1）
    Evaluation  —— 多局表现汇总
    Memory      —— 实验记录保存与读取

未来 LLM 策略以 callable(state) -> action 接入 Simulator.play_game。
"""
from simulation.state import GameState
from simulation.rules import GameRules
from simulation.simulator import Simulator, IllegalActionError
from simulation.reward import GameResult, reward_for
from simulation.evaluation import Evaluation
from simulation.memory import Memory

__all__ = [
    "GameState",
    "GameRules",
    "Simulator",
    "IllegalActionError",
    "GameResult",
    "reward_for",
    "Evaluation",
    "Memory",
]
