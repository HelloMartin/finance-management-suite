from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4


class Transaction:
    """
    Represents a single financial movement.
    """
    
    def __init__(self, account_id: UUID, amount: Decimal, description: str, date: date):
        self.id: UUID = uuid4()
        self.account_id: UUID = account_id
        self.amount: Decimal = amount
        self.description: str = description
        self.transaction_date: date = date
        