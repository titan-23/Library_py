from typing import List, Union

class ModMatrix:

  # mod = 1000000007
  mod = 998244353

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
          ai[j] %= ModMatrix.mod
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
      inv = pow(ai[i], ModMatrix.mod-2, ModMatrix.mod)
      for j in range(i+1, self.n):
        aj = a[j]
        freq = aj[i] * inv % ModMatrix.mod
        for k in range(i+1, self.n):  # i+1スタートで十分
          aj[k] = (aj[k] - freq * ai[k]) % ModMatrix.mod
      res *= ai[i]
      res %= ModMatrix.mod
    if flip:
      res = -res % ModMatrix.mod
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
      tmp = pow(ai[i], ModMatrix.mod-2, ModMatrix.mod)
      for j in range(self.n):
        ai[j] = ai[j] * tmp % ModMatrix.mod
        ri[j] = ri[j] * tmp % ModMatrix.mod
      for j in range(self.n):
        if i == j: continue
        aj = a[j]
        rj = r[j]
        aji = aj[i]
        for k in range(self.n):
          aj[k] = (aj[k] - ai[k] * aji) % ModMatrix.mod
          rj[k] = (rj[k] - ri[k] * aji) % ModMatrix.mod
    return ModMatrix(r, _exter=False)

  @classmethod
  def linear_equations(cls, A: 'ModMatrix', b: 'ModMatrix', inplace=False):
    # A_inv = A.inv(inplace=inplace)
    # res = A_inv @ b
    # return res
    pass

  def __add__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= ModMatrix.mod
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        for j in range(self.m):
          val = resi[j] + other
          resi[j] = val if val < ModMatrix.mod else val-ModMatrix.mod
      return ModMatrix(res, _exter=False)
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        oi = other.a[i]
        for j in range(self.m):
          val = resi[j] + oi[j]
          resi[j] = val if val < ModMatrix.mod else val-ModMatrix.mod
      return ModMatrix(res, _exter=False)
    else:
      raise TypeError

  def __sub__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= ModMatrix.mod
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        for j in range(self.m):
          val = resi[j] - other
          resi[j] = val+ModMatrix.mod if val < 0 else val
      return ModMatrix(res, _exter=False)
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        oi = other.a[i]
        for j in range(self.m):
          val = resi[j] - oi[j]
          resi[j] = val+ModMatrix.mod if val < 0 else val
      return ModMatrix(res, _exter=False)
    else:
      raise TypeError

  def __mul__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= ModMatrix.mod
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        for j in range(self.m):
          resi[j] = resi[j] * other % ModMatrix.mod
      return ModMatrix(res, _exter=False)
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        oi = other.a[i]
        for j in range(self.m):
          resi[j] = resi[j] * oi[j] % ModMatrix.mod
      return ModMatrix(res, _exter=False)
    else:
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
            res_i[j] = (res_i[j] + ok[j] * sik) % ModMatrix.mod
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

  def __radd__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    return self.__add__(other)

  def __rsub__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= ModMatrix.mod
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        for j in range(self.m):
          val = other - resi[j]
          resi[j] = val+ModMatrix.mod if val < 0 else val
      return ModMatrix(res, _exter=False)
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      res = [a[:] for a in self.a]
      for i in range(self.n):
        resi = res[i]
        oi = other.a[i]
        for j in range(self.m):
          val = oi[j] - resi[j]
          resi[j] = val+ModMatrix.mod if val < 0 else val
      return ModMatrix(res, _exter=False)
    else:
      raise TypeError

  def __rmul__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    return self.__mul__(other)

  def __iadd__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= ModMatrix.mod
      for i in range(self.n):
        si = self.a[i]
        for j in range(self.m):
          val = si[j] + other
          si[j] = val if val < ModMatrix.mod else val-ModMatrix.mod
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      for i in range(self.n):
        si = self.a[i]
        oi = other.a[i]
        for j in range(self.m):
          val = si[j] + oi[j]
          si[j] = val if val < ModMatrix.mod else val-ModMatrix.mod
    else:
      raise TypeError
    return self
  
  def __isub__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= ModMatrix.mod
      for i in range(self.n):
        si = self.a[i]
        for j in range(self.m):
          val = si[j] - other
          si[j] = val+ModMatrix.mod if val < 0 else val
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      for i in range(self.n):
        si = self.a[i]
        oi = other.a[i]
        for j in range(self.m):
          val = si[j] - oi[j]
          si[j] = val+ModMatrix.mod if val < 0 else val
    else:
      raise TypeError
    return self

  def __imul__(self, other: Union[int, 'ModMatrix']) -> 'ModMatrix':
    if isinstance(other, int):
      other %= ModMatrix.mod
      for i in range(self.n):
        si = self.a[i]
        for j in range(self.m):
          si[j] = si[j] * other % ModMatrix.mod
    elif isinstance(other, ModMatrix):
      assert self.n == other.n and self.m == other.m
      for i in range(self.n):
        si = self.a[i]
        oi = other.a[i]
        for j in range(self.m):
          si[j] = si[j] * oi[j] % ModMatrix.mod
    else:
      raise TypeError
    return self

  def __imatmul__(self, other: 'ModMatrix') -> 'ModMatrix':
    return self.__matmul__(other)

  def __ipow__(self, n: int) -> 'ModMatrix':
    assert self.n == self.m
    res = ModMatrix.identity(self.n)
    while n > 0:
      if n & 1 == 1:
        res @= self
      self @= self
      n >>= 1
    return res

  def get(self, n, m):
    assert 0 <= n < self.n and 0 <= m < self.m
    return self.a[n][m]

  def get_n(self, n):
    assert 0 <= n < self.n
    return self.a[n]

  def set(self, n, m, key):
    assert 0 <= n < self.n and 0 <= m < self.m
    self.a[n][m] = key % ModMatrix.mod

  def tolist(self):
    return [a[:] for a in self.a]

  def show(self):
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

