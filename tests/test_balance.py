from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from finance_suite.balance import calculate_balance, is_transaction_allowed
from finance_suite.transaction import Transaction

now_utc = datetime.now(ZoneInfo("UTC"))
transaction_date = now_utc.date()
test_account_id = uuid4()


def test_standard_positive_sum():
    """Test case for a standard list of positive transactions."""

    t1 = Transaction(
        test_account_id, Decimal("100.00"), "test transaction 1", transaction_date
    )
    t2 = Transaction(
        test_account_id, Decimal("200.00"), "test transaction 1", transaction_date
    )
    t3 = Transaction(
        test_account_id, Decimal("300.00"), "test transaction 1", transaction_date
    )

    transactions = [t1, t2, t3]
    expected_total = Decimal("600.00")
    result = calculate_balance(test_account_id, transactions)

    assert result == expected_total


def test_empty_list():
    """Test case for an empty list of transactions."""

    transactions = []
    expected_total = Decimal("0.00")
    result = calculate_balance(test_account_id, transactions)

    assert result == expected_total


def test_mixed_sign_sum():
    """Test case involving positive, negative, and zero amounts."""

    t1 = Transaction(
        test_account_id, Decimal("100.00"), "test transaction 1", transaction_date
    )
    t2 = Transaction(
        test_account_id, Decimal("0.00"), "test transaction 1", transaction_date
    )
    t3 = Transaction(
        test_account_id, Decimal("-300.00"), "test transaction 1", transaction_date
    )

    transactions = [t1, t2, t3]
    expected_total = Decimal("-200.00")
    result = calculate_balance(test_account_id, transactions)

    assert result == expected_total


def test_single_transaction():
    """Test case with only one transaction."""

    t1 = Transaction(
        test_account_id, Decimal("100.00"), "test transaction 1", transaction_date
    )

    transactions = [t1]
    expected_total = Decimal("100.00")
    result = calculate_balance(test_account_id, transactions)

    assert result == expected_total


def test_account_without_matching_transactions():
    """Test case with unknown account."""

    t1 = Transaction(
        test_account_id, Decimal("100.00"), "test transaction 1", transaction_date
    )
    t2 = Transaction(
        test_account_id, Decimal("200.00"), "test transaction 1", transaction_date
    )
    t3 = Transaction(
        test_account_id, Decimal("300.00"), "test transaction 1", transaction_date
    )

    unknown_account_id: UUID = uuid4()
    transactions = [t1, t2, t3]
    expected_total = Decimal("0.00")
    result = calculate_balance(unknown_account_id, transactions)

    assert result == expected_total


def test_transaction_is_allowed_positive_balance():
    """Test allowed transaction with positive balance"""

    t1 = Transaction(
        test_account_id, Decimal("100.00"), "test transaction 1", transaction_date
    )

    t2 = Transaction(
        test_account_id, Decimal("100.00"), "test transaction 1", transaction_date
    )

    transactions = [t1]

    assert is_transaction_allowed(transactions, t2)


def test_transaction_allowed_when_balance_reaches_zero():
    """Test allowed transaction with zero balance"""

    t1 = Transaction(
        test_account_id, Decimal("100.00"), "test transaction 1", transaction_date
    )

    t2 = Transaction(
        test_account_id, Decimal("-100.00"), "test transaction 1", transaction_date
    )

    transactions = [t1]

    assert is_transaction_allowed(transactions, t2)


def test_transaction_rejected_when_balance_would_be_negative():
    """Test allowed transaction with negative balance"""

    t1 = Transaction(
        test_account_id, Decimal("100.00"), "test transaction 1", transaction_date
    )

    t2 = Transaction(
        test_account_id, Decimal("-200.00"), "test transaction 1", transaction_date
    )

    transactions = [t1]

    assert not is_transaction_allowed(transactions, t2)
