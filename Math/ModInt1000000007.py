from typing import Union
_titan23_ModInt1000000007_MOD = 1000000007

class ModInt1000000007:

  __slots__ = 'val'

  @staticmethod
  def _inv(a: int) -> int:
    res = 1
    b = _titan23_ModInt1000000007_MOD - 2
    while b:
      if b & 1:
        res = res * a % _titan23_ModInt1000000007_MOD
      a = a * a % _titan23_ModInt1000000007_MOD
      b >>= 1
    return res

  @staticmethod
  def get_mod() -> int:
    return _titan23_ModInt1000000007_MOD

  def __init__(self, val: int) -> None:
    self.val = val if 0 <= val < _titan23_ModInt1000000007_MOD else val % _titan23_ModInt1000000007_MOD

  def __add__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(self.val + int(other))

  def __sub__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(self.val - int(other))

  def __mul__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(self.val * int(other))

  def __pow__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(pow(self.val, int(other), _titan23_ModInt1000000007_MOD))

  def __truediv__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(self.val * (self._inv(int(other))))

  # __iadd__ = __add__
  # __isub__ = __sub__
  # __imul__ = __mul__
  # __ipow__ = __pow__
  # __itruediv__ = __truediv__

  def __iadd__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    self.val += int(other)
    self.val %= _titan23_ModInt1000000007_MOD
    return self

  def __isub__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    self.val -= int(other)
    self.val %= _titan23_ModInt1000000007_MOD
    return self

  def __imul__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    self.val *= int(other)
    self.val %= _titan23_ModInt1000000007_MOD
    return self

  def __ipow__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    self.val = pow(self.val, int(other), _titan23_ModInt1000000007_MOD)
    return self

  def __itruediv__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    self.val *= self._inv(int(other))
    return self

  __radd__ = __add__
  __rmul__ = __mul__

  def __rsub__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(int(other) - self.val)

  def __rpow__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(pow(int(other), self.val, _titan23_ModInt1000000007_MOD))

  def __rtruediv__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(int(other) * self._inv(self.val))

  def __eq__(self, other: Union[int, 'ModInt1000000007']) -> bool:
    return self.val == int(other)

  def __lt__(self, other: Union[int, 'ModInt1000000007']) -> bool:
    return self.val < int(other)

  def __le__(self, other: Union[int, 'ModInt1000000007']) -> bool:
    return self.val <= int(other)

  def __gt__(self, other: Union[int, 'ModInt1000000007']) -> bool:
    return self.val > int(other)

  def __ge__(self, other: Union[int, 'ModInt1000000007']) -> bool:
    return self.val >= int(other)

  def __ne__(self, other: Union[int, 'ModInt1000000007']) -> bool:
    return self.val != int(other)

  def __neg__(self) -> 'ModInt1000000007':
    return ModInt1000000007(-self.val)

  def __pos__(self) -> 'ModInt1000000007':
    return ModInt1000000007(self.val)

  def __int__(self) -> int:
    return self.val

  def __str__(self) -> str:
    return str(self.val)

  def __repr__(self):
    # return f'ModInt1000000007({self})'
    return f'{self}'

