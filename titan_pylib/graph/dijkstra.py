from typing import Union
from heapq import heappush, heappop


def dijkstra(
    G: list[list[tuple[int, int]]], s: int, INF: Union[int, float] = float("inf")
) -> list[Union[int, float]]:
    """ダイクストラです。

    Args:
      G (list[list[tuple[int, int]]]): 隣接リストです。
      s (int): 始点です。
      INF (Union[int, float], optional): 無限大です。

    Returns:
      list[Union[int, float]]: 各頂点について、 ``s`` からの最短距離を返します。
    """
    dist = [INF] * len(G)
    dist[s] = 0
    hq: list[tuple[int, int]] = [(0, s)]
    while hq:
        d, v = heappop(hq)
        if dist[v] < d:
            continue
        for x, c in G[v]:
            if dist[x] > d + c:
                dist[x] = d + c
                heappush(hq, (d + c, x))
    return dist
