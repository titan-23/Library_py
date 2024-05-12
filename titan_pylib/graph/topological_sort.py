from heapq import heapify, heappush, heappop

# len(toposo) != n: 閉路が存在


def topological_sort_min(G: list[list[int]]) -> list[int]:
    n = len(G)
    d = [0] * n
    F = [[] for _ in range(n)]
    for i in range(n):
        for x in G[i]:
            d[x] += 1
            F[x].append(i)
    hq = [i for i, a in enumerate(d) if not a]
    heapify(hq)
    ret = []
    while hq:
        v = heappop(hq)
        ret.append(v)
        for x in F[v]:
            d[x] -= 1
            if d[x] == 0:
                heappush(hq, x)
    return ret


from typing import list

"""Return topological_sort. / O(|V|+|E|)"""


def topological_sort(G: list[list[int]]) -> list[int]:
    n = len(G)
    d = [0] * n
    outs = [[] for _ in range(n)]
    for v in range(n):
        for x in G[v]:
            d[x] += 1
            outs[v].append(x)
    res = []
    todo = [i for i in range(n) if d[i] == 0]
    while todo:
        v = todo.pop()
        res.append(v)
        for x in outs[v]:
            d[x] -= 1
            if d[x] == 0:
                todo.append(x)
    return res
