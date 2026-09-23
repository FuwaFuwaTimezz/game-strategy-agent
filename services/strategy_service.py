"""Service 层：业务编排，不依赖 FastAPI，也不直接依赖 demo_data。

职责：通过 GameAdapter 取状态 -> 调用 StrategyEngine -> 组装 StrategyResult。
"""
from schemas import StrategyRequest, StrategyResult
from engines.placeholder import PlaceholderEngine
from adapters.demo import DemoGameAdapter


class GameNotFoundError(Exception):
    """内部异常：game_id 不存在（由 Route 层统一转成 404）。"""

    def __init__(self, game_id: str):
        self.game_id = game_id
        super().__init__(f"game not found: {game_id}")


class StrategyService:
    def __init__(self, engine=None, adapter=None):
        # 依赖注入：默认用占位引擎和 demo 适配器，将来换真实实现只改装配处
        self.engine = engine or PlaceholderEngine()
        self.adapter = adapter or DemoGameAdapter()

    def analyze(self, request: StrategyRequest) -> StrategyResult:
        # 通过 GameAdapter 取状态，不再直接 import demo_data
        state = self.adapter.get_state(request.game_id)
        if state is None:
            raise GameNotFoundError(request.game_id)

        recommendations = self.engine.analyze(
            state=state,
            goal=request.goal,
            query=request.query,
        )

        return StrategyResult(
            game_id=request.game_id,
            engine=self.engine.name,
            analysis="占位分析：当前引擎未做真实策略计算。",
            recommendations=recommendations,
        )
