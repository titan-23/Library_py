from heapq import heapify, heappush, heappop
from collections import Counter

class kthMutiset():

  def __init__(self, k: int):
    self.lower = []
    self.upper = []
    self.lower_size = 0
    self.upper_size = 0
    self.k = k
    self.lower_del = Counter()
    self.upper_del = Counter()

  def add(self, key):
    if self.lower_del[key]:
      self.lower_del[key] -= 1
      return
    if self.upper_del[key]:
      self.upper_del[key] -= 1
      return
    if self.lower_size <= self.k:
      heappush(self.lower, -key)
      self.lower_size += 1
      return
    last = -self.lower[0]
    while self.lower_del[last]:
      self.lower_del[last] -= 1
      heappop(self.lower)
      last = -self.lower[0]
    if key > last:
      heappush(self.upper, key)
    else:
      heappop(self.lower)
      heappush(self.lower, -key)
      heappush(self.upper, last)
    self.upper_size += 1

  def remove(self, key):
    if self.lower_size <= self.k:
      self.lower_del[key] += 1
      self.lower_size -= 1
      return
    last = -self.lower[0]
    while self.lower_del[last]:
      self.lower_del[last] -= 1
      last = -self.lower[0]
    if key > last:
      self.upper_del[key] += 1
      self.upper_size -= 1
    else:
      up = heappop(self.upper)
      self.lower_del[key] += 1
      heappush(self.lower, -up)
    self.upper_size += 1

  def get(self):
    assert len(self) >= self.k
    last = -self.lower[0]
    while self.lower_del[last]:
      self.lower_del[last] -= 1
      heappop(self.lower)
      last = -self.lower[0]
    return last

  def fix(self):
    lower, upper = [], []
    for ele in self.lower:
      if self.lower_del[-ele]:
        self.lower_del[-ele] -= 1
      else:
        lower.append(ele)
    for ele in self.upper:
      if self.upper_del[ele]:
        self.upper_del[ele] -= 1
      else:
        upper.append(ele)
    self.lower_del = Counter()
    self.upper_del = Counter()
    heapify(lower)
    heapify(upper)
    self.lower = lower
    self.upper = upper

  def show(self):
    self.fix()
    print(sorted(-x for x in self.lower) + sorted(self.upper))

  def tolist(self):
    self.fix()
    return sorted(-x for x in self.lower) + sorted(self.upper)

  def __len__(self):
    return self.lower_size + self.upper_size

