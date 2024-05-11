from typing import List, Tuple, Union
from collections import deque


def bfs(
    G: List[List[Tuple[int, int]]], s: int, inf: Union[int, float] = float("inf")
) -> List[Union[int, float]]:
    """
    Args:
      G (List[List[Tuple[int, int]]]): 隣接リストです。
      s (int): 始点です。
      inf (Union[int, float], optional): 無限大です。

    Returns:
      List[Union[int, float]]: 始点 ``s`` からの距離です。
    """
    dist = [inf] * len(G)
    dist[s] = 0
    todo = deque([s])
    while todo:
        v = todo.popleft()
        for x, c in G[v]:
            if dist[x] == inf:
                dist[x] = dist[v] + c
                todo.append(x)
    return dist


def bfs_path(
    G: List[List[Tuple[int, int]]],
    s: int,
    t: int,
    inf: Union[int, float] = float("inf"),
) -> Tuple[List[int], List[Union[int, float]]]:
    """
    Args:
      G (List[List[Tuple[int, int]]]): 隣接リストです。
      s (int): 始点です。
      t (int): 終点です。
      inf (Union[int, float], optional): 無限大です。

    Returns:
      Tuple[List[int], List[Union[int, float]]]: ``s`` から ``t`` へのパスと、 ``s`` からの距離です。
    """
    prev = [-1] * len(G)
    dist = [inf] * len(G)
    dist[s] = 0
    todo = deque([s])
    while todo:
        v = todo.popleft()
        for x, c in G[v]:
            if dist[x] == inf:
                dist[x] = dist[v] + c
                prev[x] = v
                todo.append(x)
    if dist[t] == inf:
        return [], dist
    path = []
    while prev[t] != -1:
        path.append(t)
        t = prev[t]
    path.append(t)
    return path[::-1], dist
