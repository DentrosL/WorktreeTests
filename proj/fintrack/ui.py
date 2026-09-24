from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .service import FinanceService


class FinanceUI:
    def __init__(self, service: FinanceService):
        self.service = service
        self.console = Console()

    def run(self):
        while True:
            self._header()
            self._menu()

            option = input("\nEscolha uma opção: ").strip()

            if option == "1":
                self._add_transaction()
            elif option == "2":
                self._list_transactions()
            elif option == "3":
                self._show_summary()
            elif option == "4":
                self._show_categories()
            elif option == "5":
                self._show_dashboard()
            elif option == "0":
                self.console.print("\nAté mais!")
                return
            else:
                self.console.print("[red]Opção inválida.[/red]")

            input("\nPressione Enter para continuar...")

    def _header(self):
        self.console.clear()
        self.console.print(
            Panel.fit(
                "[bold cyan]FinTrack[/bold cyan]\n"
                "[dim]Controle financeiro pessoal[/dim]",
                border_style="cyan",
            )
        )

    def _menu(self):
        self.console.print(
            "\n[bold]1[/bold] - Adicionar lançamento\n"
            "[bold]2[/bold] - Listar lançamentos\n"
            "[bold]3[/bold] - Resumo financeiro\n"
            "[bold]4[/bold] - Ver categorias\n"
            "[bold]5[/bold] - Dashboard\n"
            "[bold]0[/bold] - Sair"
        )

    def _add_transaction(self):
        self.console.print("\n[bold]Novo lançamento[/bold]")

        description = input("Descrição: ").strip()
        amount = self._read_amount()
        category = input("Categoria: ").strip() or "Outros"

        transaction_type = input(
            "Tipo (receita/despesa): "
        ).strip().lower()

        if transaction_type not in {"r", "d"}:
            self.console.print("[red]Tipo inválido.[/red]")
            return

        self.service.add_transaction(
            description=description,
            amount=amount,
            category=category,
            transaction_type="income" if transaction_type == "r" else "expense",
        )

        self.console.print("[green]Lançamento adicionado com sucesso![/green]")

    def _read_amount(self) -> float:
        while True:
            try:
                value = input("Valor: R$ ").replace(",", ".")
                amount = float(value)

                if amount <= 0:
                    raise ValueError

                return amount
            except ValueError:
                self.console.print("[red]Digite um valor maior que zero.[/red]")

    def _list_transactions(self):
        transactions = self.service.list_transactions()

        table = Table(title="Lançamentos")
        table.add_column("ID", justify="right")
        table.add_column("Data")
        table.add_column("Descrição")
        table.add_column("Categoria")
        table.add_column("Tipo")
        table.add_column("Valor", justify="right")

        for transaction in transactions:
            color = "green" if transaction.transaction_type == "income" else "red"
            label = "Receita" if transaction.transaction_type == "income" else "Despesa"

            table.add_row(
                str(transaction.id),
                transaction.date,
                transaction.description,
                transaction.category,
                f"[{color}]{label}[/{color}]",
                f"R$ {transaction.amount:.2f}",
            )

        self.console.print(table)

    def _show_summary(self):
        summary = self.service.summary()

        table = Table(title="Resumo financeiro")
        table.add_column("Indicador")
        table.add_column("Valor", justify="right")

        table.add_row("Receitas", f"R$ {summary['income']:.2f}")
        table.add_row("Despesas", f"R$ {summary['expenses']:.2f}")
        table.add_row("Saldo", f"R$ {summary['balance']:.2f}")
        table.add_row("Lançamentos", str(summary["count"]))

        self.console.print(table)

    def _show_categories(self):
        categories = self.service.categories()

        if not categories:
            self.console.print("[dim]Nenhuma despesa cadastrada.[/dim]")
            return

        table = Table(title="Despesas por categoria")
        table.add_column("Categoria")
        table.add_column("Total", justify="right")

        for category, amount in categories.items():
            table.add_row(category, f"R$ {amount:.2f}")

        self.console.print(table)

    def _show_dashboard(self):
        dashboard = self.service.dashboard()
        summary = dashboard["summary"]

        cards = Columns(
            [
                Panel(
                    f"[green]R$ {summary['income']:.2f}[/green]",
                    title="Receitas",
                    border_style="green",
                ),
                Panel(
                    f"[red]R$ {summary['expenses']:.2f}[/red]",
                    title="Despesas",
                    border_style="red",
                ),
                Panel(
                    f"[cyan]R$ {summary['balance']:.2f}[/cyan]",
                    title="Saldo",
                    border_style="cyan",
                ),
            ]
        )

        self.console.print("\n")
        self.console.print(
            Panel(
                cards,
                title="[bold cyan]Dashboard Financeiro[/bold cyan]",
                border_style="cyan",
            )
        )

        recent_table = Table(title="Últimos lançamentos")

        recent_table.add_column("Data")
        recent_table.add_column("Descrição")
        recent_table.add_column("Categoria")
        recent_table.add_column("Tipo")
        recent_table.add_column("Valor", justify="right")

        for transaction in dashboard["recent_transactions"]:
            color = (
                "green"
                if transaction.transaction_type == "income"
                else "red"
            )

            label = (
                "Receita"
                if transaction.transaction_type == "income"
                else "Despesa"
            )

            recent_table.add_row(
                transaction.date,
                transaction.description,
                transaction.category,
                f"[{color}]{label}[/{color}]",
                f"R$ {transaction.amount:.2f}",
            )

        self.console.print(recent_table)

        categories_table = Table(title="Principais categorias de despesa")

        categories_table.add_column("Categoria")
        categories_table.add_column("Total", justify="right")

        for category, amount in dashboard["categories"].items():
            categories_table.add_row(
                category,
                f"R$ {amount:.2f}",
            )

        self.console.print(categories_table)