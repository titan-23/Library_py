from Library_py.String.HashString import HashStringBase, HashString
from typing import Optional, Tuple, List
import random

class MultiHashStringBase():

  def __init__(self, n: int, base_cnt: int=1, base_list: List[int]=[], seed: Optional[int]=None) -> None:
    if seed is None:
      seed = random.randint(0, 10**9)
    assert base_cnt > 0, f'ValueError: MultiHashString base_cnt must be > 0'
    base_list = base_list if len(base_list) == base_cnt else [random.randint(37, 10**9) for _ in range(base_cnt)]
    hsb = tuple(HashStringBase(n, base_list[i]) for i in range(base_cnt))
    self.hsb = hsb

class MultiHashString():
  
  def __init__(self, hsb: MultiHashStringBase, s: str, update: bool=False) -> None:
    self.hsb = hsb
    self.hs = tuple(HashString(hsb, s, update=update) for hsb in self.hsb.hsb)

  def get(self, l: int, r: int) -> Tuple[int]:
    return tuple(hs.get(l, r) for hs in self.hs)

  def __getitem__(self, k: int) -> Tuple[int]:
    return self.get(k, k+1)

  def set(self, k: int, c: str) -> None:
    for hs in self.hs:
      hs.set(k, c)

  def __setitem__(self, k: int, c: str) -> None:
    self.set(k, c)

