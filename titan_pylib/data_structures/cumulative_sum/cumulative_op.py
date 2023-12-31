from typing import Generic, TypeVar, Callable, Iterable
T = TypeVar('T')

class CumulativeOp(Generic[T]):
  """抽象化累積和です。
  """

  def __init__(self, a: Iterable[T], op: Callable[[T, T], T], inv: Callable[[T], T], e: T):
    """
    :math:`O(n)` です。

    Args:
      a (Iterable[T]): ``CumulativeOp`` を構築する配列です。
      op (Callable[[T, T], T]): 2項演算をする関数です。
      inv (Callable[[T], T]): 逆元を返す関数です。 ``prod`` メソッドを使用する場合必要です。
      e (T): 単位元です。
    """
    a = list(a)
    n = len(a)
    acc = [e for _ in range(n+1)]
    for i in range(n):
      acc[i+1] = op(acc[i], [i])
    self.n = n
    self.acc = acc
    self.a = a
    self.op = op
    self.inv = inv

  def pref(self, r: int) -> T:
    """区間 ``[0, r)`` の演算結果を返します。

    :math:`O(1)` です。

    Args:
      r (int): インデックスです。
    """
    return self.acc[r]

  def prod(self, l: int, r: int) -> T:
    """区間 `[l, r)` の演算結果を返します。

    :math:`O(1)` です。

    Args:
      l (int): インデックスです。
      r (int): インデックスです。
    """
    assert 0 <= l <= r <= self.n, f'IndexError: {self.__class__.__name__}.prod({l}, {r})'
    return self.op(self.acc[r], self.inv(self.acc[l]))

  def all_prod(self) -> T:
    """区間 `[0, N)` の演算結果を返します。

    :math:`O(1)` です。
    """
    return self.acc[-1]

  def __getitem__(self, k: int) -> T:
    return self.a[k]

  def __len__(self):
    return len(self.a)

  def __str__(self):
    return str(self.acc)

  __repr__ = __str__

