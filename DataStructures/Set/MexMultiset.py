from typing import Iterable
from Library_py.DataStructures.SegmentTree.SegmentTree import SegmentTree

class MexMultiset():

  def __init__(self, u: int, a: Iterable[int]=[]) -> None:
    data = [0] * (u+1)
    init_data = [1] * (u+1)
    for e in a:
      if e <= u:
        data[e] += 1
        init_data[e] = 0
    self.u = u
    self.data = data
    self.seg = SegmentTree(init_data, lambda s, t: s|t, 0)

  def add(self, key: int) -> None:
    if key > self.u: return
    if self.data[key] == 0:
      self.seg[key] = 0
    self.data[key] += 1

  def remove(self, key: int) -> None:
    if key > self.u: return
    if self.data[key] == 1:
      self.seg[key] = 1
    self.data[key] -= 1

  def mex(self) -> int:
    return self.seg.max_right(0, lambda lr: lr==0)

