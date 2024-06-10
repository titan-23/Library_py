# ref: https://qiita.com/keymoon/items/11fac5627672a6d6a9f6
from titan_pylib.data_structures.splay_tree.reversible_lazy_splay_tree_array import (
    ReversibleLazySplayTreeArrayData,
    ReversibleLazySplayTreeArray,
)
from typing import Optional, Final
import random
import string

_titan_pylib_DynamicHashString_MOD: Final[int] = (1 << 61) - 1
_titan_pylib_DynamicHashString_DIC: Final[dict[str, int]] = {
    c: i for i, c in enumerate(string.ascii_lowercase, 1)
}
_titan_pylib_DynamicHashString_MASK30: Final[int] = (1 << 30) - 1
_titan_pylib_DynamicHashString_MASK31: Final[int] = (1 << 31) - 1
_titan_pylib_DynamicHashString_MASK61: Final[int] = _titan_pylib_DynamicHashString_MOD


class DynamicHashStringBase:
    """動的な文字列に対するロリハです。

    平衡二分木にモノイドを載せてるだけです。こんなライブラリ必要ないです。

    Example:
        ```
        base = DynamicHashStringBase(2 * 10**5 + 1)
        dhs_s = DynamicHashString(base, s)
        dhs_t = DynamicHashString(base, t)

        pref = dhs_s.get(0, r)
        suff = dhs_t.get(l, n)
        h = base.unite(pref, suff, n-l)
        ```
    """

    def __init__(self, n: int = 0, base: int = -1, seed: Optional[int] = None) -> None:
        assert n >= 0
        rand = random.Random(seed)
        base = rand.randint(37, 10**9) if base < 0 else base
        powb = [1] * (n + 1)
        for i in range(1, n + 1):
            powb[i] = self.get_mul(powb[i - 1], base)
        op = lambda s, t: (self.unite(s[0], t[0], t[1]), s[1] + t[1])
        e = (0, 0)
        self.base = base
        self.data = ReversibleLazySplayTreeArrayData(op=op, e=e)
        self.n = n
        self.powb = powb

    @staticmethod
    def get_mul(a: int, b: int) -> int:
        au = a >> 31
        ad = a & _titan_pylib_DynamicHashString_MASK31
        bu = b >> 31
        bd = b & _titan_pylib_DynamicHashString_MASK31
        mid = ad * bu + au * bd
        midu = mid >> 30
        midd = mid & _titan_pylib_DynamicHashString_MASK30
        return DynamicHashStringBase.get_mod(
            au * bu * 2 + midu + (midd << 31) + ad * bd
        )

    @staticmethod
    def get_mod(x: int) -> int:
        # 商と余りを計算して足す->割る
        xu = x >> 61
        xd = x & _titan_pylib_DynamicHashString_MASK61
        res = xu + xd
        if res >= _titan_pylib_DynamicHashString_MOD:
            res -= _titan_pylib_DynamicHashString_MOD
        return res

    def extend(self, cap: int) -> None:
        pre_cap = len(self.powb)
        powb = self.powb
        powb += [0] * cap
        for i in range(pre_cap, pre_cap + cap):
            powb[i] = DynamicHashStringBase.get_mul(powb[i - 1], self.base)

    def get_cap(self) -> int:
        return len(self.powb)

    def unite(self, h1: int, h2: int, k: int) -> int:
        """2つの hash 値を concat します。

        Args:
            h1 (int): prefix
            h2 (int): suffix
            k (int): h2の長さ

        Returns:
            int: h1 + h2
        """
        # h1, h2, k
        # len(h2) == k
        # h1 <- h2
        if k >= self.get_cap():
            self.extend(k - self.get_cap() + 1)
        return self.get_mod(self.get_mul(h1, self.powb[k]) + h2)


class DynamicHashString:

    def __init__(self, hsb: DynamicHashStringBase, s: str) -> None:
        self.hsb = hsb
        self.splay: ReversibleLazySplayTreeArray[tuple[int, int], None] = (
            ReversibleLazySplayTreeArray(
                hsb.data, ((_titan_pylib_DynamicHashString_DIC[c], 1) for c in s)
            )
        )

    def insert(self, k: int, c: str) -> None:
        """位置 ``k`` に ``c`` を挿入します。
        :math:`O(\\log{n})` です。
        """
        self.splay.insert(k, (_titan_pylib_DynamicHashString_DIC[c], 1))

    def pop(self, k: int) -> int:
        return self.splay.pop(k)

    def reverse(self, l: int, r: int) -> None:
        self.splay.reverse(l, r)

    def all_reverse(self) -> None:
        self.splay.all_reverse()

    def split(self, k: int) -> tuple["DynamicHashString", "DynamicHashString"]:
        left, right = self.splay.split(k)
        return (DynamicHashString(self.hsb, left), DynamicHashString(self.hsb, right))

    def all_get(self) -> int:
        return self.splay.all_prod()[0]

    def get(self, l: int, r: int) -> int:
        return self.splay.prod(l, r)[0]

    def extend(self, other: "DynamicHashString") -> None:
        assert self.hsb is other.hsb
        self.splay.merge(other.splay)

    def __getitem__(self, k: int) -> int:
        return self.splay[k][0]

    def set(self, k: int, c: str) -> None:
        self.splay[k] = (_titan_pylib_DynamicHashString_DIC[c], 1)

    def __setitem__(self, k: int, c: str) -> None:
        return self.set(k, c)

    def __len__(self) -> int:
        return len(self.splay)

    def __str__(self) -> str:
        return str([self[i] for i in range(len(self))])
