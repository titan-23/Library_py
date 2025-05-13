from random import Random
from typing import Optional
from titan_pylib.others.antirec import antirec
from titan_pylib.string.hash_string import HashStringBase


class HashRootedTree:

    def __init__(self, G: list[list[int]], root: int, seed=None) -> None:
        self.n = len(G)
        self.G = G
        self.root = root
        self.hs = [0] * self.n
        self._build(seed)

    def _build(self, seed: Optional[int]) -> None:
        G, hs = self.G, self.hs
        rnd = Random(seed)
        R = [rnd.randint(1, (1 << 61) - 1) for _ in range(self.n + 1)]
        base = HashStringBase()
        h = [0] * self.n

        @antirec
        def dfs(v, p):
            m = 1
            mh = 0
            for x in G[v]:
                if x == p:
                    continue
                yield dfs(x, v)
                mh = max(mh, h[x])
                m = base.get_mul(m, base.get_mod(R[h[x]] + hs[x]))
            hs[v] = m
            h[v] = mh + 1
            yield

        dfs(self.root, -1)

    def __getitem__(self, v: int) -> int:
        return self.hs[v]
