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

from typing import List, Callable, Tuple, Generator

def rerooting_dp(G: List[List[Tuple[int, int]]], merge: Callable, apply: Callable, leaf: Callable, e):
  @antirec
  def dfs1(v: int, p: int) -> Generator:
    dp_v = dp[v]
    if p != -1 and len(dp_v) == 1:
      yield leaf(v)
    else:
      acc = e
      for i, (x, c) in enumerate(G[v]):
        if x == p: continue
        res = yield dfs1(x, v)
        dp_v[i] = apply(res, x, c, True)
        acc = merge(acc, dp_v[i])
      yield acc

  @antirec
  def dfs2(v: int, p: int, dp_p) -> Generator:
    dp_v = dp[v]
    G_v = G[v]
    for i, (x, _) in enumerate(G_v):
      if x == p:
        dp_v[i] = dp_p
        break
    d = len(dp_v)
    acc_l = [e] * (d + 1)
    acc_r = [e] * (d + 1)
    for i in range(d):
        acc_l[i+1] = merge(acc_l[i], apply(dp_v[i], G_v[i][0], G_v[i][1], False))
        acc_r[i+1] = merge(acc_r[i], apply(dp_v[-i-1], G_v[-i-1][0], G_v[-i-1][1], False))
    ans[v] = acc_l[-1]
    for i, (x, c) in enumerate(G_v):
      if x == p: continue
      yield dfs2(x, v, apply(merge(acc_l[i], acc_r[d-i-1]), v, c, True))
    yield

  dp = [[e]*len(g) for g in G]
  ans = [e] * len(G)
  dfs1(0, -1)
  dfs2(0, -1, e)
  return ans

def leaf(v: int):
  return

def merge(s, t):
  return

def apply(dp_x, x, edge, flag):
  # flag: (辺などを含む)加工をするかどうか
  return

e = None

