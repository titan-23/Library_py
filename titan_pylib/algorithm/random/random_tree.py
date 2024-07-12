from titan_pylib.data_structures.avl_tree.avl_tree_set2 import AVLTreeSet2
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
        avl: AVLTreeSet2[tuple[int, int]] = AVLTreeSet2((D[i], i) for i in range(n))
        for a in A:
            d, v = avl.pop_min()
            assert d == 1
            edges.append((v, a))
            D[v] -= 1
            avl.remove((D[a], a))
            D[a] -= 1
            if D[a] >= 1:
                avl.add((D[a], a))
        u = D.index(1)
        D[u] -= 1
        v = D.index(1)
        D[v] -= 1
        edges.append((u, v))
        return edges
