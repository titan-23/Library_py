from Library_py.DataStructures.SegmentTree.SegmentTree import SegmentTree
import random
_titan23_HashString_Mod = (1<<61)-1
_titan23_HashString_B = random.randint(37, 100000)

class HashStringBase():

  def __init__(self, n: int):
    self.n = n
    powb = [1] * (self.n+1)
    for i in range(1, self.n+1):
      powb[i] = powb[i-1] * _titan23_HashString_B % _titan23_HashString_Mod
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
    self.n = len(s)
    data = [0] * (self.n+1)
    for i in range(1, self.n+1):
      data[i] = ((_titan23_HashString_B*data[i-1])%_titan23_HashString_Mod+ord(s[i-1])) % _titan23_HashString_Mod
    self.data = data
    self.used_seg = False
    op = lambda s, t: (self.hsb.unite(s[0], t[0], t[1]), s[1]+t[1])
    e  = (self.get(0, 0), 0)
    if update:
      self.seg = SegmentTree(((ord(s[i]), 1) for i in range(self.n)), op, e)

  def get(self, l: int, r: int) -> int:
    if self.used_seg:
      return self.seg.prod(l, r)[0]
    return (self.data[r] - (self.data[l]*self.hsb.powb[r-l])%_titan23_HashString_Mod) % _titan23_HashString_Mod

  def __getitem__(self, k: int) -> int:
    return self.get(k, k+1)

  def set(self, k: int, c: str) -> None:
    self.used_seg = True
    self.seg[k] = (ord(c), 1)

  def __setitem__(self, k: int, c: str) -> None:
    return self.set(k, c)

