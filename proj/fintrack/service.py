from .models import Transaction, TransactionType
from .storage import JsonStorage


class FinanceService:
    def __init__(self, storage: JsonStorage):
        self.storage = storage

    def list_transactions(self) -> list[Transaction]:
        return sorted(
            self.storage.load(),
            key=lambda transaction: transaction.date,
            reverse=True,
        )

    def add_transaction(
        self,
        description: str,
        amount: float,
        category: str,
        transaction_type: TransactionType,
    ) -> Transaction:
        transactions = self.storage.load()
        next_id = max((transaction.id for transaction in transactions), default=0) + 1

        transaction = Transaction.create(
            transaction_id=next_id,
            description=description,
            amount=amount,
            category=category,
            transaction_type=transaction_type,
        )

        transactions.append(transaction)
        self.storage.save(transactions)

        return transaction

    def summary(self) -> dict:
        transactions = self.storage.load()

        income = sum(
            transaction.amount
            for transaction in transactions
            if transaction.transaction_type == "income"
        )
        expenses = sum(
            transaction.amount
            for transaction in transactions
            if transaction.transaction_type == "expense"
        )

        return {
            "income": income,
            "expenses": expenses,
            "balance": income - expenses,
            "count": len(transactions),
        }

    def categories(self) -> dict[str, float]:
        result: dict[str, float] = {}

        for transaction in self.storage.load():
            if transaction.transaction_type != "expense":
                continue

            result[transaction.category] = (
                result.get(transaction.category, 0) + transaction.amount
            )

        return dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
