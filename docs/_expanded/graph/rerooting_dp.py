# from titan_pylib.graph.rerooting_dp import rerooting_dp
from typing import List, Callable, Tuple, TypeVar
T = TypeVar('T')
E = TypeVar('E')

def rerooting_dp(G: List[List[Tuple[int, int]]],
                 merge: Callable[[T, T], T],
                 apply_vertex: Callable[[T, int], T],
                 apply_edge: Callable[[T, E, int, int], T],
                 e: T) -> None:
  n = len(G)

  dp: List[List[T]] = [[e]*len(g) for g in G]
  ans = [e] * len(G)

  root = 0
  par = [-2] * n
  par[root] = -1
  toposo = [root]

  todo = [root]
  while todo:
    v = todo.pop()
    for x, _ in G[v]:
      if par[x] != -2: continue
      par[x] = v
      toposo.append(x)
      todo.append(x)

  arr = [e] * n
  for v in toposo[::-1]:
    dp_v = dp[v]
    acc = e
    for i, (x, c) in enumerate(G[v]):
      if x == par[v]: continue
      dp_v[i] = apply_edge(arr[x], c, x, v)
      acc = merge(acc, dp_v[i])
    arr[v] = apply_vertex(acc, v)

  dp_par = [e] * n
  acc_l = [e] * (n + 1)
  acc_r = [e] * (n + 1)
  for v in toposo:
    dp_v = dp[v]
    for i, (x, _) in enumerate(G[v]):
      if x == par[v]:
        dp_v[i] = dp_par[v]
        break
    d = len(dp_v)
    for i in range(d):
      acc_l[i+1] = merge(acc_l[i], dp_v[i])
      acc_r[i+1] = merge(acc_r[i], dp_v[d-i-1])
    ans[v] = apply_vertex(acc_l[d], v)
    for i, (x, c) in enumerate(G[v]):
      if x == par[v]: continue
      dp_par[x] = apply_edge(apply_vertex(merge(acc_l[i], acc_r[d-i-1]), v,), c, v, x)
  return ans

"""
apply_vertex
       v          } return
 --------------   }
|  /   |   \  |   }
| o    o    o | } dp_x
| △   △   △ |
 --------------

apply_edge
  v      } return
  | } e
  x | } dp_x
  △|
"""

# def merge(s: T, t: T) -> T:
#   """``s`` , ``t`` をマージする"""
#   ...

# def apply_vertex(dp_x: T, v: int) -> T:
#   ...

# def apply_edge(dp_x: T, e: E, x: int, v: int) -> T:
#   ...

# e: T = ...

