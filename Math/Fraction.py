from typing import Union
from math import gcd

class Fraction():

  def __init__(self, p: Union[int, str], q: int=1):
    if isinstance(p, int):
      if q < 0:
        p, q = -p, -q
    elif isinstance(p, str):
      if '.' not in p:
        p = int(p)
      else:
        p, q = map(int, p.split('.'))
    else:
      raise TypeError(f'{p=}, {q=}')
    g = gcd(p, q)
    self.n: int = p // g
    self.d: int = q // g

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

