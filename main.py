"""
v0.3：引入 GameAdapter，让 Route 和 Service 不再直接依赖 demo_data。

分层：
    Route（main.py） -> Service（services/） -> GameAdapter（adapters/）
    Route（main.py） -> GameAdapter（adapters/）   # 三个 GET 直接走 adapter
    Service -> StrategyEngine（engines/）

启动方式（在项目目录下执行）：
    .venv/Scripts/python.exe -m uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException
from schemas import GameSummary, GameState, StrategyRequest, StrategyResult
from adapters.demo import DemoGameAdapter
from services.strategy_service import StrategyService, GameNotFoundError

# 创建 FastAPI 应用实例。title 只是显示在自动文档页上的标题。
app = FastAPI(title="Game Strategy & Play Agent (v0.3)")

# 游戏数据访问的唯一入口（当前只有 demo 数据）
demo_adapter = DemoGameAdapter()
strategy_service = StrategyService(adapter=demo_adapter)


# ============ v0.1 的三个 GET 接口 ============


@app.get("/health")
def health() -> dict:
    """存活检查：不依赖任何数据，服务能响应就返回 ok。"""
    return {"status": "ok", "version": "0.3.0"}


@app.get("/games", response_model=list[GameSummary])
def list_games() -> list[GameSummary]:
    """返回游戏列表，数据通过 demo_adapter 取。"""
    return demo_adapter.list_games()


@app.get("/games/{game_id}/state", response_model=GameState)
def get_game_state(game_id: str) -> GameState:
    """根据 game_id 返回游戏状态；找不到就返回 404。"""
    state = demo_adapter.get_state(game_id)
    if state is None:
        raise HTTPException(status_code=404, detail=f"game not found: {game_id}")
    return state


# ============ v0.2 新增的 POST 接口 ============


@app.post("/strategy/analyze", response_model=StrategyResult)
def analyze_strategy(request: StrategyRequest) -> StrategyResult:
    """策略分析：Route -> Service -> GameAdapter + StrategyEngine。"""
    try:
        return strategy_service.analyze(request)
    except GameNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
