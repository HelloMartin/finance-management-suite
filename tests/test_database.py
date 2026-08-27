import sqlite3

from finance_suite.account import Account
from finance_suite.database import (
    add_account,
    get_account_by_id,
    get_all_accounts,
    setup_database,
)


def test_setup_database_creates_accounts_table(tmp_path):
    """Test that setup_database() creates the accounts table."""

    db_path = tmp_path / "test.sqlite3"

    setup_database(db_path=db_path)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(accounts)")
        columns = [row[1] for row in cursor.fetchall()]

        assert columns == [
            "account_id",
            "account_name",
            "account_currency",
        ]


def test_add_and_get_account_by_id(tmp_path):
    """Test that an account can be loaded with all fields, including its original UUID."""

    db_path = tmp_path / "test.sqlite3"

    write_account = Account(name="Jon Doe", currency="CHF")

    setup_database(db_path=db_path)
    add_account(account=write_account, db_path=db_path)

    read_account: Account | None = get_account_by_id(
        uuid_str=str(write_account.id), db_path=db_path
    )

    assert read_account is not None
    assert write_account.id == read_account.id
    assert write_account.name == read_account.name
    assert write_account.currency == read_account.currency


def test_get_account_by_unknown_id_returns_none(tmp_path):
    """Test that requesting an unknown UUID returns None."""

    db_path = tmp_path / "test.sqlite3"

    setup_database(db_path=db_path)
    account = get_account_by_id("569c3039-FAKE-FAKE-FAKE-b6479594c113", db_path=db_path)

    assert account is None


def test_get_all_accounts_returns_all_accounts(tmp_path):
    """Test that get_all_accounts() returns both added accounts."""

    db_path = tmp_path / "test.sqlite3"

    write_account_1 = Account(name="Jon Doe", currency="CHF")
    write_account_2 = Account(name="Marry Doe", currency="USD")

    write_accounts: list[Account] = [write_account_1, write_account_2]

    setup_database(db_path=db_path)
    add_account(account=write_account_1, db_path=db_path)
    add_account(account=write_account_2, db_path=db_path)

    read_accounts: list[Account] = get_all_accounts(db_path=db_path)

    assert len(write_accounts) == len(read_accounts)
    assert {a.id for a in write_accounts} == {a.id for a in read_accounts}
