from typing import Iterable

class MexMultiset():

  # MEX差分計算クラス
  # - add(x: int) xを追加する / O(logN)
  # - discard(x: int) xを削除する / O(logN)
  # - contains(x) 存在判定 / O(logN) この機能いる？？
  # - count(x) xの要素数を取得 / O(logN)この機能いる2？？
  # - mex() mexを取得する / O(logN)
  # 
  # predecessor problemを高速(O(logN))に解けるデータ構造が必要

  def __init__(self, a: Iterable[int]=[]):
    self.data = SplayTreeSetTopDown()
    self.dic = {}
    for a_ in sorted(a):
      self.add(a_)

  def add(self, x: int) -> None:
    if x in self.dic:
      self.dic[x] += 1
      return
    self.dic[x] = 1
    if x < 0: return
    t = self.data.ge((x-1, 2))
    if t is not None and t[0] == x-1:
      self.data.discard(t)
      t = self.data.gt(t)
    else:
      self.data.add((x, 1))
    if t is not None and t[0] == x+1:
      self.data.discard(t)
    else:
      self.data.add((x, 2))

  def discard(self, x: int) -> None:
    if x not in self.dic: return
    if self.dic[x] > 1:
      self.dic[x] -= 1
      return
    del self.dic[x]
    if x < 0: return
    t = self.data.lt((x, 2))
    if t[0] == x:
      self.data.discard(t)
    else:
      self.data.add((x-1, 2))
    t = self.data.ge((x, 2))
    if t[0] == x:
      self.data.discard(t)
    else:
      self.data.add((x+1, 1))

  def mex(self) -> int:
    t = self.data.ge((0, -1))
    if t is None or t[0] != 0:
      return 0
    else:
      t = self.data.gt(t)
      return t[0] + 1

  def count(self, x: int) -> int:
    if x in self.dic:
      return self.dic[x]
    return 0

  def __contains__(self, x: int):
    return x in self.dic
  
  def __str__(self):
    return '{' + ', '.join(map(str, sorted(k for k, v in self.dic.items() for _ in range(v)))) + '}'

