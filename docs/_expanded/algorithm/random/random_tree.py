# from titan_pylib.algorithm.random.random_tree import RandomTree
# from titan_pylib.data_structures.heap.deletable_min_heap import DeletableMinHeap
# from titan_pylib.data_structures.heap.min_heap import MinHeap
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Protocol


class SupportsLessThan(Protocol):

    def __lt__(self, other) -> bool: ...
from typing import TypeVar, Generic, Iterable

T = TypeVar("T", bound=SupportsLessThan)


class MinHeap(Generic[T]):

    def __init__(self, a: Iterable[T] = []) -> None:
        self.a = list(a)
        self._heapify()

    def _heapify(self) -> None:
        for i in range(len(self.a) - 1, -1, -1):
            self._down(i)

    def _down(self, i: int) -> None:
        a = self.a
        n = len(a)
        while i * 2 + 1 < n:
            u, v = i * 2 + 1, i * 2 + 2
            if v < n and a[u] > a[v]:
                u = v
            if a[i] > a[u]:
                a[i], a[u] = a[u], a[i]
                i = u
            else:
                break

    def _up(self, i: int) -> None:
        a = self.a
        while i > 0:
            p = (i - 1) >> 1
            if a[i] < a[p]:
                a[i], a[p] = a[p], a[i]
                i = p
            else:
                break

    def get_min(self) -> T:
        return self.a[0]

    def pop_min(self) -> T:
        res = self.a[0]
        self.a[0] = self.a[-1]
        self.a.pop()
        self._down(0)
        return res

    def push(self, key: T) -> None:
        self.a.append(key)
        self._up(len(self.a) - 1)

    def pushpop_min(self, key: T) -> T:
        if self.a[0] > key or self.a[0] == key:
            return key
        res = self.a[0]
        self.a[0] = key
        self._down(0)
        return res

    def replace_min(self, key: T) -> T:
        res = self.a[0]
        self.a[0] = key
        self._down(0)
        return res

    def __getitem__(self, k: int) -> T:
        assert k == 0
        return self.a[0]

    def tolist(self) -> list[T]:
        return sorted(self.a)

    def __len__(self):
        return len(self.a)

    def __str__(self):
        return str(self.a)

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import TypeVar, Generic, Iterable

T = TypeVar("T", bound=SupportsLessThan)


class DeletableMinHeap(Generic[T]):

    def __init__(self, a: Iterable[T] = []) -> None:
        """削除可能Minヒープです。
        要素の 追加/削除/最小値取得 が効率よく行えます。
        """
        self.hq: MinHeap[T] = MinHeap(a)
        self.rem_hq: MinHeap[T] = MinHeap()
        self._len: int = len(self.hq)

    def push(self, key: T) -> None:
        """``key`` を追加します。
        :math:`O(\\log{n})` です。
        """
        self._len += 1
        if self.rem_hq and self.rem_hq.get_min() == key:
            self.rem_hq.pop_min()
            return
        self.hq.push(key)

    def remove(self, key: T) -> None:
        """``key`` を削除します。
        :math:`O(\\log{n})` です。
        """
        assert self._len > 0
        self._len -= 1
        if self.hq.get_min() == key:
            self.hq.pop_min()
        else:
            self.rem_hq.push(key)

    def _delete(self) -> None:
        while self.rem_hq and self.rem_hq.get_min() == self.hq.get_min():
            self.hq.pop_min()
            self.rem_hq.pop_min()

    def get_min(self) -> T:
        """最小の要素を返します。
        :math:`O(\\log{n})` です。
        """
        assert self._len > 0
        self._delete()
        return self.hq.get_min()

    def pop_min(self) -> T:
        """最小の要素を削除して返します。
        :math:`O(\\log{n})` です。
        """
        assert self._len > 0
        self._len -= 1
        self._delete()
        return self.hq.pop_min()

    def __len__(self) -> int:
        return self._len
import enum
from typing import Optional
import random


class RandomTreeType(enum.Enum):
    """``RandomTree`` で木の形を指定するときに使用する列挙型クラスです。"""

    random = enum.auto()
    path = enum.auto()
    star = enum.auto()


class RandomTree:

    @classmethod
    def build(
        cls,
        n: int,
        typ: RandomTreeType = RandomTreeType.random,
        seed: Optional[int] = None,
    ) -> list[tuple[int, int]]:
        """ランダムな木を生成し、辺を返します。
        :math:`O(n \\log{n})` です。

        Args:
            n (int): 頂点の数です。
            typ (RandomTreeType, optional): 木の形です。 Defaults to RandomTreeType.random。
            seed (Optional[int], optional): seed値です。 Defaults to None。

        Returns:
            list[tuple[int, int]]: 辺のリストです。辺のインデックスは 0-indexed です。
        """
        cls.rand = random.Random(seed)
        edges = None
        if typ == RandomTreeType.random:
            edges = cls._build_random(n)
        elif typ == RandomTreeType.path:
            edges = cls._build_path(n)
        elif typ == RandomTreeType.star:
            edges = cls._build_star(n)
        assert (
            edges is not None
        ), f"{cls.__class__.__name__}.build({typ}), typ is not defined."
        cls.rand.shuffle(edges)
        return edges

    @classmethod
    def _build_star(cls, n: int) -> list[tuple[int, int]]:
        center = cls.rand.randrange(0, n)
        edges = []
        for i in range(n):
            if i == center:
                continue
            if cls.rand.random() < 0.5:
                edges.append((center, i))
            else:
                edges.append((i, center))
        return edges

    @classmethod
    def _build_path(cls, n: int) -> list[tuple[int, int]]:
        p = list(range(n))
        cls.rand.shuffle(p)
        edges = [
            (p[i], p[i + 1]) if cls.rand.random() < 0.5 else (p[i + 1], p[i])
            for i in range(n - 1)
        ]
        return edges

    @classmethod
    def _build_random(cls, n: int) -> list[tuple[int, int]]:
        edges = []
        D = [1] * n
        A = [0] * (n - 2)
        for i in range(n - 2):
            v = cls.rand.randrange(0, n)
            D[v] += 1
            A[i] = v
        avl: DeletableMinHeap[tuple[int, int]] = DeletableMinHeap(
            (D[i], i) for i in range(n)
        )
        for a in A:
            d, v = avl.pop_min()
            assert d == 1
            edges.append((v, a))
            D[v] -= 1
            avl.remove((D[a], a))
            D[a] -= 1
            if D[a] >= 1:
                avl.push((D[a], a))
        u = D.index(1)
        D[u] -= 1
        v = D.index(1)
        D[v] -= 1
        edges.append((u, v))
        return edges
