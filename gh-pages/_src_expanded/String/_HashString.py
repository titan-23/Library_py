raise NotImplementedError

from Library_py.DataStructures.SegmentTree.SegmentTree import SegmentTree
'''
逃避数列加算ができれば一点更新可能
かけ算最適化してないので使わないこと！
'''
from typing import Optional
import random
import string
_titan23_HashString_Mod = (1<<61)-1
_titan23_HashString_Dic = {c: i for i, c in enumerate(string.ascii_lowercase)}

class HashStringBase():

  def __init__(self, n: int, seed: Optional[int]=None):
    random.seed(seed)
    base = random.randint(37, 10**9)
    self.n = n
    powb = [1] * (self.n+1)
    for i in range(1, self.n+1):
      powb[i] = powb[i-1] * base % _titan23_HashString_Mod
    self.base = base
    self.powb = powb

  def unite(self, h1: int, h2: int, k: int) -> int:
    '''
    h1, h2, k
    len(h2) == k
    h1 <- h2
    '''
    return ((h1 * self.powb[k])%_titan23_HashString_Mod + h2)%_titan23_HashString_Mod

class HashString():

  def __init__(self, hsb: HashStringBase, s: str, update: bool=False):
    self.hsb = hsb
    base = hsb.base
    self.n = len(s)
    data = [0] * (self.n+1)
    for i in range(1, self.n+1):
      data[i] = ((base*data[i-1])%_titan23_HashString_Mod+_titan23_HashString_Dic[s[i-1]]) % _titan23_HashString_Mod
    self.data = data
    self.used_seg = False
    op = lambda s, t: (self.hsb.unite(s[0], t[0], t[1]), s[1]+t[1])
    e  = (self.get(0, 0), 0)
    if update:
      self.seg = SegmentTree(((_titan23_HashString_Dic[s[i]], 1) for i in range(self.n)), op, e)

  def get(self, l: int, r: int) -> int:
    if self.used_seg:
      return self.seg.prod(l, r)[0]
    return (self.data[r] - (self.data[l]*self.hsb.powb[r-l])%_titan23_HashString_Mod) % _titan23_HashString_Mod

  def __getitem__(self, k: int) -> int:
    return self.get(k, k+1)

  def set(self, k: int, c: str) -> None:
    self.used_seg = True
    self.seg[k] = (_titan23_HashString_Dic[c], 1)

  def __setitem__(self, k: int, c: str) -> None:
    return self.set(k, c)

