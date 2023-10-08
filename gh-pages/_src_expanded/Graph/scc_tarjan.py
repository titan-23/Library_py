from types import GeneratorType
# 再帰用デコレータ
# yieldにするのを忘れないこと
# 参考: https://github.com/cheran-senthil/PyRival/blob/master/pyrival/misc/bootstrap.py

def antirec(func, stack=[]):
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

def get_scc(G):

  n = len(G)

  def _csr(G):
    start = [0] * (n + 1)
    E = []
    # 後で重み付きに対応させる
    for v in range(n):
      for x in G[v]:
        E.append((v, x))
    elist = [0] * len(E)
    for e0,e1 in E:
      start[e0+1] += 1
    for i in range(1, n+1):
      start[i] += start[i-1]

    cnt = start[:]
    for e0,e1 in E:
      elist[cnt[e0]] = e1
      cnt[e0] += 1
    return start, elist

  start, elist = _csr(G)

  def _scc_ids():

    now_ord, group_num = 0, 0

    visited = []

    low = [0] * n
    ord_ = [-1] * n
    ids = [0] * n

    @antirec
    def _dfs(v):
      nonlocal now_ord, group_num, visited, low, ord_, ids

      low[v] = ord_[v] = now_ord
      now_ord += 1
      visited.append(v)

      for i in range(start[v], start[v+1]):
        to = elist[i]

        if ord_[to] == -1:
          yield _dfs(to)

          low[v] = min(low[v], low[to])
        else:
          low[v] = min(low[v], ord_[to])

      if low[v] == ord_[v]:
        while True:
          u = visited.pop()
          ord_[u] = n
          ids[u] = group_num
          if u == v:
            break
        group_num += 1

      yield

    for i in range(n):
      if ord_[i] == -1:
        _dfs(i)

    for i in range(n):
      ids[i] = group_num - 1 - ids[i]

    return group_num, ids

  group_num, ids = _scc_ids()
  groups = [[] for _ in range(group_num)]
  for i in range(n):
    groups[ids[i]].append(i)
  return groups
