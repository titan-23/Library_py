from typing import Union
from functools import lru_cache

class ModInt998244353:

  __slots__ = ['val']

  @staticmethod
  @lru_cache(maxsize=None)
  def _inv(a: int) -> int:
    res = 1
    b = 998244351
    while b:
      if b & 1:
        res = res * a % 998244353
      a = a * a % 998244353
      b >>= 1
    return res

  def __init__(self, val: int) -> None:
    self.val = val if 0 <= val and val < 998244353 else val % 998244353

  def __add__(self, other: Union[int, 'ModInt998244353']) -> 'ModInt998244353':
    return ModInt998244353(self.val + (other if isinstance(other, int) else other.val))

  def __sub__(self, other: Union[int, 'ModInt998244353']) -> 'ModInt998244353':
    return ModInt998244353(self.val - (other if isinstance(other, int) else other.val))

  def __mul__(self, other: Union[int, 'ModInt998244353']) -> 'ModInt998244353':
    return ModInt998244353(self.val * (other if isinstance(other, int) else other.val))

  def __pow__(self, other: Union[int, 'ModInt998244353']) -> 'ModInt998244353':
    return ModInt998244353(pow(self.val, (other if isinstance(other, int) else other.val), 998244353))

  def __truediv__(self, other: Union[int, 'ModInt998244353']) -> 'ModInt998244353':
    return ModInt998244353(self.val * (self._inv(other) if isinstance(other, int) else self._inv(other.val)))

  __iadd__ = __add__
  __isub__ = __sub__
  __imul__ = __mul__
  __ipow__ = __pow__
  __itruediv__ = __truediv__

  def __radd__(self, other: Union[int, 'ModInt998244353']) -> 'ModInt998244353':
    return ModInt998244353((other if isinstance(other, int) else other.val) + self.val)

  def __rsub__(self, other: Union[int, 'ModInt998244353']) -> 'ModInt998244353':
    return ModInt998244353((other if isinstance(other, int) else other.val) - self.val)

  def __rmul__(self, other: Union[int, 'ModInt998244353']) -> 'ModInt998244353':
    return ModInt998244353((other if isinstance(other, int) else other.val) * self.val)

  def __rpow__(self, other: Union[int, 'ModInt998244353']) -> 'ModInt998244353':
    return ModInt998244353(pow((other if isinstance(other, int) else other.val), self.val, 998244353))

  def __rtruediv__(self, other: Union[int, 'ModInt998244353']) -> 'ModInt998244353':
    return ModInt998244353((other if isinstance(other, int) else other.val) * self._inv(self.val))

  def __eq__(self, other: Union[int, 'ModInt998244353']):
    return self.val == int(other)

  def __lt__(self, other: Union[int, 'ModInt998244353']):
    return self.val < int(other)

  def __le__(self, other: Union[int, 'ModInt998244353']):
    return self.val <= int(other)

  def __gt__(self, other: Union[int, 'ModInt998244353']):
    return self.val > int(other)

  def __ge__(self, other: Union[int, 'ModInt998244353']):
    return self.val >= int(other)

  def __ne__(self, other: Union[int, 'ModInt998244353']):
    return self.val != int(other)

  def __neg__(self):
    return ModInt998244353(998244353 - self.val)

  def __pos__(self):
    return ModInt998244353(self.val)

  def __int__(self):
    return self.val

  def __str__(self):
    return str(self.val)

  def __repr__(self):
    # return f'ModInt998244353({self})'
    return f'{self}'
mint = ModInt998244353


from typing import Union
from functools import lru_cache

