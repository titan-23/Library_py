from heapq import heapify, heappush, heappop

# len(toposo) != n: 閉路が存在


def topological_sort_min(G: list[list[int]]) -> list[int]:
    n = len(G)
    d = [0] * n
    for i in range(n):
        for x in G[i]:
            d[x] += 1
    hq = [i for i in range(n) if d[i] == 0]
    heapify(hq)
    ret = []
    while hq:
        v = heappop(hq)
        ret.append(v)
        for x in G[v]:
            d[x] -= 1
            if d[x] == 0:
                heappush(hq, x)
    return ret


def topological_sort(G: list[list[int]]) -> list[int]:
    """Return topological_sort. / O(|V|+|E|)"""
    n = len(G)
    d = [0] * n
    for v in range(n):
        for x in G[v]:
            d[x] += 1
    res = []
    todo = [i for i in range(n) if d[i] == 0]
    while todo:
        v = todo.pop()
        res.append(v)
        for x in G[v]:
            d[x] -= 1
            if d[x] == 0:
                todo.append(x)
    return res
