from typing import List, Tuple, Union
from collections import deque

def bfs(G: List[List[Tuple[int, int]]], s: int, inf: Union[int, float]=float('inf')) -> List[Union[int, float]]:
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

'''Return Tuple[Path: from s to t, Dist: from s]'''
def bfs_path(G: List[List[Tuple[int, int]]], s: int, t: int, inf: Union[int, float]=float('inf')) -> Tuple[List[int], List[Union[int, float]]]:
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
