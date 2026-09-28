"""Memory：把实验记录追加到本地 JSONL 文件，支持按 strategy 读取。

本地文件方案，不用任何外部数据库。
"""
import json
import os


class Memory:
    def __init__(self, path: str):
        self.path = path

    def save(self, record: dict):
        """把一条实验记录追加为一行 JSON。"""
        directory = os.path.dirname(self.path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def load(self, strategy: str | None = None) -> list[dict]:
        """读取所有记录；指定 strategy 时只返回该策略的记录。"""
        if not os.path.exists(self.path):
            return []
        out = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                if strategy is None or record.get("strategy") == strategy:
                    out.append(record)
        return out
