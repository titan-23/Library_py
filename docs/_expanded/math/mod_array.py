# from titan_pylib.math.mod_array import ModArray
from typing import Iterable, Union, List
from functools import reduce, lru_cache

class ModArray998244353():

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

  def __init__(self, n_or_a: Union[int, Iterable[int]], e: int=0):
    e %= 998244353
    self.a: List[int] = [e] * n_or_a if isinstance(n_or_a, int) else [e % 998244353 for e in n_or_a]

  def resize(self, size: int, e: int=0):
    e %= 998244353
    self.a = [e] * size

  def append(self, v: int) -> None:
    self.a.append(v % 998244353)

  def pop(self, k: int=-1) -> int:
    return self.a.pop(k)

  def all_sum(self) -> int:
    return sum(self.a) % 998244353

  def all_mul(self) -> int:
    return reduce(lambda x, y: x * y % 998244353, self.a)

  def add(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] + v) % 998244353

  def sub(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] - v) % 998244353

  def mul(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] * v) % 998244353

  def div(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] * self._inv(v)) % 998244353

  def get_mod(self) -> int:
    return 998244353

  def __iter__(self):
    self._iter = 0
    return self

  def __next__(self):
    if self._iter >= len(self.a):
      raise StopIteration
    self._iter += 1
    return self.a[self._iter-1]

  def __getitem__(self, k: Union[int, slice]) -> Union[int, 'ModArray998244353']:
    return ModArray998244353(self.a[k]) if isinstance(k, slice) else self.a[k]

  def __setitem__(self, k: int, v: int) -> None:
    assert isinstance(v, int)
    self.a[k] = v % 998244353

  def __str__(self):
    return str(self.a)

  def __len__(self):
    return len(self.a)

Array = ModArray998244353

# ---------------------- #

from typing import Iterable, Union, List
from functools import reduce, lru_cache

class ModArray1000000007():

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

  def __init__(self, n_or_a: Union[int, Iterable[int]], e: int=0):
    e %= 1000000007
    self.a: List[int] = [e] * n_or_a if isinstance(n_or_a, int) else [e % 1000000007 for e in n_or_a]

  def resize(self, size: int, e: int=0):
    e %= 1000000007
    self.a = [e] * size

  def append(self, v: int) -> None:
    self.a.append(v % 1000000007)

  def pop(self, k: int=-1) -> int:
    return self.a.pop(k)

  def all_sum(self) -> int:
    return sum(self.a) % 1000000007

  def all_mul(self) -> int:
    return reduce(lambda x, y: x * y % 1000000007, self.a)

  def add(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] + v) % 1000000007

  def sub(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] - v) % 1000000007

  def mul(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] * v) % 1000000007

  def div(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] * self._inv(v)) % 1000000007

  def get_mod(self) -> int:
    return 1000000007

  def __iter__(self):
    self._iter = 0
    return self

  def __next__(self):
    if self._iter >= len(self.a):
      raise StopIteration
    self._iter += 1
    return self.a[self._iter-1]

  def __getitem__(self, k: Union[int, slice]) -> Union[int, 'ModArray1000000007']:
    return ModArray1000000007(self.a[k]) if isinstance(k, slice) else self.a[k]

  def __setitem__(self, k: int, v: int) -> None:
    assert isinstance(v, int)
    self.a[k] = v % 1000000007

  def __str__(self):
    return str(self.a)

  def __len__(self):
    return len(self.a)

Array = ModArray1000000007

# ---------------------- #

from typing import Iterable, Union, List
from functools import reduce, lru_cache

class ModArray():

  @lru_cache(maxsize=None)
  def _inv(self, a: int) -> int:
    res = 1
    b = self.mod - 2
    while b:
      if b & 1:
        res = res * a % self.mod
      a = a * a % self.mod
      b >>= 1
    return res

  def __init__(self, mod: int, n_or_a: Union[int, Iterable[int]]=[], e: int=0):
    self.mod: int = mod
    e %= mod
    self.a: List[int] = [e] * n_or_a if isinstance(n_or_a, int) else [e % mod for e in n_or_a]

  def resize(self, size: int, e: int=0):
    e %= self.mod
    self.a = [e] * size

  def append(self, v: int) -> None:
    self.a.append(v % self.mod)

  def pop(self, k: int=-1) -> int:
    return self.a.pop(k)

  def all_sum(self) -> int:
    return sum(self.a) % self.mod

  def all_mul(self) -> int:
    return reduce(lambda x, y: x * y % self.mod, self.a)

  def add(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] + v) % self.mod

  def sub(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] - v) % self.mod

  def mul(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] * v) % self.mod

  def div(self, k: int, v: int) -> None:
    self.a[k] = (self.a[k] * self._inv(v)) % self.mod

  def get_mod(self) -> int:
    return self.mod

  def __iter__(self):
    self._iter = 0
    return self

  def __next__(self):
    if self._iter >= len(self.a):
      raise StopIteration
    self._iter += 1
    return self.a[self._iter-1]

  def __getitem__(self, k: Union[int, slice]) -> Union[int, 'ModArray']:
    return ModArray(self.mod, self.a[k]) if isinstance(k, slice) else self.a[k]

  def __setitem__(self, k: int, v: int) -> None:
    assert isinstance(v, int)
    self.a[k] = v % self.mod

  def __str__(self):
    return str(self.a)

  def __len__(self):
    return len(self.a)

Array = ModArray

# ---------------------- #


