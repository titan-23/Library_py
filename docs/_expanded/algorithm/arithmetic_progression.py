# from titan_pylib.algorithm.arithmetic_progression import ArithmeticProgression
class ArithmeticProgression:

    def __init__(self, a: int, d: int) -> None:
        """
        Args:
            a (int): 初項です。
            d (int): 公差です。
        """
        self.a = a
        self.d = d

    def __getitem__(self, k: int) -> int:
        """0-indexed."""
        assert k >= 0
        return self.a + k * self.d

    def index(self, v: int) -> int:
        """vが先頭から何番目か(0-indexed)"""
        v -= self.a
        assert v % self.d == 0
        i = v // self.d
        assert i >= 0
        return i

    def pref(self, n: int) -> int:
        """先頭n項の和."""
        if n < 0:
            return 0
        return (self[0] + self[n - 1]) // 2 * n

    def sum(self, l: int, r: int) -> int:
        """[l, r)"""
        return self.pref(r) - self.pref(l - 1)
