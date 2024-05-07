from typing import List, Tuple, Union
from heapq import heappush, heappop


def dijkstra_bit(
    G: List[List[Tuple[int, int]]], s: int, INF: Union[int, float] = float("inf")
) -> List[Union[int, float]]:
    dist = [INF] * len(G)
    dist[s] = 0
    bit = len(G).bit_length()
    msk = (1 << bit) - 1
    hq: List[int] = [s]
    while hq:
        dv = heappop(hq)
        d = dv >> bit
        v = dv & msk
        if dist[v] < d:
            continue
        for x, c in G[v]:
            if dist[x] > d + c:
                dist[x] = d + c
                heappush(hq, (d + c) << bit | x)
    return dist


def dijkstra_path(
    G: List[List[Tuple[int, int]]],
    s: int,
    t: int,
    INF: Union[int, float] = float("inf"),
) -> Tuple[List[int], List[Union[int, float]]]:
    """Return (Path: from s to t, Dist: from s)"""
    prev = [-1] * len(G)
    dist = [INF] * len(G)
    dist[s] = 0
    hq: List[Tuple[int, int]] = [(0, s)]
    while hq:
        d, v = heappop(hq)
        if dist[v] < d:
            continue
        for x, c in G[v]:
            if dist[x] > d + c:
                dist[x] = d + c
                prev[x] = v
                heappush(hq, (d + c, x))
    if dist[t] == INF:
        return [], dist
    path = []
    d = dist[t]
    while prev[t] != -1:
        path.append(t)
        t = prev[t]
    path.append(t)
    return path[::-1], dist
