from collections import deque
inf = float('inf')

# O(VE)
# 負のコストでもよい
# ベルマンフォードより高速かもしれない
def spfa(G, s):
  n = len(G)
  now = [0] * n
  dist = [inf] * n
  dq = deque([s])
  dist[s] = 0
  now[s] = 1
  cnt = [0] * n
  cnt[s] = 1
  while dq:
    v = dq.pop()
    now[v] = 0
    d = dist[v]
    for x, c in G[v]:
      if dist[x] > d + c:
        dist[x] = d + c
        if not now[x]:
          cnt[x] += 1
          if n <= cnt[x]:
            return None
          if dq and d + c < dq[0]:
            dq.appendleft(x)
          else:
            dq.append(x)
          now[x] = 1

  return dist
