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

from typing import List, Callable

def rerooting_dp(G: List[List[int]], op: Callable, add_root: Callable, e):
  dp = [[e]*len(g) for g in G]
  ans = [e] * len(G)

  @antirec
  def dfs(v, p):
    dp_v = dp[v]
    acc = e
    for i, x in enumerate(G[v]):
      if x == p: continue
      dp_v[i] = yield dfs(x, v)
      acc = op(acc, add_root(dp_v[i]))
    yield acc

  @antirec
  def dfs2(v, p, dp_p):
    dp_v = dp[v]
    for i, x in enumerate(G[v]):
      if x == p:
        dp_v[i] = dp_p
    d = len(G[v])
    acc_l = [e] * (d + 1)
    acc_r = [e] * (d + 1)
    for i in range(d):
      acc_l[i+1] = op(acc_l[i], add_root(dp_v[i]))
      acc_r[d-i-1] = op(acc_r[d-i], add_root(dp_v[d-i-1]))
    ans[v] = acc_l[-1]
    for i, x in enumerate(G[v]):
      if x == p: continue
      yield dfs2(x, v, op(acc_l[i], acc_r[i+1]))
    yield

  dfs(0, -1)
  dfs2(0, -1, e)
  return ans

def op(s, t):
  return

def add_root(s):
  return

e = None
