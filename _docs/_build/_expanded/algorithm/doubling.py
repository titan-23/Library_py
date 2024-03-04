# from titan_pylib.algorithm.doubling import Doubling
from typing import Callable, TypeVar, Generic
T = TypeVar('T')

class Doubling(Generic[T]):
  """ダブリングテーブルを構築します。
  :math:`O(n\\log{lim})` です。

  Args:
    Generic (T): 状態の型です。
    n (int): テーブルサイズです。
    lim (int): クエリの最大数です。
    move_to (Callable[[T], T]): 遷移関数です。 ``u`` から ``v`` へ遷移します。
  """

  def __init__(self, n: int, lim: int, move_to: Callable[[T], T]) -> None:
    self.move_to = move_to
    self.n = n
    self.lim = lim
    self.log = lim.bit_length()
    db = [[0]*self.n for _ in range(self.log+1)]
    for i in range(self.n):
      db[0][i] = move_to(i)
    for k in range(self.log):
      for i in range(self.n):
        db[k+1][i] = db[k][db[k][i]]
    self.db = db

  def kth(self, start: T, k: int) -> T:
    """``start`` から ``k`` 個進んだ状態を返します。
    :math:`O(\\log{k})` です。

    Args:
      start (T): スタートの状態です。
      k (int): 遷移関数を適用する回数です。
    """
    now = start
    for i in range(self.log):
      if k & 1:
        now = self.db[i][now]
      k >>= 1
    return now

