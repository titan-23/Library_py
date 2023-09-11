from Library_py.DataStructures.FenwickTree.FenwickTree import FenwickTree

class StringCount():

  alp = 'abcdefghijklmnopqrstuvwxyz'
  # alp = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  DIC = {c: i for i, c in enumerate(alp)}

  def __init__(self, s: str):
    assert isinstance(s, str)
    self.n = len(s)
    self.s = list(s)
    self.data = [FenwickTree(self.n) for _ in range(26)]
    for i, c in enumerate(s):
      self.data[StringCount.DIC[c]].add(i, 1)

  # 区間[l, r)が昇順かどうか判定する
  def is_ascending(self, l: int, r: int) -> bool:
    # assert 0 <= l <= r <= self.n
    end = l
    for i in range(26):
      c = self.data[i].sum(l, r)
      end += c
      if end > r or self.data[i].sum(l, end) != c:
        return False
    return True

  # 区間[l, r)が降順かどうか判定する
  # 未確認
  def is_descending(self, l: int, r: int) -> bool:
    # assert 0 <= l <= r <= self.n
    start = r - 1
    for i in range(25, -1, -1):
      c = self.data[i].sum(l, r)
      start -= c
      if start < l or self.data[i].sum(start, r) != c:
        return False
    return True

  # 区間[l, r)の最小の文字を返す
  def get_min(self, l, r):
    for i in range(26):
      if self.data[i].sum(l, r):
        return StringCount.alp[i]

  # 区間[l, r)の最大の文字を返す
  def get_max(self, l, r):
    for i in range(25, -1, -1):
      if self.data[i].sum(l, r):
        return StringCount.alp[i]

  # k番目の文字をcに変更する
  def __setitem__(self, k: int, c: str):
    # assert 0 <= k < self.n
    self.data[StringCount.DIC[self.s[k]]].add(k, -1)
    self.s[k] = c
    self.data[StringCount.DIC[c]].add(k, 1)

  # 区間[l, r)の全ての文字の個数を返す
  # 返り値は要素数26のList[int]
  def get_all_count(self, l: int, r: int):
    return [self.data[i].sum(l, r) for i in range(26)]

  # 区間[l, r)のcの個数を返す
  def get_count(self, l: int, r: int, c: str):
    return self.data[StringCount.DIC[c]].sum(l, r)

  def __getitem__(self, item):
    if isinstance(item, int):
      return self.s[item]
    elif isinstance(item, slice):
      return ''.join(self.s[item])
    raise TypeError

  def __str__(self):
    return ''.join(self.s)

