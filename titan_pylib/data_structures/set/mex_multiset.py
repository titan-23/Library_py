from titan_pylib.data_structures.segment_tree.segment_tree import SegmentTree
from typing import Iterable, List

class MexMultiset():
  """``MexMultiset`` です。

  各操作は `log` がつきますが、ANDセグ木の ``log`` で割と軽いです。
  """

  def __init__(self, u: int, a: Iterable[int]=[]) -> None:
    """``[0, u)`` の範囲の mex を計算する ``MexMultiset`` を構築します。

    時間・空間共に :math:`O(u)` です。

    Args:
      u (int): 値の上限です。
    """
    data = [0] * (u+1)
    init_data = [1] * (u+1)
    for e in a:
      if e <= u:
        data[e] += 1
        init_data[e] = 0
    self.u: int = u
    self.data: List[int] = data
    self.seg: SegmentTree[int] = SegmentTree(init_data, op=lambda s, t: s|t, e=0)

  def add(self, key: int) -> None:
    """``key`` を追加します。

    :math:`O(\\log{n})` です。
    """
    if key > self.u: return
    if self.data[key] == 0:
      self.seg[key] = 0
    self.data[key] += 1

  def remove(self, key: int) -> None:
    """``key`` を削除します。 ``key`` は存在していなければなりません。

    :math:`O(\\log{n})` です。
    """
    if key > self.u: return
    if self.data[key] == 1:
      self.seg[key] = 1
    self.data[key] -= 1

  def mex(self) -> int:
    """mex を返します。

    :math:`O(\\log{n})` です。
    """
    return self.seg.max_right(0, lambda lr: lr==0)

