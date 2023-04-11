from heapq import heapify, heappush, heappop
from collections import deque

dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

dx = [-1, -1, -1, 0, 0, 1, 1, 1]
dy = [1, 0, -1, 1, -1, 1, 0, -1]

#########################

def grid_dijkstra(F: list, s: tuple):
  h = len(F)
  w = len(F[0])
  G = [[] for _ in range(h)]
  for i in range(n):
    for j in range(n):
      if F[i][j] == '.':
        continue
      for x in range(len(dx)):
        ni, nj = i+dy[x], j+dx[x]
        if not (0 <= ni < h and 0 <= nj < w): continue
        if F[ni][nj] == '.':
          continue
        G[(i, j)].append((ni, nj))
  return dijkstra(G, s)

#########################
# kiacc
# 根からの距離distが必要

todo = deque([0])
while todo:
  v = todo.popleft()
  for x in G[v]:
    if dist[x] > dist[v]:
      acc_from_root[x] += acc_from_root[v]
      todo.append(x)

#################
"トポロジカルソートの数え上げ"

  for i in range(16):
    b[i] = 0
  n, m = map(int, input().split())
  for _ in range(m):
    x, y = map(int, input().split())
    x -= 1
    y -= 1
    b[x] |= (1 << y)

  for i in range(1 << 16):
    dp[i] = 0
  dp[0] = 1
  for i in range(1 << n):
    for j in range(n):
      if (i & (1 << j)) == 0 and (i & b[j]) == 0:
        dp[i | 1<<j] += dp[i]
  return dp[(1<<n)-1]

#################

sys.setrecursionlimit(10**6)
def get_articulation_points(G: list, s: int=0) -> list:
  "Return articulation points. / O(|V|+|E|)"
  n = len(G)
  order = [None] * n
  res = []
  cnt = 0
  def dfs(v, pre):
    nonlocal cnt
    r_min = order[v] = cnt
    fcnt = 0
    p_art = 0
    cnt += 1
    for w in G[v]:
      if w == pre:
        continue
      if order[w] == None:
        ret = dfs(w, v)
        p_art |= (order[v] <= ret)
        r_min = min(r_min, ret)
        fcnt += 1
      else:
        r_min = min(r_min, order[w])
    p_art |= (r_min == order[v] and len(G[v]) > 1)
    if (pre == -1 and fcnt > 1) or (pre != -1 and p_art):
      res.append(v)
    return r_min
  dfs(s, -1)
  return res

#################
sys.setrecursionlimit(10**6)
def get_bridge(G: list) -> list:
  "Return bridge of G. / O(|V|+|E|)"
  n = len(G)
  order = [-1] * n
  lowlink = [inf] * n
  k = 0
  def dfs1(v, p):
    nonlocal k
    order[v] = lowlink[v] = k
    k += 1
    for x in G[v]:
      if x == p:
        continue
      if order[x] == -1:
        dfs1(x, v)
        if lowlink[v] > lowlink[x]:
          lowlink[v] = lowlink[x]
      else:
        if lowlink[v] > order[x]:
          lowlink[v] = order[x]
  dfs1(0, -1)

  res = []
  seen = [0] * n
  def dfs2(v, p):
    seen[v] = 1
    for x in G[v]:
      if seen[x]:
        continue
      # vとxが橋かどうか
      if order[v] < lowlink[x]:
        res.append([v, x])
      dfs2(x, v)
  dfs2(0, -1)

  return res

#################
def grid_bfs(field, sx, sy, tx, ty, ok='.', ng='#'):
  dx = [0, 1, 0, -1]
  dy = [1, 0, -1, 0]
  #     ↓ → ↑ ←
  n = len(field)
  m = len(field[0])
  dist = [[-1]*m for _ in range(n)]
  dist[sy][sx] = 0
  todo = deque([(sy, sx)])
  while todo:
    vy, vx = todo.popleft()
    for d in range(4):
      ny, nx = vy+dy[d], vx+dx[d]
      if 0 <= ny < n and 0 <= nx < m:
        if field[ny][nx] == ng or dist[ny][nx] != -1:
          continue
        dist[ny][nx] = dist[vy][vx] + 1
        if ny == ty and nx == tx:
          break
        todo.append((ny, nx))
    else:
      continue
    break
  # return dist

  direct = ('U', 'L', 'D', 'R')
  fukugen = []
  di = dist[ty][tx]
  gy, gx = ty, tx
  while di:
    for d in range(4):
      ny, nx = gy+dy[d], gx+dx[d]
      if 0 <= ny < n and 0 <= nx < m:
        if dist[ny][nx] == di - 1:
          di -= 1
          fukugen.append(direct[d])
          if ny == sy and nx == sx:
            break
          gy, gx = ny, nx
          break
  return fukugen[::-1]
