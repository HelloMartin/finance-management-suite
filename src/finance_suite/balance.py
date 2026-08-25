from decimal import Decimal
from uuid import UUID

from finance_suite.transaction import Transaction


def calculate_balance(account_id: UUID, transactions: list[Transaction]) -> Decimal:
    total_amount: Decimal = sum(
        (t.amount for t in transactions if t.account_id == account_id),
        start=Decimal("0.00"),
    )
    return total_amount


def is_transaction_allowed(
    transactions: list[Transaction], new_transaction: Transaction
) -> bool:
    if new_transaction.amount >= 0:
        return True

    return (
        calculate_balance(new_transaction.account_id, transactions)
        + new_transaction.amount
    ) >= 0
