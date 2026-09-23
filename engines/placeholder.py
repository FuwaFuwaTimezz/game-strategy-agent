"""StrategyEngine 的占位实现。

V0-B 不真正计算策略，只从当前状态里挑第一个可选动作返回，
用来验证 Route -> Service -> Engine 这条链路能跑通。
将来换成规则引擎 / 搜索 / LLM 时，只替换这个类，其它层不变。
"""
from schemas import Recommendation


class PlaceholderEngine:
    name = "placeholder-v0"

    def analyze(self, state: dict, goal: str, query: str | None) -> list[Recommendation]:
        actions = state.get("valid_actions", [])
        if not actions:
            return []
        first = actions[0]
        return [
            Recommendation(
                rank=1,
                action=first,
                confidence=0.5,
                rationale="占位引擎：返回第一个可选动作（未做真实策略计算）",
            )
        ]
