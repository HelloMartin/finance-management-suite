from decimal import Decimal
from uuid import UUID

from finance_suite.transaction import Transaction


def calculate_balance(account_id: UUID, transactions: list[Transaction]) -> Decimal:
    total_amount: Decimal = sum(
        (t.amount for t in transactions if t.account_id == account_id),
        start=Decimal("0.00"),
    )
    return total_amount
