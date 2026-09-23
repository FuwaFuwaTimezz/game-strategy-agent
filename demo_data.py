"""
V0-A 的内存 Demo 数据。

特点：
- 进程启动时加载进内存，进程结束就消失，重启后回到这份初始数据。
- 未来接入真实游戏时，这个文件会被"GameAdapter"替换，
  而 main.py 里的接口代码不需要改动（那是后续版本的事，现在只做 V0-A）。
"""

# 游戏列表：GET /games 返回的就是这个
GAMES = [
    {
        "id": "demo-tictactoe",
        "title": "井字棋 Demo",
        "genre": "board",
        "description": "用于演示接口的内存井字棋",
    },
]

# 游戏状态表：GET /games/{game_id}/state 会根据 game_id 到这里查。
# 井字棋棋盘用长度为 9 的列表表示 3x3 网格，索引 0~8 对应：
#   0 1 2
#   3 4 5
#   6 7 8
GAME_STATES = {
    "demo-tictactoe": {
        "game_id": "demo-tictactoe",
        "turn": "X",                    # 当前轮到谁
        "board": ["X", "O", "", "X", "", "", "", "", ""],
        "winner": None,                 # 还没有赢家
        "phase": "playing",             # 对局进行中
        "valid_actions": [              # 当前所有可选落子位置（空位）
            {"action_id": "place-2", "type": "place", "cell": 2, "player": "X"},
            {"action_id": "place-4", "type": "place", "cell": 4, "player": "X"},
            {"action_id": "place-5", "type": "place", "cell": 5, "player": "X"},
            {"action_id": "place-6", "type": "place", "cell": 6, "player": "X"},
            {"action_id": "place-7", "type": "place", "cell": 7, "player": "X"},
            {"action_id": "place-8", "type": "place", "cell": 8, "player": "X"},
        ],
    },
}
