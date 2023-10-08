from typing import List, Tuple, Union
from heapq import heappush, heappop
inf = float('inf')

def dijkstra(G: List[List[Tuple[int, int]]], s: int) -> List[Union[int, float]]:
  dist = [inf] * len(G)
  dist[s] = 0
  hq: List[Tuple[int, int]] = [(0, s)]
  while hq:
    d, v = heappop(hq)
    if dist[v] < d: continue
    for x, c in G[v]:
      if dist[x] > d + c:
        dist[x] = d + c
        heappush(hq, (d + c, x))
  return dist

def dijkstra_path(G: List[List[Tuple[int, int]]], s: int, t: int) -> Tuple[List[int], List[Union[int, float]]]:
  '''Return (Path: from s to t, Dist: from s)'''
  prev = [-1] * len(G)
  dist = [inf] * len(G)
  dist[s] = 0
  hq: List[Tuple[int, int]] = [(0, s)]
  while hq:
    d, v = heappop(hq)
    if dist[v] < d: continue
    for x, c in G[v]:
      if dist[x] > d + c:
        dist[x] = d + c
        prev[x] = v
        heappush(hq, (d + c, x))
  if dist[t] == inf:
    return [], dist
  path = []
  d = dist[t]
  while prev[t] != -1:
    path.append(t)
    t = prev[t]
  path.append(t)
  return path[::-1], dist
