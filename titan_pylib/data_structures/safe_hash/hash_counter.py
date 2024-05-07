from titan_pylib.data_structures.safe_hash.hash_dict import HashDict
from typing import Iterable


class HashCounter:

    def __init__(self, a: Iterable[int] = []):
        self._data = HashDict()
        for a_ in a:
            if a_ in self._data:
                self._data[a_] += 1
            else:
                self._data[a_] = 1

    def __iter__(self):
        for k, v in self._data.items():
            yield k, v

    def __setitem__(self, key: int, val: int):
        self._data[key] = val

    def __getitem__(self, key: int) -> int:
        return self._data[key] if key in self._data else 0

    def __delitem__(self, key: int):
        if key in self._data:
            del self._data[key]

    def __contains__(self, key: int):
        return key in self._data

    def most_common(self):
        return sorted(self._data.items(), key=lambda x: -x[1])

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return f"{self.__class__.__name__}({str(self._data)})"
