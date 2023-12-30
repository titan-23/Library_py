from typing import Iterable, List, TypeVar, Generic
T = TypeVar('T')

class PartialPersistentArray(Generic[T]):
  """部分永続配列です。
  最新版の更新と、過去へのアクセスが可能です。
  """

  def __init__(self, a: Iterable[T]):
    """``a`` から部分永続配列を構築します。
    初期配列のバージョンは ``0`` です。

    :math:`O(n)` です。
    """
    self.a: List[List[T]] = [[e] for e in a]
    self.t: List[List[int]] = [[0] for _ in range(len(self.a))]
    self.last_time: int = 0

  def set(self, k: int, v: T, t: int) -> None:
    """位置 ``k`` を ``v`` に更新します。

    :math:`O(1)` です。

    Args:
      k (int): インデックスです。
      v (T): 更新する値です。
      t (int): 新たな配列のバージョンです。
    """
    assert t >= self.last_time
    assert t > self.t[k][-1]
    self.a[k].append(v)
    self.t[k].append(t)
    self.last_time = t

  def get(self, k: int, t: int=-1) -> T:
    """位置 ``k`` 、バージョン ``t`` の要素を返します。

    :math:`O(\\log{n})` です。

    Args:
      k (int): インデックスです。
      t (int, optional): バージョンです。デフォルトは最新バージョンです。
    """
    if t == -1 or t >= self.t[k][-1]:
      return self.a[k][-1]
    tk = self.t[k]
    ok, ng = 0, len(tk)
    while ng - ok > 1:
      mid = (ok + ng) // 2
      if tk[mid] <= t:
        ok = mid
      else:
        ng = mid
    return self.a[k][ok]

  def tolist(self, t: int) -> List[T]:
    """バージョン ``t`` の配列を返します。

    :math:`O(n\\log{n})` です。
    """
    return [self.get(i, t) for i in range(len(self))]

  def show(self, t: int) -> None:
    print(f'Time: {t}', end='')
    print([self.get(i, t) for i in range(len(self))])

  def show_all(self) -> None:
    """すべてのバージョンの配列を表示します。
    """
    for i in range(self.last_time):
      self.show(i)

  def __len__(self):
    return len(self.a)

