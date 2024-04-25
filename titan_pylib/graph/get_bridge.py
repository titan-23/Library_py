from titan_pylib.others.antirec import antirec
from typing import List, Tuple

def get_bridge(G: List[List[int]]) -> Tuple[List[int], List[Tuple[int, int]]]:
  # ref: https://algo-logic.info/bridge-lowlink/

  n = len(G)
  bridges = []
  articulation_points = []
  order = [-1] * n
  lowlink = [0] * n
  cur_time = 0

  @antirec
  def dfs(v: int, p: int=-1) -> None:
    nonlocal cur_time
    order[v] = cur_time
    lowlink[v] = cur_time
    cur_time += 1
    cnt = 0
    flag = False
    for x in G[v]:
      if x == p: continue
      if order[x] == -1:
        cnt += 1
        yield dfs(x, v)
        if p != -1 and order[v] <= lowlink[x]:
          flag = True
        lowlink[v] = min(lowlink[v], lowlink[x])
        if lowlink[x] > order[v]:
          bridges.append((x, v))
      else:
        lowlink[v] = min(lowlink[v], order[x])
    if p == -1 and cnt >= 2:
      flag = True
    if flag:
      articulation_points.append(v)
    yield
  for v in range(n):
    if order[v] == -1:
      dfs(v)
  return articulation_points, bridges
