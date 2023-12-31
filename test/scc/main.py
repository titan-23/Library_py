# from Library_py.Graph.get_scc import get_scc

from typing import List

def get_scc_lowlink(G: List[List[int]]) -> List[List[int]]:
  n = len(G)
  stack = [0] * n
  ptr = 0
  lowlink = [-1] * n
  order = [-1] * n
  ids = [0] * n
  cur_time = 0
  group_cnt = 0

  par = [-1] * n
  search_index = [0] * n

  def dfs(v: int) -> None:
    # https://nachiavivias.github.io/cp-library/column/2022/01.html
    nonlocal cur_time, ptr

    par[v] = -2
    while v >= 0:
      if search_index[v] == 0:
        # 行きがけ
        order[v] = cur_time
        lowlink[v] = cur_time
        cur_time += 1
        stack[ptr] = v; ptr += 1
      if search_index[v] == len(G[v]):
        # 帰りがけ
        if lowlink[v] == order[v]:
          nonlocal group_cnt
          while True:
            u = stack[ptr-1]; ptr -= 1
            order[u] = n
            ids[u] = group_cnt
            if u == v: break
          group_cnt += 1

        v = par[v]
        continue

      x = G[v][search_index[v]]
      search_index[v] += 1
      if par[x] != -1:
        # 後退辺
        lowlink[v] = min(lowlink[v], order[x])
        continue

      # DFS木の辺

      par[x] = v
      v = x

  for v in range(n):
    if order[v] == -1:
      dfs(v)

  groups = [[] for _ in range(group_cnt)]
  for v in range(n):
    groups[group_cnt-1-ids[v]].append(v)
  return groups

n, m = map(int, input().split())
G = [[] for _ in range(n)]
for _ in range(m):
  a, b = map(int, input().split())
  G[a].append(b)
scc = get_scc_lowlink(G)
# scc = get_scc(G)
print(len(scc))
for cycle in scc:
  print(len(cycle), ' '.join(map(str, cycle)))
