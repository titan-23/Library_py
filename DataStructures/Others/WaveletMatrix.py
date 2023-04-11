# 参考: https://judge.yosupo.jp/submission/33990
class FullyIndexableDictionary:

  def __init__(self, size):
    self._size = size
    self._block = (size + 31) >> 5
    self._bit = [0] * self._block
    self._sum = [0] * self._block

  def _popcount(self, x):
    x = x - ((x >> 1) & 0x55555555)
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
    x = x + (x >> 4) & 0x0f0f0f0f
    x = x + (x >> 8)
    x = x + (x >> 16)
    return x & 0x0000007f

  def set(self, k: int):
    self._bit[k >> 5] |= 1 << (k & 31)

  def build(self):
    for i in range(1, self._block):
      self._sum[i] = self._sum[i - 1] + self._popcount(self._bit[i - 1])

  def access(self, k: int):
    return (self._bit[k >> 5] >> (k & 31)) & 1

  def rank(self, k: int, v: int):
    r = self._sum[k >> 5] + self._popcount(self._bit[k >> 5] & ((1 << (k & 31)) - 1))
    return r if v else k - r

  def select(self, k: int, v: int):
    if k < 0 or self.rank(self._size, v) <= k: return -1
    l, r = 0, self._size
    while r - l > 1:
      m = (l + r) // 2
      if self.rank(m, v) >= k + 1:
        r = m
      else:
        l = m
    return l


class WaveletMatrix:

  def __init__(self, log=32):
    self._size = 0
    self._log = log
    self._mat = [None] * log
    self._mid = [None] * log

  def build(self, arr: list):
    self._size = len(arr)
    for lv in range(self._log)[::-1]:
      self._mat[lv] = FullyIndexableDictionary(self._size+1)
      lt = []
      rt = []
      for i, a in enumerate(arr):
        if (a >> lv) & 1:
          self._mat[lv].set(i)
          rt.append(a)
        else:
          lt.append(a)
      self._mid[lv] = len(lt)
      self._mat[lv].build()
      arr = lt + rt

  def access(self, k: int):
    "Return A[k]. / O(log)"
    res = 0
    for lv in range(self._log)[::-1]:
      if self._mat[lv].access(k):
        res |= 1 << lv
        k = self._mat[lv].rank(k, 1) + self._mid[lv]
      else:
        k = self._mat[lv].rank(k, 0)
    return res

  def rank(self, x: int, r: int):
    "[0, r)にxがいくつあるか"
    l = 0
    for lv in range(self._log)[::-1]:
      if (x >> lv) & 1:
        l = self._mat[lv].rank(l, 1) + self._mid[lv]
        r = self._mat[lv].rank(r, 1) + self._mid[lv]
      else:
        l = self._mat[lv].rank(l, 0)
        r = self._mat[lv].rank(r, 0)
    return r - l

  def select(self, x: int, k: int):
    "k個目のxの次の位置"
    res = 0
    for lv in range(self._log)[::-1]:
      if (x >> lv) & 1:
        res = self._mat[lv].rank(self._size, 0) + self._mat[lv].rank(res, 1)
      else:
        res = self._mat[lv].rank(res, 0)
    res += k
    for lv in range(self._log):
      if (x >> lv) & 1:
        res = self._mat[lv].select(res - self._mat[lv].rank(self._size, 0), 1)
      else:
        res = self._mat[lv].select(res, 0)
    return res

  def quantile(self, l: int, r: int, k: int):
    "[l, r)の中でk番目(0スタート)に小さい値を返す"
    res = 0
    for lv in range(self._log)[::-1]:
      cnt = self._mat[lv].rank(r, 0) - self._mat[lv].rank(l, 0)
      if cnt <= k:
        res |= 1 << lv
        k -= cnt
        l = self._mat[lv].rank(l, 1) + self._mid[lv]
        r = self._mat[lv].rank(r, 1) + self._mid[lv]
      else:
        l = self._mat[lv].rank(l, 0)
        r = self._mat[lv].rank(r, 0)
    return res

  def topk(self, l: int, r: int, k: int):
    "[l, r)中で出現回数が多い順にその頻度とともにk個返す"
    pass

  def sum(self, l: int, r: int):
    "Return sum( [l, r) )."
    pass

  def rangefreq(self, l: int, r: int, x: int, y: int):
    "[l, r) 中に出現するx <= c < yを満たす値の合計出現数を返す"
    pass

  def rangelist(self, l: int, r: int, x: int, y: int):
    "[l, r) 中に出現するx <= c < yを満たす値を頻度とともに列挙する"
    pass

  def rangemaxk(self, l: int, r: int, k: int):
    "[l, r) 中に出現する値を大きい順にその頻度とともにk個返す"
    pass

  def rangemink(self, l: int, r: int, k: int):
    "[l, r) 中に出現する値を小さい順にその頻度とともにk個返す"
    pass

  def prevvalue(self, l: int, r: int, x: int, y: int):
    "[l, r) 中にでx <= c < yを満たす最大のcを返す"
    pass

  def nextvalue(self, l: int, r: int, x: int, y: int):
    "[l, r) 中にでx <= c < yを満たす最小のcを返す"
    pass

  def intersect(self, l1: int, r1: int, l2: int, r2: int):
    "[l1, r1) と [l2, r2)の間で共通して出現する値と頻度を返す"
    pass


