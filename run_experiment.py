"""运行 Rule vs Random 多局对战实验的入口脚本。

用法：
    .venv/Scripts/python.exe run_experiment.py --games 1000 --seed 42

统计始终从 Rule（第一个参数 strategy_a）的视角统计。
"""
import argparse

from simulation.rule_strategy import rule_strategy
from simulation.random_strategy import random_strategy
from simulation.experiment import run_match


def _print_eval(label: str, e):
    print(f"[{label}] 胜 {e.wins} / 平 {e.draws} / 负 {e.losses}"
          f" | 胜率 {e.win_rate * 100:.2f}%")


def main():
    parser = argparse.ArgumentParser(description="Rule vs Random 多局对战实验")
    parser.add_argument("--games", type=int, default=1000,
                        help="总局数（正整数，建议偶数以保证先后手均衡）")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    args = parser.parse_args()

    report = run_match(rule_strategy, random_strategy, args.games, args.seed)

    print(f"Rule vs Random（N={report.n_games}，seed={args.seed}）")
    _print_eval("总", report.total)
    _print_eval("先手(执 X)", report.as_x)
    _print_eval("后手(执 O)", report.as_o)


if __name__ == "__main__":
    main()
