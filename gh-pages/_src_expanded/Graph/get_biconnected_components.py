# from Library_py.Graph.get_biconnected_components import get_biconnected_components
# from Library_py.Others.antirec import antirec
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

def get_biconnected_components(G: List[List[int]]) -> Tuple[List[List[int]], List[List[Tuple[int, int]]]]:
  n = len(G)
  order = [-1] * n
  lowlink = [-1] * n
  cur_time = 0
  stack = []
  edge_ans = []
  vertex_ans = []

  @antirec
  def dfs_rec(v: int, p: int=-1) -> None:
    nonlocal cur_time
    order[v] = cur_time
    lowlink[v] = cur_time
    cur_time += 1
    for x in G[v]:
      if x == p:
        continue
      if order[x] < order[v]:
        stack.append((min(v, x), max(v, x)))
      if order[x] == -1:
        yield dfs_rec(x, v)
        lowlink[v] = min(lowlink[v], lowlink[x])
        if lowlink[x] >= order[v]:
          vx = (min(x, v), max(x, v))
          this_edge_ans = []
          this_vertex_ans = set()
          while True:
            a, b = stack.pop()
            this_edge_ans.append((a, b))
            this_vertex_ans.add(a)
            this_vertex_ans.add(b)
            if vx == this_edge_ans[-1]:
              break
          edge_ans.append(this_edge_ans)
          vertex_ans.append(list(this_vertex_ans))
      else:
        lowlink[v] = min(lowlink[v], order[x])
    yield

  for root in range(n):
    if order[root] == -1:
      pre_len = len(vertex_ans)
      dfs_rec(root)
      if len(vertex_ans) == pre_len:
        vertex_ans.append([root])
        edge_ans.append([])
  return vertex_ans, edge_ans

