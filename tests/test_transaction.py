from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from finance_suite.account import Account
from finance_suite.transaction import Transaction

now_utc = datetime.now(ZoneInfo("UTC"))


def test_transaction_initialization():
    """Tests that the Transaction object initializes correctly with valid data."""

    test_name = "Savings"
    test_currency = "CHF"
    account = Account(name=test_name, currency=test_currency)

    transaction_amount = Decimal("100.00")
    transaction_description = "Salary"
    transaction_date = now_utc.date()

    transaction = Transaction(
        account.id, transaction_amount, transaction_description, transaction_date
    )

    assert transaction.account_id == account.id
    assert transaction.amount == transaction_amount
    assert transaction.description == transaction_description
    assert transaction.transaction_date == transaction_date
    assert isinstance(transaction.id, UUID)


def test_id_is_unique_across_instances():
    """Tests that creating multiple instances results in different UUIDs"""

    account_id = uuid4()
    test_amount = Decimal("0.00")
    test_description = ""
    test_date = now_utc.date()

    transaction1 = Transaction(account_id, test_amount, test_description, test_date)

    transaction2 = Transaction(account_id, test_amount, test_description, test_date)

    assert transaction1.id != transaction2.id
