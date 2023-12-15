from typing import Union

class ModInt:

  mod = -1

  __slots__ = 'val'

  @classmethod
  def _inv(cls, a: int) -> int:
    res = 1
    b = cls.self.mod - 2
    while b:
      if b & 1:
        res = res * a % cls.mod
      a = a * a % cls.mod
      b >>= 1
    return res

  @classmethod
  def get_mod(cls) -> int:
    return cls.mod

  def __init__(self, val: int) -> None:
    self.val = val if 0 <= val < self.mod else val % self.mod

  def __add__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(self.val + int(other))

  def __sub__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(self.val - int(other))

  def __mul__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(self.val * int(other))

  def __pow__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(pow(self.val, int(other), self.mod))

  def __truediv__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(self.val * (self._inv(int(other))))

  # __iadd__ = __add__
  # __isub__ = __sub__
  # __imul__ = __mul__
  # __ipow__ = __pow__
  # __itruediv__ = __truediv__

  def __iadd__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    self.val += int(other)
    self.val %= self.mod
    return self

  def __isub__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    self.val -= int(other)
    self.val %= self.mod
    return self

  def __imul__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    self.val *= int(other)
    self.val %= self.mod
    return self

  def __ipow__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    self.val = pow(self.val, int(other), self.mod)
    return self

  def __itruediv__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    self.val *= self._inv(int(other))
    return self

  __radd__ = __add__
  __rmul__ = __mul__

  def __rsub__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(int(other) - self.val)

  def __rpow__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(pow(int(other), self.val, self.mod))

  def __rtruediv__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(int(other) * self._inv(self.val))

  def __eq__(self, other: Union[int, 'ModInt']) -> bool:
    return self.val == int(other)

  def __lt__(self, other: Union[int, 'ModInt']) -> bool:
    return self.val < int(other)

  def __le__(self, other: Union[int, 'ModInt']) -> bool:
    return self.val <= int(other)

  def __gt__(self, other: Union[int, 'ModInt']) -> bool:
    return self.val > int(other)

  def __ge__(self, other: Union[int, 'ModInt']) -> bool:
    return self.val >= int(other)

  def __ne__(self, other: Union[int, 'ModInt']) -> bool:
    return self.val != int(other)

  def __neg__(self) -> 'ModInt':
    return ModInt(-self.val)

  def __pos__(self) -> 'ModInt':
    return ModInt(self.val)

  def __int__(self) -> int:
    return self.val

  def __str__(self) -> str:
    return str(self.val)

  def __repr__(self):
    # return f'ModInt({self})'
    return f'{self}'

