from typing import List

def is_bipartite_graph(G: List[List[int]]) -> bool:
  col = [-1] * len(G)
  for i in range(len(G)):
    if col[i] != -1:
      continue
    col[i] = 0
    stack = [i]
    while stack:
      v = stack.pop()
      cx = 1 - col[v]
      for x in G[v]:
        if col[x] == -1:
          col[x] = cx
          stack.append(x)
        elif col[x] != cx:
          return False
  return False if -1 in col else True

