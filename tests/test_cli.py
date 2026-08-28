from typer.testing import CliRunner

from finance_suite.account import Account
from finance_suite.cli import app
from finance_suite.database import add_account, get_all_accounts, setup_database

runner = CliRunner()


def test_cli_help_exits_successfully():
    """Tests that the CLI --help option displays tool name and usage list"""
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Finance Management Suite CLI." in result.output
    assert "Usage: " in result.output


def test_cli_hello_outputs_app_name():
    """Test that the CLI hello optiono displays the tool name"""
    result = runner.invoke(app, ["hello"])

    assert result.exit_code == 0
    assert "Finance Management Suite" in result.output


def test_cli_account_create(tmp_path, monkeypatch):
    """Test that the CLI creates and displays an account."""

    db_path = tmp_path / "test.sqlite3"
    setup_database(db_path=db_path)
    monkeypatch.setenv(name="FINANCE_DB_PATH", value=str(db_path))

    name: str = "Jon Doe"
    currency: str = "CHF"

    result = runner.invoke(app, ["account", "create", name, currency])

    assert result.exit_code == 0, result.exception
    assert name in result.output
    assert currency in result.output

    accounts = get_all_accounts(db_path=db_path)

    assert len(accounts) == 1
    assert accounts[0].name == name
    assert accounts[0].currency == currency


def test_cli_account_list(tmp_path, monkeypatch):
    """Test that the CLI displays a list of accounts."""

    db_path = tmp_path / "test.sqlite3"
    setup_database(db_path=db_path)
    monkeypatch.setenv(name="FINANCE_DB_PATH", value=str(db_path))

    account = Account(name="Jon Doe", currency="CHF")
    add_account(account=account, db_path=db_path)

    result = runner.invoke(app, ["account", "list"])

    assert result.exit_code == 0, result.exception
    assert str(account.id) in result.output
    assert account.name in result.output
    assert account.currency in result.output
