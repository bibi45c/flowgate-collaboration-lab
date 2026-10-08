"""Toy in-memory settlement fixture."""


class Ledger:
    def __init__(self) -> None:
        self.total = 0

    def settle(self, reservation_id: str, amount: int) -> int:
        """Add a synthetic reservation charge and return the total."""
        self.total += amount
        return self.total
