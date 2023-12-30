from typing import List, Tuple, Union

'''Return min dist s.t. dist[a][b] -> a to b. / O(|n|^3)'''
def warshall_floyd(G: List[List[Tuple[int, int]]], INF: Union[int, float]=float('inf')) -> List[List[Union[int, float]]]:
  n = len(G)
  dist = [[INF]*n for _ in range(n)]
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
      if dist_i_k_ == INF: continue
      for j, dist_k_j_ in enumerate(dist_k_):
        if dist_i_[j] > dist_i_k_ + dist_k_j_:
          dist_i_[j] = dist_i_k_ + dist_k_j_
  return dist


from typing import List, Tuple, Union

'''Return min dist s.t. dist[a][b] -> a to b. / O(|n|^3)'''
def warshall_floyd(D: List[List[int]], INF: Union[int, float]=float('inf')) -> List[List[Union[int, float]]]:
  n = len(D)
  dist = [d[:] for d in D]
  for k in range(n):
    dist_k_ = dist[k]
    for i in range(n):
      dist_i_ = dist[i]
      dist_i_k_ = dist_i_[k]
      if dist_i_k_ == INF: continue
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

