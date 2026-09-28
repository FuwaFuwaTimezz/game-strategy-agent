"""v0.4 验证脚本：验证 simulation 包各模块正确。

运行：.venv/Scripts/python.exe verify_simulation.py
纯 Python assert + try-except，不依赖 pytest。
"""
import os
import random

from simulation import (
    GameState,
    GameRules,
    Simulator,
    IllegalActionError,
    Evaluation,
    Memory,
    reward_for,
)
from simulation.simulator import GameOverError


def check_state_and_rules():
    s = GameState.empty()
    assert s.board == ("",) * 9
    assert s.turn == "X"
    assert s.done is False and s.winner is None
    assert GameRules.legal_actions(s) == list(range(9))

    s2 = GameRules.apply(s, 4)
    assert s2.board[4] == "X"
    assert s2.turn == "O"
    assert s2.done is False
    # 原状态未被修改（不可变）
    assert s.board == ("",) * 9 and s.board[4] == ""
    print("[OK] GameState / GameRules")


def check_simulator_transition():
    sim = Simulator()
    s = GameState.empty()
    nxt = sim.step(s, 4)
    assert nxt.board[4] == "X" and nxt.turn == "O"
    assert s.board[4] == ""  # 原状态不变

    # 非法：落已有子的格子
    try:
        sim.step(nxt, 4)
        raise AssertionError("应抛 IllegalActionError")
    except IllegalActionError:
        pass
    # 非法：越界
    try:
        sim.step(s, 9)
        raise AssertionError("应抛 IllegalActionError")
    except IllegalActionError:
        pass
    # 对局已结束仍落子 → 抛 GameOverError
    done_state = GameState(board=("X", "X", "X", "O", "O", "", "", "", ""),
                           turn="O", winner="X", done=True)
    try:
        sim.step(done_state, 6)
        raise AssertionError("应抛 GameOverError")
    except GameOverError:
        pass
    print("[OK] Simulator.step")


def check_win_and_draw():
    win_board = ("X", "X", "X", "O", "O", "", "", "", "")
    assert GameRules.winner_of(win_board) == "X"
    assert GameRules.is_done(win_board) is True

    draw_board = ("X", "O", "X", "X", "O", "O", "O", "X", "X")
    assert GameRules.winner_of(draw_board) is None
    assert GameRules.is_done(draw_board) is True
    print("[OK] 胜负 / 平局判断")


def check_reward():
    win = GameState(board=("X", "X", "X", "O", "O", "", "", "", ""),
                    turn="O", winner="X", done=True)
    assert reward_for(win, "X") == 1.0
    assert reward_for(win, "O") == -1.0

    draw = GameState(board=("X", "O", "X", "X", "O", "O", "O", "X", "X"),
                     turn="X", winner=None, done=True)
    assert reward_for(draw, "X") == 0.0
    assert reward_for(draw, "O") == 0.0
    print("[OK] Reward")


def check_evaluation():
    e = Evaluation()
    e.record(1.0)
    e.record(0.0)
    e.record(-1.0)
    e.record(1.0)
    assert (e.wins, e.draws, e.losses) == (2, 1, 1)
    assert e.total == 4
    assert abs(e.win_rate - 0.5) < 1e-9
    print("[OK] Evaluation")


def check_memory():
    path = "experiments/verify_records.jsonl"
    if os.path.exists(path):
        os.remove(path)
    m = Memory(path)
    m.save({"strategy": "A", "experiment_id": 1, "winner": "X"})
    m.save({"strategy": "B", "experiment_id": 2, "winner": "O"})
    m.save({"strategy": "A", "experiment_id": 3, "winner": None})

    all_records = m.load()
    assert len(all_records) == 3
    a_records = m.load(strategy="A")
    assert len(a_records) == 2
    assert all(r["strategy"] == "A" for r in a_records)
    os.remove(path)
    print("[OK] Memory")


def check_play_game():
    random.seed(42)

    def random_strategy(state):
        return random.choice(GameRules.legal_actions(state))

    sim = Simulator()
    result = sim.play_game(random_strategy, random_strategy)
    assert result.final_state.done is True
    non_empty = sum(1 for c in result.final_state.board if c != "")
    assert len(result.history) == non_empty
    print("[OK] Simulator.play_game（跑完整局）")


if __name__ == "__main__":
    check_state_and_rules()
    check_simulator_transition()
    check_win_and_draw()
    check_reward()
    check_evaluation()
    check_memory()
    check_play_game()
    print("\nALL CHECKS PASSED")
