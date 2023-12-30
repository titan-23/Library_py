# ref: https://qiita.com/keymoon/items/11fac5627672a6d6a9f6
from titan_pylib.data_structures.splay_tree.reversible_lazy_splay_tree_array import ReversibleLazySplayTreeData, ReversibleLazySplayTree
from typing import Optional, Dict, Final
import random
import string
_titan_pylib_DynamicHashString_MOD: Final[int] = (1 << 61) - 1
_titan_pylib_DynamicHashString_DIC: Final[Dict[str, int]] = {c: i for i, c in enumerate(string.ascii_lowercase, 1)}
_titan_pylib_DynamicHashString_MASK30: Final[int] = (1 << 30) - 1
_titan_pylib_DynamicHashString_MASK31: Final[int] = (1 << 31) - 1
_titan_pylib_DynamicHashString_MASK61: Final[int] = _titan_pylib_DynamicHashString_MOD

class DynamicHashStringBase():

  def __init__(self, n: int, base: int=-1, seed: Optional[int]=None) -> None:
    random.seed(seed)
    base = random.randint(37, 10**9) if base < 0 else base
    powb = [1] * (n+1)
    for i in range(1, n+1):
      powb[i] = self.get_mul(powb[i-1], base)
    op = lambda s, t: (self.unite(s[0], t[0], t[1]), s[1]+t[1])
    e = (0, 0)
    self.data = ReversibleLazySplayTreeData(op=op, e=e)
    self.n = n
    self.powb = powb

  @staticmethod
  def get_mul(a: int, b: int) -> int:
    au = a >> 31
    ad = a & _titan_pylib_DynamicHashString_MASK31
    bu = b >> 31
    bd = b & _titan_pylib_DynamicHashString_MASK31
    mid = ad * bu + au * bd
    midu = mid >> 30
    midd = mid & _titan_pylib_DynamicHashString_MASK30
    return DynamicHashStringBase.get_mod(au * bu * 2 + midu + (midd << 31) + ad * bd)

  @staticmethod
  def get_mod(x: int) -> int:
    # 商と余りを計算して足す->割る
    xu = x >> 61
    xd = x & _titan_pylib_DynamicHashString_MASK61
    res = xu + xd
    if res >= _titan_pylib_DynamicHashString_MOD:
      res -= _titan_pylib_DynamicHashString_MOD
    return res

  def unite(self, h1: int, h2: int, k: int) -> int:
    # h1, h2, k
    # len(h2) == k
    # h1 <- h2
    return self.get_mod(self.get_mul(h1, self.powb[k]) + h2)

class DynamicHashString():

  def __init__(self, hsb: DynamicHashStringBase, s: str) -> None:
    self.hsb = hsb
    self.splay = ReversibleLazySplayTree(hsb.data, ((_titan_pylib_DynamicHashString_DIC[c], 1) for c in s))

  def insert(self, k: int, c: str) -> None:
    self.splay.insert(k, (_titan_pylib_DynamicHashString_DIC[c], 1))

  def pop(self, k: int) -> int:
    return self.splay.pop(k)

  def reverse(self, l: int, r: int) -> None:
    self.splay.reverse(l, r)

  def get(self, l: int, r: int) -> int:
    return self.splay.prod(l, r)

  def __getitem__(self, k: int) -> int:
    return self.get(k, k+1)

  def set(self, k: int, c: str) -> None:
    self.splay[k] = (_titan_pylib_DynamicHashString_DIC[c], 1)

  def __setitem__(self, k: int, c: str) -> None:
    return self.set(k, c)

