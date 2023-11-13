# from Library_py.Graph.get_bridge import get_bridge
from typing import List

'''Return bridge of G. / O(|V|+|E|)'''
# https://algo-logic.info/bridge-lowlink/
def get_bridge(G: List[List[int]]) -> List[int]:
  n = len(G)
  order = [-1] * n
  lowlink = [3*n] * n
  k = 0

  def antirec(func):
    # 再帰用デコレータ
    # yieldにするのを忘れないこと
    # 参考: https://github.com/cheran-senthil/PyRival/blob/master/pyrival/misc/bootstrap.py
    stack = []
    def wrappedfunc(*args, **kwargs):
      if stack:
        return func(*args, **kwargs)
      to = func(*args, **kwargs)
      while True:
        if isinstance(to, GeneratorType):
          stack.append(to)
          to = next(to)
        else:
          stack.pop()
          if not stack:
            break
          to = stack[-1].send(to)
      return to
    return wrappedfunc

  @antirec
  def dfs1(v: int, p: int) -> None:
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

  res: List[int] = []
  seen = [0] * n

  if not G:
    return res
  root = 0
  stack = [root]
  seen[root] = 1
  while stack:
    v = stack.pop()
    for x in G[v]:
      if seen[x]:
        continue
      seen[x] = 1
      if order[v] < lowlink[x]:
        res.append([v, x])
      stack.append(x)
  return res


