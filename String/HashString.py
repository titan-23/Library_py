# ref: https://qiita.com/keymoon/items/11fac5627672a6d6a9f6
from Library_py.DataStructures.SegmentTree.SegmentTree import SegmentTree
from typing import Optional, List, Dict, Final
import random
import string
_titan23_HashString_MOD: Final[int] = (1 << 61) - 1
_titan23_HashString_DIC: Final[Dict[str, int]] = {c: i for i, c in enumerate(string.ascii_lowercase, 1)}
_titan23_HashString_MASK30: Final[int] = (1 << 30) - 1
_titan23_HashString_MASK31: Final[int] = (1 << 31) - 1
_titan23_HashString_MASK61: Final[int] = _titan23_HashString_MOD

class HashStringBase():

  def __init__(self, n: int, base: int=-1, seed: Optional[int]=None) -> None:
    random.seed(seed)
    base = random.randint(37, 10**9) if base < 0 else base
    powb = [1] * (n+1)
    invb = [1] * (n+1)
    invbpow = pow(base, -1, _titan23_HashString_MOD)
    for i in range(1, n+1):
      powb[i] = HashStringBase.get_mul(powb[i-1], base)
      invb[i] = HashStringBase.get_mul(invb[i-1], invbpow)
    self.n = n
    self.powb = powb
    self.invb = invb

  @staticmethod
  def get_mul(a: int, b: int) -> int:
    au = a >> 31
    ad = a & _titan23_HashString_MASK31
    bu = b >> 31
    bd = b & _titan23_HashString_MASK31
    mid = ad * bu + au * bd
    midu = mid >> 30
    midd = mid & _titan23_HashString_MASK30
    return HashStringBase.get_mod(au * bu * 2 + midu + (midd << 31) + ad * bd)

  @staticmethod
  def get_mod(x: int) -> int:
    xu = x >> 61
    xd = x & _titan23_HashString_MASK61
    res = xu + xd
    if res >= _titan23_HashString_MOD:
      res -= _titan23_HashString_MOD
    return res

  def unite(self, h1: int, h2: int, k: int) -> int:
    # len(h2) == k
    # h1 <- h2
    return self.get_mod(self.get_mul(h1, self.powb[k]) + h2)

class HashString():

  def __init__(self, hsb: HashStringBase, s: str, update: bool=False) -> None:
    n = len(s)
    data = [0] * n
    acc = [0] * (n+1)
    powb = hsb.powb
    for i, c in enumerate(s):
      data[i] = hsb.get_mul(powb[n-i-1], _titan23_HashString_DIC[c])
      acc[i+1] = hsb.get_mod(acc[i] + data[i])
    self.hsb = hsb
    self.n = n
    self.acc = acc
    self.used_seg = False
    if update:
      self.seg = SegmentTree(data, lambda s, t: (s+t)%_titan23_HashString_MOD, 0)

  def get(self, l: int, r: int) -> int:
    if self.used_seg:
      return self.hsb.get_mul(self.seg.prod(l, r), self.hsb.invb[self.n-r])
    return self.hsb.get_mul(self.hsb.get_mod(self.acc[r]-self.acc[l]), self.hsb.invb[self.n-r])

  def __getitem__(self, k: int) -> int:
    return self.get(k, k+1)

  def set(self, k: int, c: str) -> None:
    self.used_seg = True
    self.seg[k] = self.hsb.get_mul(self.hsb.powb[self.n-k-1], _titan23_HashString_DIC[c])

  def __setitem__(self, k: int, c: str) -> None:
    return self.set(k, c)

  def __len__(self):
    return self.n

  def get_lcp(self) -> List[int]:
    a = [0] * self.n
    memo = [-1] * (self.n+1)
    for i in range(self.n):
      ok, ng = 0, self.n-i+1
      while ng - ok > 1:
        mid = (ok + ng) >> 1
        if memo[mid] == -1:
          memo[mid] = self.get(0, mid)
        if memo[mid] == self.get(i, i+mid):
          ok = mid
        else:
          ng = mid
      a[i] = ok
    return a

