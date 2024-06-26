from typing import Protocol


class SupportsLessThan(Protocol):

    def __lt__(self, other) -> bool: ...
