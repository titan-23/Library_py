# from Library_py.DataStructures.Set.MultisetQuadraticDivision import MultisetQuadraticDivision
from typing import List

class MultisetQuadraticDivision():

  # OrderedMultiset[int]
  # Space Complexity : O(u)
  # add / discard / remove / contains : O(1)
  # kth_elm : O(√u)

  def __init__(self, u: int, a: List[int]=[]):
    self.data = [0] * u
    self.size = int(u ** .5) + 1
    self.bucket_cnt = (u + self.size - 1) // self.size
    self.bucket_data = [0] * self.bucket_cnt
    self._len = 0
    for e in a:
      self.add(e)

  def add(self, key: int, cnt: int=1) -> None:
    self._len += cnt
    self.data[key] += cnt
    self.bucket_data[key//self.size] += cnt

  def discard(self, key: int, cnt: int=1) -> None:
    cnt = min(cnt, self.data[key])
    self._len -= cnt
    self.data[key] -= cnt
    self.bucket_data[key//self.size] -= cnt

  def remove(self, key: int, cnt: int=1) -> None:
    self.data[key] -= cnt
    self.bucket_data[key//self.size] -= cnt

  def count(self, key: int) -> int:
    return self.data[key]

  def __contains__(self, key: int):
    return self.data[key] != 0

  def __getitem__(self, k: int) -> int:
    indx = 0
    data, bucket_data = self.data, self.bucket_data
    while bucket_data[indx] < k:
      k -= bucket_data[indx]
      indx += 1
    indx *= self.size
    while data[indx] == 0 or data[indx] <= k:
      k -= data[indx]
      indx += 1
    return indx

  def __len__(self):
    return self._len


