from typing import List

class SetQuadraticDivision():

  def __init__(self, u: int, a: List[int]=[]):
    self.data = [0] * u
    self.size = int(u ** .5) + 1
    self.bucket_cnt = (u + self.size - 1) // self.size
    self.bucket_data = [0] * self.bucket_cnt
    for e in a:
      self.add(e)

  def add(self, key: int) -> bool:
    if self.data[key]:
      return False
    self.data[key] += 1
    self.bucket_data[key//self.size] += 1
    return True

  def discard(self, key: int, cnt) -> bool:
    if not self.data[key]:
      return False
    self.data[key] -= cnt
    self.bucket_data[key//self.size] -= cnt
    return True

  def remove(self, key: int, cnt: int=1) -> None:
    self.data[key] -= cnt
    self.bucket_data[key//self.size] -= cnt

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

