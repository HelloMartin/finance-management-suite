from decimal import Decimal
from uuid import UUID

from finance_suite.balance import calculate_balance
from finance_suite.database import get_account_by_id, get_all_transactions_by_account_id
from finance_suite.transaction import Transaction


def get_account_balance(account_id: UUID, db_path: str = "db.sqlite3") -> Decimal:
    if not get_account_by_id(uuid_str=str(account_id), db_path=db_path):
        raise ValueError(f"Account with {account_id} is unknown")

    transactions: list[Transaction] = get_all_transactions_by_account_id(
        str(account_id), db_path=db_path
    )

    return calculate_balance(account_id=account_id, transactions=transactions)
