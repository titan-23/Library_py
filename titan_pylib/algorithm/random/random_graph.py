import enum
from typing import Optional
import random


class RandomGraphType(enum.Enum):
    random = enum.auto()
    cycle = enum.auto()


class RandomGraph:

    @classmethod
    def build(
        cls,
        n: int,
        m: int,
        typ: RandomGraphType = RandomGraphType.random,
        seed: Optional[int] = None,
    ) -> list[tuple[int, int]]:
        cls.rand = random.Random(seed)
        if typ == RandomGraphType.random:
            return cls._build_random(n, m)
        if typ == RandomGraphType.cycle:
            return cls._build_cycle(n, m)
        raise ValueError(typ)

    @classmethod
    def _build_cycle(cls, n: int, m: int) -> list[tuple[int, int]]:
        assert m == n
        cycle = list(range(n))
        cls.rand.shuffle(cycle)
        cycle.append(cycle[-1])
        edges = [None] * n
        for i in range(n):
            u, v = cycle[i], cycle[i + 1]
            if cls.rand.random() < 0.5:
                edges[i] = (v, u)
            else:
                edges[i] = (u, v)
        cls.rand.shuffle(edges)
        assert len(edges) == m
        return edges

    @classmethod
    def _build_random(cls, n: int, m: int) -> list[tuple[int, int]]:
        assert m <= n * (n - 1) // 2
        edges = set()
        while len(edges) < m:
            u = cls.rand.randrange(0, n)
            v = cls.rand.randrange(0, n)
            while u == v:
                v = cls.rand.randrange(0, n)
            if u > v:
                u, v = v, u
            edges.add((u, v))
        edges = list(edges)
        for i in range(m):
            u, v = edges[i]
            if cls.rand.random() < 0.5:
                edges[i] = (v, u)
        cls.rand.shuffle(edges)
        assert len(edges) == m
        return edges
