"""API 数据契约：请求体与响应体的 Pydantic 模型。

为什么单独一个文件：这些模型会被 Route（main.py）、Service、Engine 三处 import，
集中放这里可以避免 main.py 与 service 之间产生循环 import。
"""
from pydantic import BaseModel


# ---- V0-A 已有的模型（从 main.py 原样搬过来，字段不变）----


class GameSummary(BaseModel):
    """GET /games 返回的单个游戏摘要。"""

    id: str
    title: str
    genre: str
    description: str


class GameAction(BaseModel):
    """一个可选动作，例如井字棋里"把 X 放到 2 号格子"。"""

    action_id: str
    type: str
    cell: int | None = None
    player: str | None = None


class GameState(BaseModel):
    """GET /games/{game_id}/state 返回的完整游戏状态。"""

    game_id: str
    turn: str
    board: list[str]
    winner: str | None
    phase: str
    valid_actions: list[GameAction]


# ---- V0-B 新增 ----

class StrategyRequest(BaseModel):
    """POST /strategy/analyze 的请求体。"""

    game_id: str
    goal: str = "win"
    query: str | None = None


class Recommendation(BaseModel):
    """策略引擎给出的一条建议动作。"""

    rank: int
    action: dict
    confidence: float
    rationale: str


class StrategyResult(BaseModel):
    """POST /strategy/analyze 的响应体。"""

    game_id: str
    engine: str
    analysis: str
    recommendations: list[Recommendation]
