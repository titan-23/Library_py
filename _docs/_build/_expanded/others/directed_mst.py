# from titan_pylib.others.directed_mst import directed_mst
# from titan_pylib.data_structures.union_find.union_find import UnionFind
from collections import defaultdict


class UnionFind:

    def __init__(self, n: int) -> None:
        """``n`` 個の要素からなる ``UnionFind`` を構築します。
        :math:`O(n)` です。
        """
        self._n: int = n
        self._group_numbers: int = n
        self._parents: list[int] = [-1] * n

    def root(self, x: int) -> int:
        """要素 ``x`` を含む集合の代表元を返します。
        :math:`O(\\alpha(n))` です。
        """
        a = x
        while self._parents[a] >= 0:
            a = self._parents[a]
        while self._parents[x] >= 0:
            y = x
            x = self._parents[x]
            self._parents[y] = a
        return a

    def unite(self, x: int, y: int) -> bool:
        """要素 ``x`` を含む集合と要素 ``y`` を含む集合を併合します。
        :math:`O(\\alpha(n))` です。

        Returns:
          bool: もともと同じ集合であれば ``False``、そうでなければ ``True`` を返します。
        """
        x = self.root(x)
        y = self.root(y)
        if x == y:
            return False
        self._group_numbers -= 1
        if self._parents[x] > self._parents[y]:
            x, y = y, x
        self._parents[x] += self._parents[y]
        self._parents[y] = x
        return True

    def unite_right(self, x: int, y: int) -> int:
        # x -> y
        x = self.root(x)
        y = self.root(y)
        if x == y:
            return x
        self._group_numbers -= 1
        self._parents[y] += self._parents[x]
        self._parents[x] = y
        return y

    def unite_left(self, x: int, y: int) -> int:
        # x <- y
        x = self.root(x)
        y = self.root(y)
        if x == y:
            return x
        self._group_numbers -= 1
        self._parents[x] += self._parents[y]
        self._parents[y] = x
        return x

    def size(self, x: int) -> int:
        """要素 ``x`` を含む集合の要素数を返します。
        :math:`O(\\alpha(n))` です。
        """
        return -self._parents[self.root(x)]

    def same(self, x: int, y: int) -> bool:
        """
        要素 ``x`` と ``y`` が同じ集合に属するなら ``True`` を、
        そうでないなら ``False`` を返します。
        :math:`O(\\alpha(n))` です。
        """
        return self.root(x) == self.root(y)

    def members(self, x: int) -> list[int]:
        """要素 ``x`` を含む集合を返します。"""
        x = self.root(x)
        return [i for i in range(self._n) if self.root(i) == x]

    def all_roots(self) -> list[int]:
        """全ての集合の代表元からなるリストを返します。
        :math:`O(n)` です。

        Returns:
          list[int]: 昇順であることが保証されます。
        """
        return [i for i, x in enumerate(self._parents) if x < 0]

    def group_count(self) -> int:
        """集合の総数を返します。
        :math:`O(1)` です。
        """
        return self._group_numbers

    def all_group_members(self) -> defaultdict:
        """
        key に代表元、 value に key を代表元とする集合のリストをもつ defaultdict を返します。
        :math:`O(n\\alpha(n))` です。
        """
        group_members = defaultdict(list)
        for member in range(self._n):
            group_members[self.root(member)].append(member)
        return group_members

    def clear(self) -> None:
        """集合の連結状態をなくします(初期状態に戻します)。
        :math:`O(n)` です。
        """
        self._group_numbers = self._n
        for i in range(self._n):
            self._parents[i] = -1

    def __str__(self) -> str:
        """よしなにします。
        :math:`O(n\\alpha(n))` です。
        """
        return (
            f"<{self.__class__.__name__}> [\n"
            + "\n".join(f"  {k}: {v}" for k, v in self.all_group_members().items())
            + "\n]"
        )


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