class ModInt1000000007:

  __slots__ = ['val']

  @staticmethod
  @lru_cache(maxsize=None)
  def _inv(a: int) -> int:
    res = 1
    b = 1000000005
    while b:
      if b & 1:
        res = res * a % 1000000007
      a = a * a % 1000000007
      b >>= 1
    return res

  def __init__(self, val: int) -> None:
    self.val = val if 0 <= val and val < 1000000007 else val % 1000000007

  def __add__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(self.val + (other if isinstance(other, int) else other.val))

  def __sub__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(self.val - (other if isinstance(other, int) else other.val))

  def __mul__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(self.val * (other if isinstance(other, int) else other.val))

  def __pow__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(pow(self.val, (other if isinstance(other, int) else other.val), 1000000007))

  def __truediv__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(self.val * (self._inv(other) if isinstance(other, int) else self._inv(other.val)))

  __iadd__ = __add__
  __isub__ = __sub__
  __imul__ = __mul__
  __ipow__ = __pow__
  __itruediv__ = __truediv__

  def __radd__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007((other if isinstance(other, int) else other.val) + self.val)

  def __rsub__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007((other if isinstance(other, int) else other.val) - self.val)

  def __rmul__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007((other if isinstance(other, int) else other.val) * self.val)

  def __rpow__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007(pow((other if isinstance(other, int) else other.val), self.val, 998244353))

  def __rtruediv__(self, other: Union[int, 'ModInt1000000007']) -> 'ModInt1000000007':
    return ModInt1000000007((other if isinstance(other, int) else other.val) * self._inv(self.val))

  def __eq__(self, other: Union[int, 'ModInt1000000007']):
    return self.val == int(other)

  def __lt__(self, other: Union[int, 'ModInt1000000007']):
    return self.val < int(other)

  def __le__(self, other: Union[int, 'ModInt1000000007']):
    return self.val <= int(other)

  def __gt__(self, other: Union[int, 'ModInt1000000007']):
    return self.val > int(other)

  def __ge__(self, other: Union[int, 'ModInt1000000007']):
    return self.val >= int(other)

  def __ne__(self, other: Union[int, 'ModInt1000000007']):
    return self.val != int(other)

  def __neg__(self):
    return ModInt1000000007(1000000007 - self.val)

  def __pos__(self):
    return ModInt1000000007(self.val)

  def __int__(self):
    return self.val

  def __str__(self):
    return str(self.val)

  def __repr__(self):
    # return f'ModInt1000000007({self})'
    return f'{self}'
mint = ModInt1000000007


from typing import Union
from functools import lru_cache

class ModInt:

  __slots__ = ['val']

  mod = 1

  @classmethod
  def set_mod(cls, mod: int) -> None:
    cls.mod = mod

  @classmethod
  @lru_cache(maxsize=None)
  def _inv(cls, a: int) -> int:
    res = 1
    b = cls.mod - 2
    while b:
      if b & 1:
        res = res * a % cls.mod
      a = a * a % cls.mod
      b >>= 1
    return res

  def __init__(self, val: int) -> None:
    self.val = val if 0 <= val and val < ModInt.mod else val % ModInt.mod

  def __add__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(self.val + (other if isinstance(other, int) else other.val))

  def __sub__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(self.val - (other if isinstance(other, int) else other.val))

  def __mul__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(self.val * (other if isinstance(other, int) else other.val))

  def __pow__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(pow(self.val, (other if isinstance(other, int) else other.val), ModInt.mod))

  def __truediv__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(self.val * (self._inv(other) if isinstance(other, int) else self._inv(other.val)))

  __iadd__ = __add__
  __isub__ = __sub__
  __imul__ = __mul__
  __ipow__ = __pow__
  __itruediv__ = __truediv__

  def __radd__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt((other if isinstance(other, int) else other.val) + self.val)

  def __rsub__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt((other if isinstance(other, int) else other.val) - self.val)

  def __rmul__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt((other if isinstance(other, int) else other.val) * self.val)

  def __rpow__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt(pow((other if isinstance(other, int) else other.val), self.val, ModInt.mod))

  def __rtruediv__(self, other: Union[int, 'ModInt']) -> 'ModInt':
    return ModInt((other if isinstance(other, int) else other.val) * self._inv(self.val))

  def __eq__(self, other: Union[int, 'ModInt']):
    return self.val == int(other)

  def __lt__(self, other: Union[int, 'ModInt']):
    return self.val < int(other)

  def __le__(self, other: Union[int, 'ModInt']):
    return self.val <= int(other)

  def __gt__(self, other: Union[int, 'ModInt']):
    return self.val > int(other)

  def __ge__(self, other: Union[int, 'ModInt']):
    return self.val >= int(other)

  def __ne__(self, other: Union[int, 'ModInt']):
    return self.val != int(other)

  def __neg__(self):
    return ModInt(ModInt.mod - self.val)

  def __pos__(self):
    return ModInt(self.val)

  def __int__(self):
    return self.val

  def __str__(self):
    return str(self.val)

  def __repr__(self):
    # return f'ModInt({self})'
    return f'{self}'
mint = ModInt

