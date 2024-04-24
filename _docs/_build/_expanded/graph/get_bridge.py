# from titan_pylib.graph.get_bridge import get_bridge
# from titan_pylib.others.antirec import antirec
from types import GeneratorType
# ref: https://github.com/cheran-senthil/PyRival/blob/master/pyrival/misc/bootstrap.py
# ref: https://twitter.com/onakasuita_py/status/1731535542305907041

def antirec(func):
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

def antirec_cache(func):
  stack = []
  memo = {}
  args_list = []
  def wrappedfunc(*args):
    args_list.append(args)
    if stack:
      return func(*args)
    to = func(*args)
    while True:
      if args_list[-1] in memo:
        res = memo[args_list.pop()]
        if not stack:
          return res
        to = stack[-1].send(res)
        continue
      if isinstance(to, GeneratorType):
        stack.append(to)
        to = next(to)
      else:
        memo[args_list.pop()] = to
        stack.pop()
        if not stack:
          break
        to = stack[-1].send(to)
    return to
  return wrappedfunc
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

