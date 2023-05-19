from typing import Union
from math import gcd

class Fraction():

  class _NAN():

    def __init__(self):
      pass

    def calc(self, other):
      return Fraction.NAN

    __add__ = calc
    __iadd__ = calc
    __radd__ = calc
    __sub__ = calc
    __isub__ = calc
    __rsub__ = calc
    __mul__ = calc
    __imul__ = calc
    __rmul__ = calc
    __pow__ = calc
    __ipow__ = calc
    __rpow__ = calc
    __div__ = calc
    __idiv__ = calc
    __rdiv__ = calc
    __floordiv__ = calc
    __ifloordiv__ = calc
    __rfloordiv__ = calc
    __truediv__ = calc
    __itruediv__ = calc
    __rtruediv__ = calc
    __pos__ = calc
    __neg__ = calc

    def __hash__(self):
      return hash(str(self))

    def __str__(self):
      return 'NAN'

    __repr__ = __str__

  NAN = _NAN()

  class _INF():

    def __init__(self):
      self.sgn = 1

    def __add__(self, other):
      if isinstance(other, Fraction._INF) or other == float('inf'):
        return Fraction.NAN
      return self

    def __sub__(self, other):
      if isinstance(other, Fraction._INF) or other == float('inf'):
        return Fraction.NAN
      return self

    def __mul__(self, other):
      res = Fraction._INF()
      if other < 0:
        res.sgn = 1 if res.sgn == -1 else 1
      return res

    def __truediv__(self, other):
      if isinstance(other, Fraction._INF) or other == float('inf'):
        return Fraction.NAN
      res = Fraction._INF()
      if other < 0:
        res *= -1
      return res

    def __rtruediv__(self, other):
      if isinstance(other, Fraction._INF) or other == float('inf'):
        return Fraction.NAN
      res = Fraction(0, 1)
      if other < 0:
        res *= -1
      return res

    __iadd__ = __add__
    __radd__ = __add__
    __imul__ = __mul__
    __rmul__ = __mul__
    __div__ = __truediv__
    __rdiv__ = __rtruediv__
    __floordiv__ = __truediv__
    __rfloordiv__ = __rtruediv__

    def __pow__(self, other):
      return Fraction._INF() * self.sgn

    def __gt__(self, other):
      if self.sgn == 1:
        return not isinstance(other, Fraction._INF) or other == float('INF')
      else:
        return (isinstance(other, Fraction._INF) or other == -float('INF'))

    def __le__(self, other):
      if self.sgn == 1:
        return isinstance(other, Fraction._INF) or other == float('INF')
      else:
        return not (isinstance(other, Fraction._INF) or other == -float('INF'))

    def __lt__(self, other):
      if self.sgn == 1:
        return isinstance(other, Fraction._INF) or other == float('INF')
      else:
        return not (isinstance(other, Fraction._INF) or other == -float('INF'))

    def __eq__(self, other):
      if self.sgn == 1:
        return isinstance(other, Fraction._INF) or other == float('INF')
      else:
        return not (isinstance(other, Fraction._INF) or other == -float('INF'))

    def __float__(self, other):
      return float('INF')

    def __abs__(self):
      return Fraction._INF()

    def __hash__(self):
      return hash(str(self))

    def __pos__(self):
      return Fraction._INF()

    def __neg__(self):
      res = Fraction._INF()
      res.sgn = -1
      return res

    def __str__(self):
      return 'INF' if self.sgn == 1 else '-INF'

    __repr__ = __str__

  def __init__(self, p: Union[int, str], q: int=1):
    if isinstance(p, int) and isinstance(q, int):
      if q < 0:
        p, q = -p, -q
    elif isinstance(p, str):
      if '.' not in p:
        if p == 'inf' or p == 'INF':
          p, q = 1, 0
        else:
          p = int(p)
      else:
          p, q = map(int, p.split('.'))
    elif isinstance(p, Fraction._INF) and isinstance(q, Fraction._INF):
        p, q = 1, 1
    elif isinstance(p, Fraction._INF):
      p, q = (-1 if p*q < 0 else 1), 0
    elif isinstance(q, Fraction._INF):
      p, q = 0, 1
    elif isinstance(p, Fraction._NAN):
      self.n = Fraction.NAN
      self.d = Fraction.NAN
      return
    else:
      raise TypeError(f'p={p}, q={q}')
    g = gcd(p, q) if q != 0 else -1
    self.n: int = p // g if g != -1 else ((1 if p > 0 else -1) * Fraction._INF())
    self.d: int = q // g if g != -1 else 1

  @staticmethod
  def _lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b

  def __add__(self, other):
    if not isinstance(other, Fraction): 
      other = Fraction(other)
    return Fraction(self.n*other.d+self.d*other.n, self.d*other.d)

  def __sub__(self, other):
    if not isinstance(other, Fraction): 
      other = Fraction(other)
    l = Fraction._lcm(self.d, other.d)
    return Fraction(self.n*l//self.d-other.n*l//other.d, l)

  def __mul__(self, other):
    if not isinstance(other, Fraction):
      other = Fraction(other)
    return Fraction(self.n*other.n, self.d*other.d)

  def __truediv__(self, other):
    if not isinstance(other, Fraction):
      other = Fraction(other)
    return Fraction(self.n*other.d, self.d*other.n)

  __iadd__ = __add__
  __isub__ = __sub__
  __imul__ = __mul__
  __itruediv__ = __truediv__
  __radd__ = __add__
  __rmul__ = __mul__

  def __rsub__(self, other):
    return -self + other

  def __rtruediv__(self, other):
    return other * Fraction(self.d, self.n)

  def __eq__(self, other: 'Fraction'):
    return self.n == other.n and self.d == other.d

  def __ne__(self, other: 'Fraction'):
    return self.n != other.n or self.d != other.d

  def __lt__(self, other: 'Fraction'):
    return self.n * other.d < self.d * other.n

  def __le__(self, other: 'Fraction'):
    return self.n * other.d <= self.d * other.n

  def __gt__(self, other: 'Fraction'):
    return self.n * other.d > self.d * other.n

  def __ge__(self, other: 'Fraction'):
    return self.n * other.d >= self.d * other.n

  def __pos__(self):
    return Fraction(self.n, self.d)

  def __neg__(self):
    return Fraction(-self.n, self.d)

  def __abs__(self):
    return Fraction((self.n if self.n >= 0 else -self.n), self.d)

  def __int__(self):
    return self.n // self.d

  def __float__(self):
    return self.n / self.d

  def __bool__(self):
    return self.n != 0

  def __hash__(self):
    return hash(str(self))

  def __str__(self):
    return f'({self.n}/{self.d})'

  def __repr__(self):
    # return f'Fraction({self.n}, {self.d})'
    return str(self)

