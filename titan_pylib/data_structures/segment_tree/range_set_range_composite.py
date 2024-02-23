from titan_pylib.data_structures.segment_tree.segment_tree import SegmentTree
from titan_pylib.data_structures.set.wordsize_tree_set import WordsizeTreeSet
from typing import Union, Callable, TypeVar, Generic, Iterable
T = TypeVar('T')

class RangeSetRangeComposite(Generic[T]):

  def __init__(self,
               n_or_a: Union[int, Iterable[T]],
               op: Callable[[T, T], T],
               pow_: Callable[[T, int], T],
               e: T,
               id: T
               ) -> None:
    self.op = op
    self.pow = pow_
    self.e = e
    self.id = id
    a = [e] * n_or_a if isinstance(n_or_a, int) else list(n_or_a)
    a.append(e)
    self.seg = SegmentTree(a, op, e)
    self.n = len(self.seg)
    self.indx = WordsizeTreeSet(self.n+1, range(self.n+1))
    self.val = a
    self.beki = [1] * self.n

  def prod(self, l: int, r: int) -> T:
    ll = self.indx.ge(l)
    rr = self.indx.le(r)
    ans = self.e
    if ll != l:
      l0 = self.indx.le(l)
      beki = self.beki[l0] - (l-l0) if l0+self.beki[l0] <= r else r - l
      ans = self.pow(self.val[l0], beki)
    if ll < rr:
      ans = self.op(ans, self.seg.prod(ll, rr))
    if rr != r and l <= rr:
      ans = self.op(ans, self.pow(self.val[rr], r - rr))
    return ans

  def apply(self, l: int, r: int, f: T) -> None:
    indx, val, beki, seg = self.indx, self.val, self.beki, self.seg

    l0 = indx.le(l)
    r0 = indx.le(r)
    if l != l0:
      seg[l0] = self.pow(val[l0], l - l0)
    if r != r0:
      beki[r] = beki[r0] - (r - r0)
      indx.add(r)
      val[r] = val[r0]
      seg[r] = self.pow(val[r], beki[r])
    if l != l0:
      beki[l0] = l - l0

    i = indx.gt(l)
    while i < r:
      seg[i] = self.e
      indx.discard(i)
      i = indx.gt(i)
    val[l] = f
    indx.add(l)
    beki[l] = r - l
    seg[l] = self.pow(f, beki[l])
