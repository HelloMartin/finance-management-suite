from uuid import UUID

from finance_suite.account import Account


def test_account_initialisazion():
    """Tests that the Account object initializes correctly with valid data."""

    test_name = "Savings"
    test_currency = "CHF"

    account = Account(name=test_name, currency=test_currency)

    assert account.name == test_name
    assert account.currency == test_currency
    assert isinstance(account.id, UUID)
    assert account.id is not None


def test_id_is_unique_across_instances():
    """Tests that creating multiple instances results in different UUIDs"""

    account1 = Account("", "")
    account2 = Account("", "")

    assert account1.id != account2.id
