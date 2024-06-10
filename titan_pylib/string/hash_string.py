# ref: https://qiita.com/keymoon/items/11fac5627672a6d6a9f6
from titan_pylib.data_structures.segment_tree.segment_tree import SegmentTree
from typing import Optional, Final
import random
import string

_titan_pylib_HashString_MOD: Final[int] = (1 << 61) - 1
_titan_pylib_HashString_DIC: Final[dict[str, int]] = {
    c: i for i, c in enumerate(string.ascii_lowercase, 1)
}
_titan_pylib_HashString_MASK30: Final[int] = (1 << 30) - 1
_titan_pylib_HashString_MASK31: Final[int] = (1 << 31) - 1
_titan_pylib_HashString_MASK61: Final[int] = _titan_pylib_HashString_MOD


class HashStringBase:
    """HashStringのベースクラスです。"""

    def __init__(self, n: int = 0, base: int = -1, seed: Optional[int] = None) -> None:
        """
        :math:`O(n)` です。

        Args:
            n (int): 文字列の長さの上限です。上限を超えても問題ありません。
            base (int, optional): Defaults to -1.
            seed (Optional[int], optional): Defaults to None.
        """
        rand = random.Random(seed)
        base = rand.randint(37, 10**9) if base < 0 else base
        powb = [1] * (n + 1)
        invb = [1] * (n + 1)
        invbpow = pow(base, -1, _titan_pylib_HashString_MOD)
        for i in range(1, n + 1):
            powb[i] = HashStringBase.get_mul(powb[i - 1], base)
            invb[i] = HashStringBase.get_mul(invb[i - 1], invbpow)
        self.n = n
        self.base = base
        self.invpow = invbpow
        self.powb = powb
        self.invb = invb

    @staticmethod
    def get_mul(a: int, b: int) -> int:
        au = a >> 31
        ad = a & _titan_pylib_HashString_MASK31
        bu = b >> 31
        bd = b & _titan_pylib_HashString_MASK31
        mid = ad * bu + au * bd
        midu = mid >> 30
        midd = mid & _titan_pylib_HashString_MASK30
        return HashStringBase.get_mod(au * bu * 2 + midu + (midd << 31) + ad * bd)

    @staticmethod
    def get_mod(x: int) -> int:
        xu = x >> 61
        xd = x & _titan_pylib_HashString_MASK61
        res = xu + xd
        if res >= _titan_pylib_HashString_MOD:
            res -= _titan_pylib_HashString_MOD
        return res

    def extend(self, cap: int) -> None:
        pre_cap = len(self.powb)
        powb, invb = self.powb, self.invb
        powb += [0] * cap
        invb += [0] * cap
        invbpow = pow(self.base, -1, _titan_pylib_HashString_MOD)
        for i in range(pre_cap, pre_cap + cap):
            powb[i] = HashStringBase.get_mul(powb[i - 1], self.base)
            invb[i] = HashStringBase.get_mul(invb[i - 1], invbpow)

    def get_cap(self) -> int:
        return len(self.powb)

    def unite(self, h1: int, h2: int, k: int) -> int:
        # len(h2) == k
        # h1 <- h2
        if k >= self.get_cap():
            self.extend(k - self.get_cap() + 1)
        return self.get_mod(self.get_mul(h1, self.powb[k]) + h2)


class HashString:

    def __init__(self, hsb: HashStringBase, s: str, update: bool = False) -> None:
        """ロリハを構築します。
        :math:`O(n)` です。

        Args:
            hsb (HashStringBase): ベースクラスです。
            s (str): ロリハを構築する文字列です。
            update (bool, optional): ``update=True`` のとき、1点更新が可能になります。
        """
        n = len(s)
        data = [0] * n
        acc = [0] * (n + 1)
        if n > hsb.get_cap():
            hsb.extend(n - hsb.get_cap())
        powb = hsb.powb
        for i, c in enumerate(s):
            data[i] = hsb.get_mul(powb[n - i - 1], _titan_pylib_HashString_DIC[c])
            acc[i + 1] = hsb.get_mod(acc[i] + data[i])
        self.hsb = hsb
        self.n = n
        self.acc = acc
        self.used_seg = False
        if update:
            self.seg = SegmentTree(
                data, lambda s, t: (s + t) % _titan_pylib_HashString_MOD, 0
            )

    def get(self, l: int, r: int) -> int:
        """``s[l, r)`` のハッシュ値を返します。
        1点更新処理後は :math:`O(\\log{n})` 、そうでなければ :math:`O(1)` です。

        Args:
            l (int): インデックスです。
            r (int): インデックスです。

        Returns:
            int: ハッシュ値です。
        """
        if self.used_seg:
            return self.hsb.get_mul(self.seg.prod(l, r), self.hsb.invb[self.n - r])
        return self.hsb.get_mul(
            self.hsb.get_mod(self.acc[r] - self.acc[l]), self.hsb.invb[self.n - r]
        )

    def __getitem__(self, k: int) -> int:
        """``s[k]`` のハッシュ値を返します。
        1点更新処理後は :math:`O(\\log{n})` 、そうでなければ :math:`O(1)` です。

        Args:
            k (int): インデックスです。

        Returns:
            int: ハッシュ値です。
        """
        return self.get(k, k + 1)

    def set(self, k: int, c: str) -> None:
        """`k` 番目の文字を `c` に更新します。
        :math:`O(\\log{n})` です。また、今後の ``get()`` が :math:`O(\\log{n})` になります。

        Args:
            k (int): インデックスです。
            c (str): 更新する文字です。
        """
        self.used_seg = True
        self.seg[k] = self.hsb.get_mul(
            self.hsb.powb[self.n - k - 1], _titan_pylib_HashString_DIC[c]
        )

    def __setitem__(self, k: int, c: str) -> None:
        return self.set(k, c)

    def __len__(self):
        return self.n

    def get_lcp(self) -> list[int]:
        """lcp配列を返します。
        :math:`O(n\\log{n})` です。
        """
        a = [0] * self.n
        memo = [-1] * (self.n + 1)
        for i in range(self.n):
            ok, ng = 0, self.n - i + 1
            while ng - ok > 1:
                mid = (ok + ng) >> 1
                if memo[mid] == -1:
                    memo[mid] = self.get(0, mid)
                if memo[mid] == self.get(i, i + mid):
                    ok = mid
                else:
                    ng = mid
            a[i] = ok
        return a
