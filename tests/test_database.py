import sqlite3
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest

from finance_suite.account import Account
from finance_suite.database import (
    add_account,
    add_transaction,
    get_account_by_id,
    get_all_accounts,
    get_all_transactions,
    get_all_transactions_by_account_id,
    get_transaction_by_id,
    setup_database,
)
from finance_suite.transaction import Transaction

now_utc = datetime.now(ZoneInfo("UTC"))


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


def test_setup_database_creates_transactions_table(tmp_path):
    """Test that setup_database() creates the transactions table."""

    db_path = tmp_path / "test.sqlite3"

    setup_database(db_path=db_path)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [row[1] for row in cursor.fetchall()]

        assert columns == [
            "transaction_id",
            "account_id",
            "amount",
            "description",
            "transaction_date",
        ]


def test_add_and_get_transaction_by_id(tmp_path):
    """Test that a transaction can be loaded with all fields, including its original UUID."""

    db_path = tmp_path / "test.sqlite3"

    write_account = Account(name="Jon Doe", currency="CHF")

    write_transaction = Transaction(
        account_id=write_account.id,
        amount=Decimal("100.00"),
        description="Add salary",
        date=date(2026, 1, 1),
    )

    setup_database(db_path=db_path)
    add_account(account=write_account, db_path=db_path)
    add_transaction(transaction=write_transaction, db_path=db_path)

    read_transaction: Transaction | None = get_transaction_by_id(
        uuid_str=str(write_transaction.id), db_path=db_path
    )

    assert read_transaction is not None
    assert write_transaction.id == read_transaction.id
    assert write_transaction.account_id == read_transaction.account_id
    assert write_transaction.amount == read_transaction.amount
    assert write_transaction.description == read_transaction.description
    assert write_transaction.transaction_date == read_transaction.transaction_date


def test_get_transaction_by_unknown_id_returns_none(tmp_path):
    """Test that requesting an unknown UUID returns None."""

    db_path = tmp_path / "test.sqlite3"

    setup_database(db_path=db_path)
    transaction = get_transaction_by_id(
        "569c3039-FAKE-FAKE-FAKE-b6479594c113", db_path=db_path
    )

    assert transaction is None


def test_get_all_transactions_returns_all_transactions(tmp_path):
    """Test that get_all_transactions() returns both added transactions."""

    db_path = tmp_path / "test.sqlite3"

    account_1 = Account(name="Joe Doe", currency="CHF")
    account_2 = Account(name="Marry Doe", currency="USD")

    amount = Decimal("100.00")
    description = "Add salary"
    transaction_date = date(year=2026, month=1, day=1)

    write_transaction_1 = Transaction(
        account_id=account_1.id,
        amount=amount,
        description=description,
        date=transaction_date,
    )
    write_transaction_2 = Transaction(
        account_id=account_1.id,
        amount=amount,
        description=description,
        date=transaction_date,
    )
    write_transaction_3 = Transaction(
        account_id=account_2.id,
        amount=amount,
        description=description,
        date=transaction_date,
    )

    write_transactions: list[Transaction] = [
        write_transaction_1,
        write_transaction_2,
        write_transaction_3,
    ]

    setup_database(db_path=db_path)
    add_account(account=account_1, db_path=db_path)
    add_account(account=account_2, db_path=db_path)
    add_transaction(transaction=write_transaction_1, db_path=db_path)
    add_transaction(transaction=write_transaction_2, db_path=db_path)
    add_transaction(transaction=write_transaction_3, db_path=db_path)

    read_transactions: list[Transaction] = get_all_transactions(db_path=db_path)

    assert len(write_transactions) == len(read_transactions)
    assert {a.id for a in write_transactions} == {a.id for a in read_transactions}


def test_get_transaction_by_account_id_returns_all_transactions_of_account(tmp_path):
    """
    Test that get_all_transactions_by_account_by_id()
    returns only transactions of given account.
    """

    db_path = tmp_path / "test.sqlite3"

    account_1 = Account(name="Joe Doe", currency="CHF")
    account_2 = Account(name="Marry Doe", currency="USD")

    amount = Decimal("100.00")
    description = "Add salary"
    transaction_date = date(year=2026, month=1, day=1)

    write_transaction_1 = Transaction(
        account_id=account_1.id,
        amount=amount,
        description=description,
        date=transaction_date,
    )
    write_transaction_2 = Transaction(
        account_id=account_1.id,
        amount=amount,
        description=description,
        date=transaction_date,
    )
    write_transaction_3 = Transaction(
        account_id=account_2.id,
        amount=amount,
        description=description,
        date=transaction_date,
    )

    write_transactions: list[Transaction] = [
        write_transaction_1,
        write_transaction_2,
    ]

    setup_database(db_path=db_path)
    add_account(account=account_1, db_path=db_path)
    add_account(account=account_2, db_path=db_path)
    add_transaction(transaction=write_transaction_1, db_path=db_path)
    add_transaction(transaction=write_transaction_2, db_path=db_path)
    add_transaction(transaction=write_transaction_3, db_path=db_path)

    read_transactions: list[Transaction] = get_all_transactions_by_account_id(
        uuid_str=str(account_1.id), db_path=db_path
    )

    assert len(write_transactions) == len(read_transactions)
    assert {a.id for a in write_transactions} == {a.id for a in read_transactions}


def test_transaction_for_unknown_account_is_rejected(tmp_path):
    db_path = tmp_path / "test.sqlite3"
    setup_database(db_path=db_path)

    transaction = Transaction(
        account_id=uuid4(),
        amount=Decimal("100.00"),
        description="Invalid transaction",
        date=date(2026, 1, 1),
    )

    with pytest.raises(sqlite3.IntegrityError):
        add_transaction(transaction=transaction, db_path=db_path)
