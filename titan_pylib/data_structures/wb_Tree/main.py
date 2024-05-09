from titan_pylib.data_structures.wb_tree.wbt_set import WBTSet
from titan_pylib.data_structures.wb_tree.wbt_multiset import WBTMultiset

#  -----------------------  #

import sys

input = lambda: sys.stdin.readline().rstrip()

import os
import io


class FastO:
    """標準出力高速化ライブラリです。"""

    _output = io.StringIO()

    @classmethod
    def write(cls, *args, sep: str = " ", end: str = "\n", flush: bool = False) -> None:
        """標準出力します。次の ``FastO.flush()`` が起きると print します。"""
        wr = cls._output.write
        for i in range(len(args) - 1):
            wr(str(args[i]))
            wr(sep)
        if args:
            wr(str(args[-1]))
        wr(end)
        if flush:
            cls.flush()

    @classmethod
    def flush(cls) -> None:
        """``flush`` します。これを実行しないと ``write`` した内容が表示されないので忘れないでください。"""
        os.write(1, cls._output.getvalue().encode())
        cls._output.close()


from typing import Generic, Iterable, TypeVar, Union, List

T = TypeVar("T")


class SegmentTreeRSQ(Generic[T]):

    def __init__(self, _n_or_a: Union[int, Iterable[T]], e: T = 0) -> None:
        self._e = e
        if isinstance(_n_or_a, int):
            self._n = _n_or_a
            self._log = (self._n - 1).bit_length()
            self._size = 1 << self._log
            self._data = [self._e] * (self._size << 1)
        else:
            _n_or_a = list(_n_or_a)
            self._n = len(_n_or_a)
            self._log = (self._n - 1).bit_length()
            self._size = 1 << self._log
            _data = [self._e] * (self._size << 1)
            _data[self._size : self._size + self._n] = _n_or_a
            for i in range(self._size - 1, 0, -1):
                _data[i] = _data[i << 1] + _data[i << 1 | 1]
            self._data = _data

    def get(self, k: int) -> T:
        assert (
            -self._n <= k < self._n
        ), f"IndexError: {self.__class__.__name__}.get({k}: int), n={self._n}"
        if k < 0:
            k += self._n
        return self._data[k + self._size]

    def set(self, k: int, v: T) -> None:
        assert (
            -self._n <= k < self._n
        ), f"IndexError: {self.__class__.__name__}.set({k}: int, {v}: T), n={self._n}"
        if k < 0:
            k += self._n
        k += self._size
        self._data[k] = v
        for _ in range(self._log):
            k >>= 1
            self._data[k] = self._data[k << 1] + self._data[k << 1 | 1]

    def prod(self, l: int, r: int):
        assert (
            0 <= l <= r <= self._n
        ), f"IndexError: {self.__class__.__name__}.prod({l}: int, {r}: int)"
        l += self._size
        r += self._size
        res = self._e
        while l < r:
            if l & 1:
                res += self._data[l]
                l += 1
            if r & 1:
                res += self._data[r ^ 1]
            l >>= 1
            r >>= 1
        return res

    def __getitem__(self, k: int) -> T:
        assert (
            -self._n <= k < self._n
        ), f"IndexError: {self.__class__.__name__}.__getitem__({k}: int), n={self._n}"
        return self.get(k)

    def __setitem__(self, k: int, v: T):
        assert (
            -self._n <= k < self._n
        ), f"IndexError: {self.__class__.__name__}.__setitem__{k}: int, {v}: T), n={self._n}"
        self.set(k, v)


# https://github.com/tatyam-prime/SortedSet/blob/main/SortedMultiset.py
import math
from bisect import bisect_left, bisect_right
from typing import Generic, Iterable, Iterator, List, Tuple, TypeVar, Optional

T = TypeVar("T")


