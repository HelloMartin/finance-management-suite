from uuid import UUID, uuid4


class Account:
    """
    Represents a user's financial account.
    """
    
    def __init__(self, name: str, currency: str):
        self.id: UUID = uuid4()
        self.name: str = name
        self.currency: str = currency
        