from titan_pylib.data_structures.union_find.union_find import UnionFind


class SkewHeap:

    class Node:
        def __init__(self, val):
            self.l = None
            self.r = None
            self.val = val
            self.add = 0

        def lazy_propagate(self):
            if self.l is not None:
                self.l.add += self.add
            if self.r is not None:
                self.r.add += self.add
            self.val += self.add
            self.add = 0

    def __init__(self):
        self.root = None

    def _meld(self, a, b):
        if a is None:
            return b
        if b is None:
            return a
        if b.val + b.add < a.val + a.add:
            a, b = b, a
        a.lazy_propagate()
        a.r = self._meld(a.r, b)
        a.l, a.r = a.r, a.l
        return a

    @property
    def min(self):
        self.root.lazy_propagate()
        return self.root.val

    def push(self, val):
        nd = self.Node(val)
        self.root = self._meld(self.root, nd)

    def pop(self):
        rt = self.root
        rt.lazy_propagate()
        self.root = self._meld(rt.l, rt.r)
        return rt.val

    def meld(self, other):
        self.root = self._meld(self.root, other.root)

    def add(self, val):
        self.root.add += val

    def empty(self):
        return self.root is None


def directed_mst(n, edges, root):
    OFFSET = len(edges)
    from_ = [0] * n
    from_cost = [0] * n
    from_heap = [SkewHeap() for _ in range(n)]

    uf = UnionFind(n)
    par_e = [-1] * m
    stem = [-1] * n
    used = [0] * n
    used[root] = 2
    idxs = []

    for idx, (fr, to, cost) in enumerate(edges):
        from_heap[to].push(cost * OFFSET + idx)

    res = 0
    for v in range(n):
        if used[v] != 0:
            continue
        processing = []
        chi_e = []
        cycle = 0
        while used[v] != 2:
            used[v] = 1
            processing.append(v)
            if from_heap[v].empty():
                return -1, par
            from_cost[v], idx = divmod(from_heap[v].pop(), OFFSET)
            from_[v] = uf.root(edges[idx][0])
            if stem[v] == -1:
                stem[v] = idx
            if from_[v] == v:
                continue
            res += from_cost[v]
            idxs.append(idx)
            while cycle:
                par_e[chi_e.pop()] = idx
                cycle -= 1
            chi_e.append(idx)
            if used[from_[v]] == 1:
                p = v
                while True:
                    if not from_heap[p].empty():
                        from_heap[p].add(-from_cost[p] * OFFSET)
                    if p != v:
                        uf.merge(v, p)
                        from_heap[v].meld(from_heap[p])
                    p = uf.root(from_[p])
                    cycle += 1
                    if p == v:
                        break
            else:
                v = from_[v]
        for v in processing:
            used[v] = 2

    used_e = [False] * m
    tree = [-1] * n
    for idx in reversed(idxs):
        if used_e[idx]:
            continue
        fr, to, cost = edges[idx]
        tree[to] = fr
        x = stem[to]
        while x != idx:
            used_e[x] = True
            x = par_e[x]
    return res, tree


n, m, root = map(int, input().split())
edges = [list(map(int, input().split())) for i in range(m)]


res, par = directed_mst(n, edges, root)
if res == -1:
    print(res)
else:
    print(res)
    print(*[p if p != -1 else i for i, p in enumerate(par)])
