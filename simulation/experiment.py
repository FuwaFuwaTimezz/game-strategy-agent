"""Experiment：多局策略对战与评估。

复用 Simulator、GameResult、Evaluation，批量运行两个策略的对战，
从第一个策略（strategy_a）的视角统计表现。
"""
import random
from dataclasses import dataclass

from simulation.simulator import Simulator
from simulation.evaluation import Evaluation


@dataclass
class MatchReport:
    """一批对战的结果。

    统计语义：始终统计第一个参数 strategy_a 的表现。

    total: strategy_a 的总表现（胜/平/负、胜率）
    as_x:  strategy_a 执 X（先手）时的表现
    as_o:  strategy_a 执 O（后手）时的表现
    """

    n_games: int
    total: Evaluation
    as_x: Evaluation
    as_o: Evaluation


def run_match(strategy_a, strategy_b, n_games, seed=None):
    """运行 n_games 局 strategy_a vs strategy_b，返回 MatchReport。

    先手分配（确定性，保证可复现）：
      偶数局（i % 2 == 0）→ strategy_a 执 X（先手）
      奇数局（i % 2 == 1）→ strategy_a 执 O（后手）

    统计口径：每局用 result.reward_for(a_player) 得到 strategy_a 视角的
    奖励（胜 +1 / 平 0 / 负 -1），再累计进 Evaluation。

    可复现：入口处调用 random.seed(seed) 一次。除设置种子外，本函数
    内部不做任何随机操作，先后手用奇偶确定，因此同 seed 结果完全一致。
    """
    if isinstance(n_games, bool) or not isinstance(n_games, int) or n_games <= 0:
        raise ValueError(f"n_games 必须是正整数，得到 {n_games!r}")

    if seed is not None:
        random.seed(seed)

    sim = Simulator()
    total = Evaluation()
    as_x = Evaluation()
    as_o = Evaluation()

    for i in range(n_games):
        if i % 2 == 0:
            x_strategy, o_strategy = strategy_a, strategy_b
            a_player = "X"
        else:
            x_strategy, o_strategy = strategy_b, strategy_a
            a_player = "O"

        result = sim.play_game(x_strategy, o_strategy)
        reward = result.reward_for(a_player)

        total.record(reward)
        if a_player == "X":
            as_x.record(reward)
        else:
            as_o.record(reward)

    return MatchReport(n_games=n_games, total=total, as_x=as_x, as_o=as_o)
