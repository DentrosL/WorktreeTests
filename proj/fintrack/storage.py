import json
from pathlib import Path

from .models import Transaction


class JsonStorage:
    def __init__(self, path: str):
        self.path = Path(path)

    def load(self) -> list[Transaction]:
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [Transaction.from_dict(item) for item in data]

    def save(self, transactions: list[Transaction]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self.path.open("w", encoding="utf-8") as file:
            json.dump(
                [transaction.to_dict() for transaction in transactions],
                file,
                ensure_ascii=False,
                indent=2,
            )
