from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from finance_suite.account import Account
from finance_suite.account_services import get_account_balance
from finance_suite.database import add_account, add_transaction, setup_database
from finance_suite.transaction import Transaction


def test_get_positive_account_balance(tmp_path):
    """Tests positive balance for given account"""
    db_path = tmp_path / "test.sqlite3"

    transaction_date = date(year=2026, month=1, day=1)

    account = Account(name="Jon Doe", currency="CHF")
    transaction_1 = Transaction(
        account_id=account.id,
        amount=Decimal("100.00"),
        description="Add salary",
        date=transaction_date,
    )
    transaction_2 = Transaction(
        account_id=account.id,
        amount=Decimal("-50.00"),
        description="Spend money",
        date=transaction_date,
    )
    transaction_3 = Transaction(
        account_id=account.id,
        amount=Decimal("75.00"),
        description="Add salary",
        date=transaction_date,
    )

    setup_database(db_path=db_path)
    add_account(account=account, db_path=db_path)
    add_transaction(transaction=transaction_1, db_path=db_path)
    add_transaction(transaction=transaction_2, db_path=db_path)
    add_transaction(transaction=transaction_3, db_path=db_path)

    assert get_account_balance(account_id=account.id, db_path=db_path) == Decimal(
        "125.00"
    )


def test_get_zero_account_balance(tmp_path):
    """Tests zero balance for given account"""
    db_path = tmp_path / "test.sqlite3"

    transaction_date = date(year=2026, month=1, day=1)

    account = Account(name="Jon Doe", currency="CHF")
    transaction_1 = Transaction(
        account_id=account.id,
        amount=Decimal("100.00"),
        description="Add salary",
        date=transaction_date,
    )
    transaction_2 = Transaction(
        account_id=account.id,
        amount=Decimal("-25.00"),
        description="Spend money",
        date=transaction_date,
    )
    transaction_3 = Transaction(
        account_id=account.id,
        amount=Decimal("-75.00"),
        description="Add salary",
        date=transaction_date,
    )

    setup_database(db_path=db_path)
    add_account(account=account, db_path=db_path)
    add_transaction(transaction=transaction_1, db_path=db_path)
    add_transaction(transaction=transaction_2, db_path=db_path)
    add_transaction(transaction=transaction_3, db_path=db_path)

    assert get_account_balance(account_id=account.id, db_path=db_path) == Decimal(
        "0.00"
    )


def test_get_account_balance_no_transactions(tmp_path):
    """Tests balance for given account without transactions"""
    db_path = tmp_path / "test.sqlite3"

    account = Account(name="Jon Doe", currency="CHF")

    setup_database(db_path=db_path)
    add_account(account=account, db_path=db_path)

    assert get_account_balance(account_id=account.id, db_path=db_path) == Decimal(
        "0.00"
    )


def test_get_account_balance_no_account(tmp_path):
    """Tests balance for unknown account"""
    db_path = tmp_path / "test.sqlite3"

    account_id = uuid4()

    setup_database(db_path=db_path)

    with pytest.raises(ValueError):
        get_account_balance(account_id=account_id, db_path=db_path)
