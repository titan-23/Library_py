from titan_pylib.data_structures.union_find.undoable_union_find import UndoableUnionFind
from titan_pylib.graph.get_biconnected_components import get_biconnected_components
mod = 998244353

n, m = map(int, input().split())
G = [[] for _ in range(n)]
for _ in range(m):
  u, v = map(int, input().split())
  u -= 1; v -= 1
  G[u].append(v)
  G[v].append(u)

vertex, _ = get_biconnected_components(G)
uf = UndoableUnionFind(n)

def dfs(E, V, i=0, e_cnt=0) -> int:
  if i == len(E):
    if e_cnt == len(V)-1:
      return 1
    return 0
  cnt = dfs(E, V, i+1, e_cnt)
  u, v = E[i]
  if not uf.same(u, v):
    uf.unite(u, v)
    cnt += dfs(E, V, i+1, e_cnt+1)
    uf.undo()
  return cnt

ans = 1
for V in vertex:
  v_set = set(V)
  E = []
  for v in V:
    for x in G[v]:
      if x in v_set:
        s, t = min(v, x), max(v, x)
        E.append((s, t))
  E = list(set(E))
  ans *= dfs(E, V)
  ans %= mod
print(ans*(m-n+1) % mod)
