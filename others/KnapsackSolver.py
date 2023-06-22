from bisect import bisect_right, bisect_left

class KnapsackSolver():

  def __init__(self, N, W, VW):
    self.N = N
    self.W = W
    self.VW = VW

  def solve_hanbunzenrekkyo(self) -> int:
    def naive(vw):
      ret = []
      n = len(vw)
      for i in range(1<<n):
        value, weight = 0, 0
        for j in range(n):
          if i >> j & 1:
            value += vw[j][0]
            weight += vw[j][1]
        ret.append([weight, value])
      ret.sort()
      for i in range(len(ret)-1):
        ret[i+1][1] = max(ret[i+1][1], ret[i][1])
      return ret
    left, right = self.VW[:self.N//2], self.VW[self.N//2:]
    left_ret = naive(left)
    right_ret = naive(right)
    ans = 0
    for weight, value in left_ret:
      if weight > self.W: continue
      i = bisect_right(right_ret, [self.W-weight, float('inf')]) - 1
      ans = max(ans, value + right_ret[i][1])
    return ans

  def solve_dp_small_weight(self):
    dp = [-1] * (self.W+1)
    dp[0] = 0
    for i, (v, w) in enumerate(self.VW):
      ep = [-1] * (self.W+1)
      for j in range(self.W+1):
        if dp[j] == -1: continue
        ep[j] = max(ep[j], dp[j])
        if j+w <= self.W:
          ep[j+w] = max(ep[j+w], dp[j]+v)
      dp = ep
    return max(dp)

  def solve_dp_small_value(self) -> int:
    sum_v = sum(v for v, _ in self.VW)
    inf = float('inf')
    dp = [inf] * (sum_v+1)
    dp[0] = 0
    for i, (v, w) in enumerate(self.VW):
      ep = [inf] * (sum_v+1)
      for j in range(sum_v+1):
        if dp[j] == inf: continue
        ep[j] = min(ep[j], dp[j])
        if j+v <= sum_v:
          ep[j+v] = min(ep[j+v], dp[j]+w)
      dp = ep
    for j in range(sum_v, -1, -1):
      if dp[j] <= self.W:
        return j
    return -1

