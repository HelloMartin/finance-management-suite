import os

import typer
from rich.console import Console
from rich.table import Table

from finance_suite.account import Account
from finance_suite.database import add_account, get_all_accounts, setup_database

app = typer.Typer()
account_app = typer.Typer()
console = Console()

app.add_typer(account_app, name="account")


def get_db_path() -> str:
    return os.getenv("FINANCE_DB_PATH", "db.sqlite3")


@app.callback()
def callback() -> None:
    """Finance Management Suite CLI."""


@app.command()
def hello() -> None:
    """Small command to verify the CLI works."""
    typer.echo("Finance Management Suite")


@account_app.command("create")
def create_account(name: str, currency: str) -> None:
    """Create an account."""
    db_path = get_db_path()
    setup_database(db_path=db_path)

    account = Account(name=name, currency=currency)
    add_account(account=account, db_path=db_path)

    table = Table("ID", "Name", "Currency")
    table.add_row(str(account.id), account.name, account.currency)
    console.print(table)


@account_app.command("list")
def list_accounts() -> None:
    """List all accounts."""

    db_path = get_db_path()
    setup_database(db_path=db_path)

    accounts = get_all_accounts(db_path=db_path)
    table = Table("ID", "Name", "Currency")

    for account in accounts:
        table.add_row(str(account.id), account.name, account.currency)

    console.print(table)


def main() -> None:
    app()
