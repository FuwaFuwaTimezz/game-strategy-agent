"""Demo 游戏的具体 Adapter：封装 demo_data 的访问。

v0.3 引入 GameAdapter 的意义：让 Service 和 Route 不再直接 import demo_data，
而是通过这个 adapter 获取游戏数据。将来接入真实游戏时，新增一个 adapter 即可，
Service 和 Route 不用改。
"""
from demo_data import GAMES, GAME_STATES


class DemoGameAdapter:
    """demo 数据的具体适配器（当前只有 demo-tictactoe 一个游戏）。"""

    def list_games(self) -> list[dict]:
        """返回游戏列表（对应 GET /games）。"""
        return GAMES

    def get_state(self, game_id: str) -> dict | None:
        """返回指定游戏的状态；找不到返回 None。"""
        return GAME_STATES.get(game_id)
