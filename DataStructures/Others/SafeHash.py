from typing import Iterable, Set
import random

class HashSet():

  _xor = random.randrange(10000000, 1000000000)

  def __init__(self, a: Iterable[int]=[]):
    self._data: Set[int] = set(x^HashSet._xor for x in a)

  def add(self, key: int) -> None:
    self._data.add(key^HashSet._xor)

  def discard(self, key: int) -> None:
    self._data.discard(key^HashSet._xor)

  def remove(self, key: int) -> None:
    self._data.remove(key^HashSet._xor)

  def __contains__(self, key: int):
    return key^HashSet._xor in self._data

  def __len__(self):
    return len(self._data)

  def __iter__(self):
    return (k^HashSet._xor for k in self._data.__iter__())

  def __str__(self):
    return '{' + ', '.join(sorted(map(str, self))) + '}'

  def __repr__(self):
    return f'HashSet({self})'

from typing import Iterable, Dict, Any
import random

class HashDict():

  _xor = random.randrange(10000000, 1000000000)

  def __init__(self):
    self._data: Dict = {}

  def __setitem__(self, key: int, val: Any):
    self._data[key^HashDict._xor] = val

  def __getitem__(self, key: int) -> Any:
    return self._data[key^HashDict._xor]

  def __delitem__(self, key: int):
    del self._data[key^HashDict._xor]

  def __contains__(self, key: int):
    return key^HashDict._xor in self._data

  def __len__(self):
    return len(self._data)

  def keys(self):
    return (k^HashDict._xor for k in self._data.keys())

  def values(self):
    return (v for v in self._data.values())

  def items(self):
    return ((k^HashDict._xor, v) for k, v in self._data.items())

  def __str__(self):
    return '{' + ', '.join(f'{k}: {v}' for k,v in self.items()) + '}'

from typing import Iterable
import random

class HashCounter():

  def __init__(self, a: Iterable[int]=[]):
    self._data = HashDict()
    for a_ in a:
      if a_ in self._data:
        self._data[a_] += 1
      else:
        self._data[a_] = 1

  def __iter__(self):
    for k, v in self._data.items():
      yield k, v

  def __setitem__(self, key: int, val: int):
    self._data[key] = val

  def __getitem__(self, key: int) -> int:
    return self._data[key] if key in self._data else 0

  def __delitem__(self, key: int):
    if key in self._data:
      del self._data[key]

  def __contains__(self, key: int):
    return key in self._data

  def most_common(self):
    return sorted(self._data.items(), key=lambda x: -x[1])

  def keys(self):
    return self._data.keys()

  def values(self):
    return self._data.values()

  def items(self):
    return self._data.items()

  def __len__(self):
    return len(self._data)

  def __str__(self):
    return f'HashCounter({str(self._data)})'

from typing import Iterable
from collections import defaultdict
import random

class HashDefaultDict():
  
  _xor = random.randrange(10000000, 1000000000)

  def __init__(self, missing):
    self._data = defaultdict(missing)

  def __iter__(self):
    for k, v in self.items():
      yield k, v

  def __setitem__(self, key: int, value):
    self._data[key^HashDefaultDict._xor] = value

  def __getitem__(self, key: int):
    return self._data[key^HashDefaultDict._xor]

  def __delitem__(self, key: int):
    del self._data[key^HashDefaultDict._xor]

  def __contains__(self, item):
    return item^HashDefaultDict._xor in self._data

  def __len__(self):
    return len(self._data)

  def keys(self):
    return (k^HashDefaultDict._xor for k in self._data.keys())

  def values(self):
    return (v for v in self._data.values())

  def items(self):
    return ((k^HashDefaultDict._xor, v) for k, v in self._data.items())

  def __str__(self):
    return 'HashDefaultDict({' + ', '.join(f'{k}: {v}' for k,v in self.items()) + '})'

