from titan_pylib.data_structures.fenwick_tree.fenwick_tree import FenwickTree
import string


class StringCount:

    alp: str = string.ascii_lowercase
    # alp: str = string.ascii_uppercase
    DIC: dict[str, int] = {c: i for i, c in enumerate(alp)}

    def __init__(self, s: str):
        assert isinstance(s, str)
        self.n: int = len(s)
        self.s: list[str] = list(s)
        self.data: list[FenwickTree] = [FenwickTree(self.n) for _ in range(26)]
        for i, c in enumerate(s):
            self.data[StringCount.DIC[c]].add(i, 1)

    # 区間[l, r)が昇順かどうか判定する
    def is_ascending(self, l: int, r: int) -> bool:
        # assert 0 <= l <= r <= self.n
        end = l
        for i in range(26):
            c = self.data[i].sum(l, r)
            end += c
            if end > r or self.data[i].sum(l, end) != c:
                return False
        return True

    # 区間[l, r)が降順かどうか判定する
    # 未確認
    def is_descending(self, l: int, r: int) -> bool:
        # assert 0 <= l <= r <= self.n
        start = r - 1
        for i in range(25, -1, -1):
            c = self.data[i].sum(l, r)
            start -= c
            if start < l or self.data[i].sum(start, r) != c:
                return False
        return True

    # 区間[l, r)の最小の文字を返す
    def get_min(self, l: int, r: int) -> str:
        for i in range(26):
            if self.data[i].sum(l, r):
                return StringCount.alp[i]
        assert False, "Indexerror"

    # 区間[l, r)の最大の文字を返す
    def get_max(self, l: int, r: int) -> str:
        for i in range(25, -1, -1):
            if self.data[i].sum(l, r):
                return StringCount.alp[i]
        assert False, "Indexerror"

    # k番目の文字をcに変更する
    def __setitem__(self, k: int, c: str):
        # assert 0 <= k < self.n
        self.data[StringCount.DIC[self.s[k]]].add(k, -1)
        self.s[k] = c
        self.data[StringCount.DIC[c]].add(k, 1)

    # 区間[l, r)の全ての文字の個数を返す
    # 返り値は要素数26のlist[int]
    def get_all_count(self, l: int, r: int) -> list[int]:
        return [self.data[i].sum(l, r) for i in range(26)]

    # 区間[l, r)のcの個数を返す
    def get_count(self, l: int, r: int, c: str) -> int:
        return self.data[StringCount.DIC[c]].sum(l, r)

    def __getitem__(self, k: int) -> str:
        return self.s[k]

    def __str__(self):
        return "".join(self.s)
