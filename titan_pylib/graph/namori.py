from typing import List


class Namori:

    def __init__(self, G: List[List[int]]):
        n = len(G)
        deg = [0] * n
        for v in range(n):
            for x in G[v]:
                deg[x] += 1
        todo = [i for i, x in enumerate(deg) if x == 1]
        cycle = set(range(n))
        while todo:
            v = todo.pop()
            cycle.discard(v)
            for x in G[v]:
                deg[x] -= 1
                if deg[x] == 1:
                    todo.append(x)
        tree = []
        treeid = [-1] * n
        now = 0
        cycle_list = list(cycle)
        for i in cycle_list:
            tmp = []
            todo = [i]
            treeid[i] = now
            while todo:
                v = todo.pop()
                tmp.append(v)
                for x in G[v]:
                    if treeid[x] != -1 or x in cycle:
                        continue
                    todo.append(x)
                    treeid[x] = now
            now += 1
            tree.append(tmp)
        # tree[i][j]:= cycle[i]を根とする木
        # tree[i][0]は常に根
        self.cycle = cycle_list
        self.tree = tree
        self.treeid = treeid

    def same_tree(self, u: int, v: int) -> bool:
        return self.treeid[u] == self.treeid[v]

    def get_cycle(self):
        return self.cycle

    def get_tree(self):
        return self.tree
