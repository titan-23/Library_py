from titan_pylib.data_structures.fenwick_tree.fenwick_tree import FenwickTree
import string


class StringCount:

    def __init__(self, s: str, is_lower: bool = True):
        assert isinstance(s, str)
        self.alp: str = string.ascii_lowercase if is_lower else string.ascii_uppercase
        self.DIC: dict[str, int] = {c: i for i, c in enumerate(self.alp)}
        self.n: int = len(s)
        self.s: list[str] = list(s)
        dat: list[list[int]] = [[0] * self.n for _ in range(26)]
        for i, c in enumerate(s):
            dat[self.DIC[c]][i] += 1
        self.data: list[FenwickTree] = [FenwickTree(d) for d in dat]

    def is_ascending(self, l: int, r: int) -> bool:
        """区間[l, r)が昇順かどうか判定する / O(σlogn)"""
        assert 0 <= l <= r <= self.n
        end = l
        for dat in self.data:
            c = dat.sum(l, r)
            end += c
            if end > r or dat.sum(l, end) != c:
                return False
        return True

    def is_descending(self, l: int, r: int) -> bool:
        """
        区間[l, r)が降順かどうか判定する / O(σlogn)
        Note: 未確認
        """
        assert 0 <= l <= r <= self.n
        start = r - 1
        for dat in reversed(self.data):
            c = dat.sum(l, r)
            start -= c
            if start < l or dat.sum(start, r) != c:
                return False
        return True

    def get_min(self, l: int, r: int) -> str:
        """区間[l, r)の最小の文字を返す / O(σlogn)"""
        for i in range(26):
            if self.data[i].sum(l, r):
                return self.alp[i]
        assert False, "Indexerror"

    def get_max(self, l: int, r: int) -> str:
        """区間[l, r)の最大の文字を返す / O(σlogn)"""
        for i in range(25, -1, -1):
            if self.data[i].sum(l, r):
                return self.alp[i]
        assert False, "Indexerror"

    def __setitem__(self, k: int, c: str):
        """k番目の文字をcに変更する / O(logn)"""
        assert 0 <= k < self.n
        self.data[self.DIC[self.s[k]]].add(k, -1)
        self.s[k] = c
        self.data[self.DIC[c]].add(k, 1)

    # 区間[l, r)の全ての文字の個数を返す
    # 返り値は要素数26のlist[int]
    def get_all_count(self, l: int, r: int) -> list[int]:
        return [self.data[i].sum(l, r) for i in range(26)]

    def get_count(self, l: int, r: int, c: str) -> int:
        """区間[l, r)のcの個数を返す / O(logn)"""
        return self.data[self.DIC[c]].sum(l, r)

    def __getitem__(self, k: int) -> str:
        return self.s[k]

    def __str__(self):
        return "".join(self.s)
