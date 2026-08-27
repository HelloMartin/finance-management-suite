from uuid import UUID, uuid4


class Account:
    """
    Represents a user's financial account.
    """

    def __init__(
        self,
        name: str,
        currency: str,
        id: UUID | None = None,
    ):
        self.id = id if id is not None else uuid4()
        self.name: str = name
        self.currency: str = currency

    def __repr__(self):
        return (
            f"Account(id={self.id}, name='{self.name}', " f"currency='{self.currency}')"
        )

    def __eq__(self, other):
        if not isinstance(other, Account):
            return NotImplemented

        return (
            self.name == other.name
            and self.currency == other.currency
            and self.id == other.id
        )
