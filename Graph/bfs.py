from typing import List, Tuple
from collections import deque
inf = float('inf')

def bfs(G: List[List[int]], s: int) -> List[int]:
  dist = [inf] * len(G)
  dist[s] = 0
  todo = deque([s])
  while todo:
    v = todo.popleft()
    nd = dist[v] + 1
    for x in G[v]:
      if dist[x] == inf:
        dist[x] = nd
        todo.append(x)
  return dist

'''Return (Path: from s to t, Dist: from s)'''
def bfs_path(G: List[List[int]], s: int, t: int) -> Tuple[List[int], List[int]]:
  prev = [-1] * len(G)
  dist = [inf] * len(G)
  dist[s] = 0
  todo = deque([s])
  while todo:
    v = todo.popleft()
    nd = dist[v] + 1
    for x in G[v]:
      if dist[x] == inf:
        dist[x] = nd
        prev[x] = v
        todo.append(x)
  if dist[t] == inf:
    return [], dist
  path = []
  d = dist[t]
  while prev[t] != -1:
    path.append(t)
    t = prev[t]
  path.append(t)
  return path[::-1], dist
