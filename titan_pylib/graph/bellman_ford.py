from typing import List, Optional, Union, Tuple

def bellman_ford(G: List[List[Tuple[int, int]]], s: int, inf: Union[int, float]=float('inf')) -> Optional[List[Union[int, float]]]:
  '''Return dist from s. / O(nm)'''
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

