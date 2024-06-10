# from titan_pylib.data_structures.safe_hash.hash_dict import HashDict
from typing import Any, Iterator
from random import Random


class HashDict:

    _r = Random()
    _xor = _r.randrange(10000000, 1000000000)

    def __init__(self) -> None:
        self._data: dict[int, Any] = {}

    def __setitem__(self, key: int, val: Any) -> None:
        self._data[key ^ self._xor] = val

    def __getitem__(self, key: int) -> Any:
        return self._data[key ^ self._xor]

    def __delitem__(self, key: int) -> None:
        del self._data[key ^ self._xor]

    def __contains__(self, key: int) -> bool:
        return key ^ self._xor in self._data

    def __len__(self) -> bool:
        return len(self._data)

    def keys(self) -> Iterator[int]:
        return (k ^ self._xor for k in self._data.keys())

    def values(self) -> Iterator[Any]:
        return (v for v in self._data.values())

    def items(self) -> Iterator[tuple[int, Any]]:
        return ((k ^ self._xor, v) for k, v in self._data.items())

    def __str__(self) -> str:
        return "{" + ", ".join(f"{k}: {v}" for k, v in self.items()) + "}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
