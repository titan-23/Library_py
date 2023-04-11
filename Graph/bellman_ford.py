from typing import List, Union
inf = float('inf')

'''Return dist from s. / O(|V||E|)'''
def bellman_ford(G: List[List[int]], s: int) -> Union[List[int], None]:
  n = len(G)
  dist = [inf] * n
  dist[s] = 0
  for _ in range(n):
    update = 0
    for v, e in enumerate(G):
      for x, c in e:
        if dist[v] != inf and dist[v] + c < dist[x]:
          dist[x] = dist[v] + c
          update = 1
    if not update:
      break
  else:
    return None  # NEGATIVE CYCLE
  return dist

