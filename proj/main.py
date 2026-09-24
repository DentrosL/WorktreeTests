from fintrack.service import FinanceService
from fintrack.storage import JsonStorage
from fintrack.ui import FinanceUI


def main():
    storage = JsonStorage("data/transactions.json")
    service = FinanceService(storage)
    ui = FinanceUI(service)
    ui.run()


if __name__ == "__main__":
    main()
