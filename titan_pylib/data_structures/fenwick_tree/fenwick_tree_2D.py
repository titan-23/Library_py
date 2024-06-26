class FenwickTree2D:
    """2次元です。"""

    def __init__(self, h: int, w: int, a: list[list[int]] = []) -> None:
        """O(HWlogHlogW)"""
        self._h = h + 1
        self._w = w + 1
        self._bit = [0] * (self._h * self._w)
        if a:
            assert len(a) == h
            if h == 0:
                return
            assert len(a[0]) == w
            self._build(a)

    def _build(self, a: list[list[int]]) -> None:
        for i in range(self._h - 1):
            for j in range(self._w - 1):
                if a[i][j] != 0:
                    self.add(i, j, a[i][j])

    def add(self, h: int, w: int, x: int) -> None:
        """Add x to a[h][w]. / O(logH * logW)"""
        assert 0 <= h < self._h - 1, f"IndexError"
        assert 0 <= w < self._w - 1, f"IndexError"
        h += 1
        w += 1
        _h, _w, _bit = self._h, self._w, self._bit
        while h < _h:
            j = w
            while j < _w:
                _bit[h * _w + j] += x
                j += j & -j
            h += h & -h

    def set(self, h: int, w: int, x: int) -> None:
        assert 0 <= h < self._h - 1, f"IndexError"
        assert 0 <= w < self._w - 1, f"IndexError"
        self.add(h, w, x - self.get(h, w))

    def _sum(self, h: int, w: int) -> int:
        """Return sum([0, h) x [0, w)) of a. / O(logH * logW)"""
        assert 0 <= h < self._h, f"IndexError"
        assert 0 <= w < self._w, f"IndexError"
        ret = 0
        _w, _bit = self._w, self._bit
        while h > 0:
            j = w
            while j > 0:
                ret += _bit[h * _w + j]
                j -= j & -j
            h -= h & -h
        return ret

    def sum(self, h1: int, w1: int, h2: int, w2: int) -> int:
        """Retrun sum([h1, h2) x [w1, w2)) of a. / O(logH * logW)"""
        assert 0 <= h1 <= h2 < self._h, f"IndexError"
        assert 0 <= w1 <= w2 < self._w, f"IndexError"
        return (
            self._sum(h2, w2)
            - self._sum(h2, w1)
            - self._sum(h1, w2)
            + self._sum(h1, w1)
        )

    def get(self, h: int, w: int) -> int:
        assert 0 <= h < self._h - 1, f"IndexError"
        assert 0 <= w < self._w - 1, f"IndexError"
        return self.sum(h, w, h + 1, w + 1)

    def __str__(self) -> str:
        ret = []
        for i in range(self._h - 1):
            ret.append(
                ", ".join(map(str, ((self.get(i, j)) for j in range(self._w - 1))))
            )
        return "[\n  " + "\n  ".join(map(str, ret)) + "\n]"
