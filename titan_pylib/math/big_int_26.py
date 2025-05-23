from string import ascii_lowercase


class BigInt26:

    D = {v: k for k, v in enumerate(ascii_lowercase)}

    def __init__(self, s=""):
        n = len(s)
        a = [0] * n
        s = s[::-1]
        for i in range(n):
            a[i] = self.D[s[i]]
        self.n = n
        self.a = a

    def __add__(self, other: "BigInt26") -> "BigInt26":
        assert isinstance(other, BigInt26)
        a = [0] * max(self.n, other.n)
        nxt = 0
        idx = 0
        while idx < min(self.n, other.n):
            a[idx] = (self.a[idx] + other.a[idx]) + nxt
            nxt = a[idx] // 26
            a[idx] %= 26
            idx += 1
        while idx < self.n:
            a[idx] = self.a[idx] + nxt
            nxt = a[idx] // 26
            a[idx] %= 26
            idx += 1
        while idx < other.n:
            a[idx] = other.a[idx] + nxt
            nxt = a[idx] // 26
            a[idx] %= 26
            idx += 1
        if nxt:
            if idx == len(a):
                a.append(nxt)
            else:
                a[idx] = nxt
        s = BigInt26()
        s.a = a
        s.n = len(a)
        return s

    def copy(self):
        s = BigInt26()
        s.a = self.a[:]
        s.n = self.n
        return s

    def __floordiv__(self, other: int) -> "BigInt26":
        assert isinstance(other, int)
        s = self.copy()
        nxt = 0
        for i in range(self.n - 1, -1, -1):
            s.a[i] += nxt * 26
            nxt = s.a[i] % other
            s.a[i] //= other
        return s

    def to_str(self) -> str:
        s = [""] * self.n
        for i in range(self.n):
            s[i] = ascii_lowercase[self.a[i]]
        s.reverse()
        return "".join(s)

    def __str__(self):
        return str(self.a)
