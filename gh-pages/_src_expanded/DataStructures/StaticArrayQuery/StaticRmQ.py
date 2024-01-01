# from Library_py.DataStructures.StaticArrayQuery.StaticRmQ import StaticRmQ
from typing import List, Iterable
from array import array

class StaticRmQ():

  class SparseTableRmQ():

    def __init__(self, a: List[int], INF: int):
      size = len(a)
      log = size.bit_length()-1
      data = [a] + [[]] * log
      for i in range(log):
        pre = data[i]
        l = 1 << i
        data[i+1] = [min(pre[j], pre[j+l]) for j in range(len(pre)-l)]
      self.size = size
      self.data = data
      self.INF = INF

    def prod(self, l: int, r: int) -> int:
      if l >= r: return self.INF
      u = (r-l).bit_length()-1
      return min(self.data[u][l], self.data[u][r-(1<<u)])

  def __init__(self, a: Iterable[int], INF=10**9):
    a = list(a)
    n = len(a)
    bucket_size = n.bit_length()//2 + 1
    bucket_size = 31
    bucket_cnt = (n + bucket_size - 1) // bucket_size
    bucket = [a[bucket_size*i:bucket_size*(i+1)] for i in range(bucket_cnt)]
    bucket_data = StaticRmQ.SparseTableRmQ([min(b) for b in bucket], INF)
    bucket_bit = array('I', bytes(4*bucket_size*bucket_cnt))

    for i, b in enumerate(bucket):
      stack = []
      for j, e in enumerate(b):
        g = -1
        while stack and b[stack[-1]] > e:
          stack.pop()
        if stack:
          g = stack[-1]
        stack.append(j)
        if g == -1: continue
        bucket_bit[i*bucket_size+j] = bucket_bit[i*bucket_size+g] | (1 << g)
    self.n = n
    self.INF = INF
    self.bucket_size = bucket_size
    self.bucket_data = bucket_data
    self.bucket = bucket
    self.bucket_bit = bucket_bit

  def prod(self, l: int, r: int) -> int:
    assert 0 <= l <= r <= self.n, \
        f'IndexError: {self.__class__.__name__}.prod({l}, {r}), n={self.n}'
    if l == r:
      return self.INF
    k1 = l // self.bucket_size
    k2 = r // self.bucket_size
    l -= k1 * self.bucket_size
    r -= k2 * self.bucket_size + 1
    if k1 == k2:
      bit = self.bucket_bit[k1*self.bucket_size+r] >> l
      return self.bucket[k1][(bit&(-bit)).bit_length()+l-1 if bit else r]
    ans = self.INF
    if l < len(self.bucket[k1]):
      bit = self.bucket_bit[k1*self.bucket_size+len(self.bucket[k1])-1] >> l
      ans = self.bucket[k1][(bit&(-bit)).bit_length()+l-1 if bit else -1]
    ans = min(ans, self.bucket_data.prod(k1+1, k2))
    if r >= 0:
      bit = self.bucket_bit[k2*self.bucket_size+r]
      ans = min(ans, self.bucket[k2][(bit&(-bit)).bit_length()-1 if bit else r])
    return ans


