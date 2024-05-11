# from titan_pylib.data_structures.permutation.permutation import Permutation
from typing import Iterable


class Permutation:

    def __init__(self, P: Iterable[int]) -> None:
        _p = list(P)
        _n = len(P)
        _inv = [-1 for _ in range(_n)]
        for i, p in enumerate(_p):
            assert 0 <= p < _n, f"P is not permutation, {P=}"
            _inv[p] = i
        assert -1 not in _inv, f"P is not permutation, {P=}"
        self._p = _p
        self._n = _n
        self._inv = _inv

    def __getitem__(self, k: int) -> int:
        return self._p[k]

    def index(self, val: int) -> int:
        return self._inv[val]

    def swap(self, i: int, j: int) -> None:
        _inv, _p = self._inv, self._p
        _inv[_p[i]], _inv[_p[j]] = _inv[_p[j]], _inv[_p[i]]
        _p[i], _p[j] = _p[j], _p[i]

    def __str__(self) -> str:
        return str(self._p)

    __repr__ = __str__
