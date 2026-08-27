from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4


class Transaction:
    """
    Represents a single financial movement.
    """

    def __init__(
        self,
        account_id: UUID,
        amount: Decimal,
        description: str,
        date: date,
        id: UUID | None = None,
    ):
        self.id = id if id is not None else uuid4()
        self.account_id: UUID = account_id
        self.amount: Decimal = amount
        self.description: str = description
        self.transaction_date: date = date

    def __repr__(self):
        return f"Transaction(id={self.id}, account_id={self.account_id}, amount={self.amount}, description={self.description}, transaction_date={self.transaction_date})"

    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return NotImplemented

        return (
            self.id == other.id
            and self.account_id == other.account_id
            and self.amount == other.amount
            and self.description == other.description
            and self.transaction_date == other.transaction_date
        )
