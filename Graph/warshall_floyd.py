from typing import List, Tuple
inf = float('inf')

'''Return min dist s.t. dist[a][b] -> a to b. / O(|n|^3)'''
def warshall_floyd(G: List[List[Tuple[int, int]]]) -> List[List[int]]:
  n = len(G)
  # dist = [dijkstra(G, s) for s in range(n)]
  dist = [[inf]*n for _ in range(n)]
  for v in range(n):
    for x, c in G[v]:
      dist[v][x] = c
    dist[v][v] = 0
  for k in range(n):
    for i in range(n):
      if dist[i][k] == inf: continue
      for j in range(n):
        if dist[i][j] > dist[i][k] + dist[k][j]:
          dist[i][j] = dist[i][k] + dist[k][j]
        # elif dist[i][j] == dist[i][k] + dist[k][j]:
        #   dist[i][j] = dist[i][k] + dist[k][j]
  '''
  for i in range(n):
    if dist[i][i] < 0:
      return 'NEGATIVE CYCLE'
  '''
  return dist

