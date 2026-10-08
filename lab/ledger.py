"""Toy in-memory settlement fixture."""


class Ledger:
    def __init__(self) -> None:
        self.total = 0
        self._settled: dict[str, int] = {}

    def settle(self, reservation_id: str, amount: int) -> int:
        """Apply a valid synthetic reservation once and return the current total."""
        if not isinstance(reservation_id, str) or not reservation_id:
            raise ValueError("reservation_id must be a nonempty string")
        if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
            raise ValueError("amount must be a positive integer excluding bool")

        if reservation_id in self._settled:
            if self._settled[reservation_id] != amount:
                raise ValueError("reservation_id already settled with a different amount")
            return self.total

        self._settled[reservation_id] = amount
        self.total += amount
        return self.total