class SortedMultiset(Generic[T]):
    BUCKET_RATIO = 16
    SPLIT_RATIO = 24

    def __init__(self, a: Iterable[T] = []) -> None:
        "Make a new SortedMultiset from iterable. / O(N) if sorted / O(N log N)"
        a = list(a)
        n = self.size = len(a)
        if any(a[i] > a[i + 1] for i in range(n - 1)):
            a.sort()
        num_bucket = int(math.ceil(math.sqrt(n / self.BUCKET_RATIO)))
        self.a = [
            a[n * i // num_bucket : n * (i + 1) // num_bucket]
            for i in range(num_bucket)
        ]

    def __iter__(self) -> Iterator[T]:
        for i in self.a:
            for j in i:
                yield j

    def __reversed__(self) -> Iterator[T]:
        for i in reversed(self.a):
            for j in reversed(i):
                yield j

    def __eq__(self, other) -> bool:
        return list(self) == list(other)

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return "SortedMultiset" + str(self.a)

    def __str__(self) -> str:
        s = str(list(self))
        return "{" + s[1 : len(s) - 1] + "}"

    def _position(self, x: T) -> Tuple[List[T], int, int]:
        "return the bucket, index of the bucket and position in which x should be. self must not be empty."
        for i, a in enumerate(self.a):
            if x <= a[-1]:
                break
        return (a, i, bisect_left(a, x))

    def __contains__(self, x: T) -> bool:
        if self.size == 0:
            return False
        a, _, i = self._position(x)
        return i != len(a) and a[i] == x

    def count(self, x: T) -> int:
        "Count the number of x."
        return self.index_right(x) - self.index(x)

    def add(self, x: T) -> None:
        "Add an element. / O(√N)"
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return
        a, b, i = self._position(x)
        a.insert(i, x)
        self.size += 1
        if len(a) > len(self.a) * self.SPLIT_RATIO:
            mid = len(a) >> 1
            self.a[b : b + 1] = [a[:mid], a[mid:]]

    def _pop(self, a: List[T], b: int, i: int) -> T:
        ans = a.pop(i)
        self.size -= 1
        if not a:
            del self.a[b]
        return ans

    def discard(self, x: T) -> bool:
        "Remove an element and return True if removed. / O(√N)"
        if self.size == 0:
            return False
        a, b, i = self._position(x)
        if i == len(a) or a[i] != x:
            return False
        self._pop(a, b, i)
        return True

    def lt(self, x: T) -> Optional[T]:
        "Find the largest element < x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] < x:
                return a[bisect_left(a, x) - 1]

    def le(self, x: T) -> Optional[T]:
        "Find the largest element <= x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] <= x:
                return a[bisect_right(a, x) - 1]

    def gt(self, x: T) -> Optional[T]:
        "Find the smallest element > x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] > x:
                return a[bisect_right(a, x)]

    def ge(self, x: T) -> Optional[T]:
        "Find the smallest element >= x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] >= x:
                return a[bisect_left(a, x)]

    def __getitem__(self, i: int) -> T:
        "Return the i-th element."
        if i < 0:
            for a in reversed(self.a):
                i += len(a)
                if i >= 0:
                    return a[i]
        else:
            for a in self.a:
                if i < len(a):
                    return a[i]
                i -= len(a)
        raise IndexError

    def pop(self, i: int = -1) -> T:
        "Pop and return the i-th element."
        if i < 0:
            for b, a in enumerate(reversed(self.a)):
                i += len(a)
                if i >= 0:
                    return self._pop(a, ~b, i)
        else:
            for b, a in enumerate(self.a):
                if i < len(a):
                    return self._pop(a, b, i)
                i -= len(a)
        raise IndexError

    def index(self, x: T) -> int:
        "Count the number of elements < x."
        ans = 0
        for a in self.a:
            if a[-1] >= x:
                return ans + bisect_left(a, x)
            ans += len(a)
        return ans

    def index_right(self, x: T) -> int:
        "Count the number of elements <= x."
        ans = 0
        for a in self.a:
            if a[-1] > x:
                return ans + bisect_right(a, x)
            ans += len(a)
        return ans


import random

random.seed(0)
write, flush = FastO.write, FastO.flush

#  -----------------------  #


def pred():
    _, q = map(int, input().split())
    s = input()
    tree = WBTSet(i for i, c in enumerate(s) if c == "1")
    for _ in range(q):
        c, k = map(int, input().split())
        if c == 0:
            tree.add(k)
            # tree.check()
        elif c == 1:
            tree.discard(k)
            # tree.check()
        elif c == 2:
            write(1 if k in tree else 0)
        elif c == 3:
            ans = tree.ge(k)
            write(-1 if ans is None else ans)
        else:
            ans = tree.le(k)
            write(-1 if ans is None else ans)
    flush()


def permutation():
    n, k = map(int, input().split())
    P = list(map(lambda x: int(x) - 1, input().split()))
    indx = [-1] * n
    for i, p in enumerate(P):
        indx[p] = i
    ans = 10**18
    ss = WBTSet(indx[:k])
    ans = min(ans, ss[-1] - ss[0])
    for i in range(k, n):
        ss.discard(indx[i - k])
        ss.add(indx[i])
        ans = min(ans, ss[-1] - ss[0])
    print(ans)


def data():
    q = int(input())
    s = WBTSet()
    ans = []
    for _ in range(q):
        t, x = map(int, input().split())
        if t == 1:
            s.add(x)
        else:
            ans.append(s.pop(x - 1))
    if ans:
        print("\n".join(map(str, ans)))


def prefix():
    n, k = map(int, input().split())
    P = list(map(int, input().split()))
    ans = []
    s = WBTSet()
    for i in range(k):
        s.add(P[i])
    ans.append(s.get_min())
    for i in range(k, n):
        if s.get_min() < P[i]:
            s.pop_min()
            s.add(P[i])
        ans.append(s.get_min())
    print("\n".join(map(str, ans)))


def call():
    n = int(input())
    A = list(map(lambda x: int(x) - 1, input().split()))
    s = WBTSet(range(n))
    for i in range(n):
        if i in s:
            s.discard(A[i])
    a = s.tolist()
    print(len(a))
    print(" ".join(map(lambda x: str(x + 1), a)))


def cutting():
    input = lambda: sys.stdin.buffer.readline().rstrip()
    l, q = map(int, input().split())
    tree = WBTSet([0, l])
    for _ in range(q):
        c, x = map(int, input().split())
        if c == 1:
            tree.add(x)
        else:
            it = tree.lt_iter(x)
            write((it + 1).key - it.key)
    flush()


def ranking():
    input = lambda: sys.stdin.buffer.readline().rstrip()

    n, q = map(int, input().split())
    P = list(map(int, input().split()))

    bit = 20
    msk = (1 << bit) - 1

    tree = WBTSet([p << bit | i for i, p in enumerate(P)])

    for _ in range(q):
        c, *qu = map(int, input().split())
        if c == 1:
            a, x = qu
            a -= 1
            tree.discard(P[a] << bit | a)
            P[a] = x
            tree.add(x << bit | a)
        elif c == 2:
            a = qu[0]
            a -= 1
            write(n - tree.index(P[a] << bit | a))
        else:
            r = qu[0]
            write((tree[-r] & msk) + 1)
    flush()


def double_end():
    input = lambda: sys.stdin.buffer.readline().rstrip()
    n, q = map(int, input().split())
    S = list(map(int, input().split()))
    tree = WBTMultiset(S)
    for _ in range(q):
        qu = list(map(int, input().split()))
        if qu[0] == 0:
            tree.add(qu[1])
        elif qu[0] == 1:
            write(tree.pop_min())
        else:
            write(tree.pop_max())
    flush()


def jealous():
    from collections import defaultdict

    n = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    AB = [(A[i], -B[i]) for i in range(n)]
    AB.sort()
    ab = []
    ab = [(AB[i][0], -AB[i][1]) for i in range(n)]
    dic = defaultdict(int)
    for i in ab:
        dic[i] += 1

    tree = WBTMultiset()
    ans = 0
    for i in range(n):
        tree.add(ab[i][1])
        ans += dic[ab[i]] - 1
        dic[ab[i]] -= 1
        ans += len(tree) - tree.index(ab[i][1])
    print(ans)


def sequence_query():
    input = lambda: sys.stdin.buffer.readline().rstrip()

    # q = int(input())
    # tree = WBTMultiset()

    # for _ in range(q):
    #     com, *qu = tuple(map(int, input().split()))
    #     if com == 1:
    #         x = qu[0]
    #         tree.add(x)
    #     elif com == 2:
    #         x, k = qu
    #         indx = tree.index_right(x)
    #         write(tree[indx - k] if indx - k >= 0 else -1)
    #     else:
    #         x, k = qu
    #         indx = tree.index(x)
    #         write(tree[indx + k - 1] if indx + k - 1 < len(tree) else -1)
    # flush()

    q = int(input())
    tree = WBTMultiset()

    def q2(x, k):
        it = tree.le_iter(x)
        if it is None:
            write(-1)
            return
        while k > 0:
            if it.count >= k:
                write(it.key)
                return
            k -= it.count
            it -= 1
            if it is None:
                write(-1)
                return

    def q3(x, k):
        it = tree.ge_iter(x)
        if it is None:
            write(-1)
            return
        while k > 0:
            if it.count >= k:
                write(it.key)
                return
            k -= it.count
            it += 1
            if it is None:
                write(-1)
                return

    for _ in range(q):
        qu = list(map(int, input().split()))
        if qu[0] == 1:
            x = qu[1]
            tree.add(x)
        elif qu[0] == 2:
            x, k = qu[1:]
            q2(x, k)
        else:
            x, k = qu[1:]
            q3(x, k)
    flush()


def jump_dist():
    n = int(input())
    XY = [tuple(map(int, input().split())) for _ in range(n)]

    def func(xy):
        n = len(xy)
        axy = []
        for u, v in xy:
            x = (u + v) // 2
            y = (u - v) // 2
            axy.append((x, y))
        xy = axy
        ans = 0

        xy.sort(key=lambda x: x[0])
        to_origin = sorted(set(y for _, y in xy))
        to_zaatsu = {x: i for i, x in enumerate(to_origin)}
        Y = SegmentTreeRSQ(n)
        yst = WBTMultiset()
        for i in range(n):
            x, y = xy[i]
            y_indx = to_zaatsu[y]
            ycnt = yst.index(y)
            ans += Y.prod(y_indx, n) - y * (len(yst) - ycnt)
            ans += y * ycnt - Y.prod(0, y_indx)
            Y[y_indx] += y
            yst.add(y)

        xy.sort(key=lambda x: x[1])
        to_origin = sorted(set(x for x, y in xy))
        to_zaatsu = {x: i for i, x in enumerate(to_origin)}
        X = SegmentTreeRSQ(n)
        xst = WBTMultiset()
        for i in range(n):
            x, _ = xy[i]
            x_indx = to_zaatsu[x]
            xcnt = xst.index(x)
            ans += X.prod(x_indx, n) - x * (len(xst) - xcnt)
            ans += x * xcnt - X.prod(0, x_indx)
            X[x_indx] += x
            xst.add(x)
        return ans

    same = []
    nonsame = []
    for x, y in XY:
        if x % 2 == y % 2:
            same.append((x, y))
        else:
            nonsame.append((x, y))
    # print(func(same))
    ans = func(same) + func(nonsame)
    print(ans)


def min_max():
    q = int(input())
    tree = WBTMultiset()
    for _ in range(q):
        com, *qu = map(int, input().split())
        if com == 1:
            x = qu[0]
            tree.add(x, 1)
        elif com == 2:
            x, c = qu
            tree.discard(x, c)
        else:
            print(tree[-1] - tree[0])


def chocolate():
    n, m = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    C = list(map(int, input().split()))
    D = list(map(int, input().split()))

    AB = [[-A[i], -B[i], 1] for i in range(n)]
    CD = [[-C[i], -D[i], 0] for i in range(m)]
    ALL = AB + CD
    ALL.sort()
    # tree = WBTMultiset()
    tree = SortedMultiset()
    for x, y, t in ALL:
        x = -x
        y = -y
        if t == 0:
            tree.add(y)
        else:
            lim = tree.ge(y)
            if lim is None:
                print("No")
                exit()
            tree.discard(lim)
    print("Yes")


def main():
    M = 100
    tree = WBTMultiset(range(M))
    tree.check()
    a = list(range(M))
    for _ in range(10**5):
        com = random.randint(0, 2)
        x = random.randint(0, M)
        if com == 0 or len(tree) == 0:
            print(f"add({x})")
            tree.add(x)
            a.append(x)
            a.sort()
        else:
            print(f"discard({x})")
            tree.discard(x)
            if x in a:
                a.remove(x)

        print(tree)
        print(a)
        tree.check()
        for i in range(M + 1):
            # index(i)
            cnt_a = sum(1 for e in a if e < i)
            cnt_b = tree.index(i)
            assert cnt_a == cnt_b
        assert list(tree) == a


from time import process_time

start = process_time()

# data()
# pred()
permutation()
# prefix()
# call()
# cutting()
# ranking()

# double_end()
# jealous()
# sequence_query()
# jump_dist()
# min_max()
# chocolate()

# main()

du = process_time() - start
print(f"\n{du:.3f} sec", file=sys.stderr)
