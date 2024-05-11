# from titan_pylib.graph.warshall_floyd import warshall_floyd
from typing import List, Tuple, Union


def warshall_floyd(
    G: List[List[Tuple[int, int]]], INF: Union[int, float] = float("inf")
) -> List[List[Union[int, float]]]:
    """重み付き隣接リスト ``G`` に対し、全点対最短経路を返します。

    :math:`O(n^3)` です。

    Args:
        G (List[List[Tuple[int, int]]]): 重み付き隣接リストです。
        INF (Union[int, float], optional): 無限大です。

    Returns:
        List[List[Union[int, float]]]: dist[a][b] -> a to b
    """
    n = len(G)
    dist = [[INF] * n for _ in range(n)]
    for v in range(n):
        dist_v_ = dist[v]
        for x, c in G[v]:
            dist_v_[x] = c
        dist_v_[v] = 0
    for k in range(n):
        dist_k_ = dist[k]
        for i in range(n):
            dist_i_ = dist[i]
            dist_i_k_ = dist_i_[k]
            if dist_i_k_ == INF:
                continue
            for j, dist_k_j_ in enumerate(dist_k_):
                if dist_i_[j] > dist_i_k_ + dist_k_j_:
                    dist_i_[j] = dist_i_k_ + dist_k_j_
    return dist


from typing import List, Tuple, Union

"""Return min dist s.t. dist[a][b] -> a to b. / O(|n|^3)"""


def warshall_floyd(
    D: List[List[int]], INF: Union[int, float] = float("inf")
) -> List[List[Union[int, float]]]:
    n = len(D)
    dist = [d[:] for d in D]
    for k in range(n):
        dist_k_ = dist[k]
        for i in range(n):
            dist_i_ = dist[i]
            dist_i_k_ = dist_i_[k]
            if dist_i_k_ == INF:
                continue
            for j, dist_k_j_ in enumerate(dist_k_):
                if dist_i_[j] > dist_i_k_ + dist_k_j_:
                    dist_i_[j] = dist_i_k_ + dist_k_j_
    return dist


# from typing import List, Tuple, Union
# '''Return min dist s.t. dist[a][b] -> a to b. / O(|n|^3)'''
# def warshall_floyd(G: List[List[Tuple[int, int]]], INF: Union[int, float]=float('inf')) -> List[List[Union[int, float]]]:
#   n = len(G)
#   # dist = [dijkstra(G, s, INF) for s in range(n)]
#   dist = [[INF]*n for _ in range(n)]
#   for v in range(n):
#     for x, c in G[v]:
#       dist[v][x] = c
#     dist[v][v] = 0
#   for k in range(n):
#     for i in range(n):
#       if dist[i][k] == INF: continue
#       for j in range(n):
#         if dist[i][j] > dist[i][k] + dist[k][j]:
#           dist[i][j] = dist[i][k] + dist[k][j]
#         # elif dist[i][j] == dist[i][k] + dist[k][j]:
#         #   dist[i][j] = dist[i][k] + dist[k][j]
#   '''
#   for i in range(n):
#     if dist[i][i] < 0:
#       return 'NEGATIVE CYCLE'
#   '''
#   return dist
