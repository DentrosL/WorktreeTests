from dataclasses import asdict, dataclass
from datetime import date
from typing import Literal

TransactionType = Literal["income", "expense"]

@dataclass
class Transaction:
    id: int
    description: str
    amount: float
    category: str
    transaction_type: TransactionType
    date: str

    @property
    def signed_amount(self) -> float:
        return self.amount if self.transaction_type == "income" else -self.amount

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(**data)

    @classmethod
    def create(
        cls,
        transaction_id: int,
        description: str,
        amount: float,
        category: str,
        transaction_type: TransactionType,
    ) -> "Transaction":
        return cls(
            id=transaction_id,
            description=description,
            amount=amount,
            category=category,
            transaction_type=transaction_type,
            date=date.today().isoformat(),
        )
