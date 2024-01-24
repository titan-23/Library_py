# from titan_pylib.graph.get_biconnected_components import get_biconnected_components
from typing import List, Tuple

def get_biconnected_components(G: List[List[int]]) -> Tuple[List[List[int]], List[List[Tuple[int, int]]]]:
  """``G`` を二重頂点連結分解します。
  :math:`O(n+m)` です。

  Args:
    G (List[List[int]]): 隣接リストです。

  Returns:
    Tuple[List[List[int]], List[List[Tuple[int, int]]]]: ``(頂点集合), (辺集合)`` のタプルです。
  """
  n = len(G)
  order = [-1] * n
  lowlink = [-1] * n
  indx = [0] * n
  cur_time = 0
  stack = []
  edge_ans = []
  vertex_ans = []

  def dfs(v: int, p: int=-1) -> None:
    nonlocal cur_time
    dfs_stack = [(v, -1)]
    while dfs_stack:
      v, p = dfs_stack.pop()
      if v >= 0:
        if indx[v] == len(G[v]):
          continue
        if indx[v] == 0:
          order[v] = cur_time
          lowlink[v] = cur_time
          cur_time += 1
        while indx[v] < len(G[v]):
          x = G[v][indx[v]]
          indx[v] += 1
          if x == p:
            continue
          if order[x] < order[v]:
            stack.append((min(v, x), max(v, x)))
          if order[x] == -1:
            if indx[v] != len(G[v]):
              dfs_stack.append((v, p))
            dfs_stack.append((~x, v))
            dfs_stack.append((x, v))
            break
          else:
            lowlink[v] = min(lowlink[v], order[x])
      else:
        x, v = ~v, p
        lowlink[v] = min(lowlink[v], lowlink[x])
        if lowlink[x] >= order[v]:
          min_vx, max_vx = min(x, v), max(x, v)
          this_edge_ans, this_vertex_ans = [], []
          while True:
            a, b = stack.pop()
            this_edge_ans.append((a, b))
            this_vertex_ans.append(a)
            this_vertex_ans.append(b)
            if min_vx == a and max_vx == b:
              break
          edge_ans.append(this_edge_ans)
          vertex_ans.append(list(set(this_vertex_ans)))
  for root in range(n):
    if order[root] == -1:
      pre_len = len(vertex_ans)
      dfs(root)
      if len(vertex_ans) == pre_len:
        vertex_ans.append([root])
        edge_ans.append([])
  return vertex_ans, edge_ans


