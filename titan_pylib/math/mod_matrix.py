from typing import List, Union, Final

_titan_pylib_ModMatrix_MOD: Final[int] = 998244353

class ModMatrix():

  @staticmethod
  def zeros(n: int, m: int) -> 'ModMatrix':
    return ModMatrix([[0]*m for _ in range(n)], _exter=False)

  @staticmethod
  def ones(n: int, m: int) -> 'ModMatrix':
    return ModMatrix([[1]*m for _ in range(n)], _exter=False)

  @staticmethod
  def identity(n: int) -> 'ModMatrix':
    a = [[0]*n for _ in range(n)]
    for i in range(n):
      a[i][i] = 1
    return ModMatrix(a, _exter=False)

  def __init__(self, a: List[List[int]], _exter=True) -> None:
    self.n: int = len(a)
    self.m: int = len(a[0]) if self.n > 0 else 0
    if _exter:
      for ai in a:
        for j in range(self.m):
          ai[j] %= _titan_pylib_ModMatrix_MOD
    self.a: List[List[int]] = a

  def det(self, inplace=False) -> int:
    # 上三角行列の行列式はその対角成分の総積であることを利用
    assert self.n == self.m
    a = self.a if inplace else [a[:] for a in self.a]
    flip = 0
    res = 1
    for i, ai in enumerate(a):
      if ai[i] == 0:
        for j in range(i+1, self.n):
          if a[j][i] != 0:
            a[i], a[j] = a[j], a[i]
            ai = a[i]
            flip ^= 1
            break
        else:
          return 0
      inv = pow(ai[i], -1, _titan_pylib_ModMatrix_MOD)
      for j in range(i+1, self.n):
        aj = a[j]
        freq = aj[i] * inv % _titan_pylib_ModMatrix_MOD
        for k in range(i+1, self.n):  # i+1スタートで十分
          aj[k] = (aj[k] - freq * ai[k]) % _titan_pylib_ModMatrix_MOD
      res *= ai[i]
      res %= _titan_pylib_ModMatrix_MOD
    if flip:
      res = -res % _titan_pylib_ModMatrix_MOD
    return res

  def inv(self, inplace=False) -> Union[None, 'ModMatrix']:
    # 掃き出し法の利用
    assert self.n == self.m
    a = self.a if inplace else [a[:] for a in self.a]
    r = [[0]*self.n for _ in range(self.n)]
    for i in range(self.n):
      r[i][i] = 1
    for i in range(self.n):
      ai = a[i]
      ri = r[i]
      if ai[i] == 0:
        for j in range(i+1, self.n):
          if a[j][i] != 0:
            a[i], a[j] = a[j], a[i]
            ai = a[i]
            r[i], r[j] = r[j], r[i]
            ri = r[i]
            break
        else:
          return None
      tmp = pow(ai[i], _titan_pylib_ModMatrix_MOD-2, _titan_pylib_ModMatrix_MOD)
      for j in range(self.n):
        ai[j] = ai[j] * tmp % _titan_pylib_ModMatrix_MOD
        ri[j] = ri[j] * tmp % _titan_pylib_ModMatrix_MOD
      for j in range(self.n):
        if i == j: continue
        aj = a[j]
        rj = r[j]
        aji = aj[i]
        for k in range(self.n):
          aj[k] = (aj[k] - ai[k] * aji) % _titan_pylib_ModMatrix_MOD
          rj[k] = (rj[k] - ri[k] * aji) % _titan_pylib_ModMatrix_MOD
    return ModMatrix(r, _exter=False)

  @classmethod
  def linear_equations(cls, A: 'ModMatrix', b: 'ModMatrix', inplace=False):
    # A_inv = A.inv(inplace=inplace)
    # res = A_inv @ b
    # return res
    pass

  def __add__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= _titan_pylib_ModMatrix_MOD
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        for j in range(self.m):
          val = resi[j] + other
          resi[j] = val if val < _titan_pylib_ModMatrix_MOD else val-_titan_pylib_ModMatrix_MOD
      return ModMatrix(res, _exter=False)
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        oi = other.a[i]
        for j in range(self.m):
          val = resi[j] + oi[j]
          resi[j] = val if val < _titan_pylib_ModMatrix_MOD else val-_titan_pylib_ModMatrix_MOD
      return ModMatrix(res, _exter=False)
    else:
      raise TypeError

  def __sub__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= _titan_pylib_ModMatrix_MOD
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        for j in range(self.m):
          val = resi[j] - other
          resi[j] = val+_titan_pylib_ModMatrix_MOD if val < 0 else val
      return ModMatrix(res, _exter=False)
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        oi = other.a[i]
        for j in range(self.m):
          val = resi[j] - oi[j]
          resi[j] = val+_titan_pylib_ModMatrix_MOD if val < 0 else val
      return ModMatrix(res, _exter=False)
    else:
      raise TypeError

  def __mul__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= _titan_pylib_ModMatrix_MOD
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        for j in range(self.m):
          resi[j] = resi[j] * other % _titan_pylib_ModMatrix_MOD
      return ModMatrix(res, _exter=False)
    if isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        oi = other.a[i]
        for j in range(self.m):
          resi[j] = resi[j] * oi[j] % _titan_pylib_ModMatrix_MOD
      return ModMatrix(res, _exter=False)
    raise TypeError

  def __matmul__(self, other: 'ModMatrix') -> 'ModMatrix':
    if isinstance(other, ModMatrix):
      assert self.m == other.n
      res = [[0]*other.m for _ in range(self.n)]
      for i in range(self.n):
        si = self.a[i]
        res_i = res[i]
        for k in range(self.m):
          ok = other.a[k]
          sik = si[k]
          for j in range(other.m):
            res_i[j] = (res_i[j] + ok[j] * sik) % _titan_pylib_ModMatrix_MOD
      return ModMatrix(res, _exter=False)
    raise TypeError

  def __pow__(self, n: int) -> 'ModMatrix':
    assert self.n == self.m
    res = ModMatrix.identity(self.n)
    a = ModMatrix([a[:] for a in self.a], _exter=False)
    while n > 0:
      if n & 1 == 1:
        res @= a
      a @= a
      n >>= 1
    return res

  __radd__ = __add__
  __rmul__ = __mul__

  def __rsub__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= _titan_pylib_ModMatrix_MOD
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        for j in range(self.m):
          val = other - resi[j]
          resi[j] = val+_titan_pylib_ModMatrix_MOD if val < 0 else val
      return ModMatrix(res, _exter=False)
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        oi = other.a[i]
        for j in range(self.m):
          val = oi[j] - resi[j]
          resi[j] = val+_titan_pylib_ModMatrix_MOD if val < 0 else val
      return ModMatrix(res, _exter=False)
    else:
      raise TypeError

  def __iadd__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= _titan_pylib_ModMatrix_MOD
      for i in range(self.n):
        si = self.a[i]
        for j in range(self.m):
          val = si[j] + other
          si[j] = val if val < _titan_pylib_ModMatrix_MOD else val-_titan_pylib_ModMatrix_MOD
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      for i in range(self.n):
        si = self.a[i]
        oi = other.a[i]
        for j in range(self.m):
          val = si[j] + oi[j]
          si[j] = val if val < _titan_pylib_ModMatrix_MOD else val-_titan_pylib_ModMatrix_MOD
    else:
      raise TypeError
    return self

  def __isub__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= _titan_pylib_ModMatrix_MOD
      for i in range(self.n):
        si = self.a[i]
        for j in range(self.m):
          val = si[j] - other
          si[j] = val+_titan_pylib_ModMatrix_MOD if val < 0 else val
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      for i in range(self.n):
        si = self.a[i]
        oi = other.a[i]
        for j in range(self.m):
          val = si[j] - oi[j]
          si[j] = val+_titan_pylib_ModMatrix_MOD if val < 0 else val
    else:
      raise TypeError
    return self

  def __imul__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= _titan_pylib_ModMatrix_MOD
      for i in range(self.n):
        si = self.a[i]
        for j in range(self.m):
          si[j] = si[j] * other % _titan_pylib_ModMatrix_MOD
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      for i in range(self.n):
        si = self.a[i]
        oi = other.a[i]
        for j in range(self.m):
          si[j] = si[j] * oi[j] % _titan_pylib_ModMatrix_MOD
    else:
      raise TypeError
    return self

  def __imatmul__(self, other: 'ModMatrix') -> 'ModMatrix':
    return self.__matmul__(other)

  def __ipow__(self, n: int) -> 'ModMatrix':
    assert self.n == self.m
    res = ModMatrix.identity(self.n)
    while n:
      if n & 1:
        res @= self
      self @= self
      n >>= 1
    return res

  def __ne__(self) -> 'ModMatrix':
    a = [a[:] for a in self.a]
    for i in range(self.n):
      for j in range(self.m):
        a[i][j] = (-a[i][j]) % _titan_pylib_ModMatrix_MOD
    return ModMatrix(a, _exter=False)

  def add(self, n: int, m: int, key: int) -> None:
    assert 0 <= n < self.n and 0 <= m < self.m
    self.a[n][m] = (self.a[n][m] + key) % _titan_pylib_ModMatrix_MOD

  def get(self, n: int, m: int) -> int:
    assert 0 <= n < self.n and 0 <= m < self.m
    return self.a[n][m]

  def get_n(self, n: int) -> List[int]:
    assert 0 <= n < self.n
    return self.a[n]

  def set(self, n: int, m: int, key: int) -> None:
    assert 0 <= n < self.n and 0 <= m < self.m
    self.a[n][m] = key % _titan_pylib_ModMatrix_MOD

  def tolist(self) -> List[List[int]]:
    return [a[:] for a in self.a]

  def show(self) -> None:
    for a in self.a:
      print(*a)
    print()

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.n:
      raise StopIteration
    self.__iter += 1
    return self.a[self.__iter-1]

  def __str__(self):
    return str(self.a)

