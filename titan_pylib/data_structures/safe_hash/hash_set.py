from typing import Iterable
from random import Random


class HashSet:

    _r = Random()
    _xor = _r.randrange(10000000, 1000000000)

    def __init__(self, a: Iterable[int] = []):
        self._data: set[int] = set(x ^ self._xor for x in a)

    def add(self, key: int) -> None:
        self._data.add(key ^ self._xor)

    def discard(self, key: int) -> None:
        self._data.discard(key ^ self._xor)

    def remove(self, key: int) -> None:
        self._data.remove(key ^ self._xor)

    def __contains__(self, key: int):
        return key ^ self._xor in self._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return (k ^ self._xor for k in self._data.__iter__())

    def __str__(self):
        return "{" + ", ".join(sorted(map(str, self))) + "}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
