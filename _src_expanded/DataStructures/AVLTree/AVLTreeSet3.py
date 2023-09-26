from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

from abc import ABC, abstractmethod
from typing import Iterable, Optional, Iterator, TypeVar, Generic, List
T = TypeVar('T', bound=SupportsLessThan)

class OrderedSetInterface(ABC, Generic[T]):

  @abstractmethod
  def __init__(self, a: Iterable[T]) -> None:
    raise NotImplementedError

  @abstractmethod
  def add(self, item: T) -> bool:
    raise NotImplementedError

  @abstractmethod
  def discard(self, item: T) -> bool:
    raise NotImplementedError

  @abstractmethod
  def remove(self, item: T) -> None:
    raise NotImplementedError

  @abstractmethod
  def le(self, item: T) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def lt(self, item: T) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def ge(self, item: T) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def gt(self, item: T) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def get_max(self) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def get_min(self) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def pop_max(self) -> T:
    raise NotImplementedError

  @abstractmethod
  def pop_min(self) -> T:
    raise NotImplementedError

  @abstractmethod
  def clear(self) -> None:
    raise NotImplementedError

  @abstractmethod
  def tolist(self) -> List[T]:
    raise NotImplementedError

  @abstractmethod
  def __iter__(self) -> Iterator:
    raise NotImplementedError

  @abstractmethod
  def __next__(self) -> T:
    raise NotImplementedError

  @abstractmethod
  def __contains__(self) -> bool:
    raise NotImplementedError

  @abstractmethod
  def __len__(self) -> int:
    raise NotImplementedError

  @abstractmethod
  def __bool__(self) -> bool:
    raise NotImplementedError

  @abstractmethod
  def __str__(self) -> str:
    raise NotImplementedError

  @abstractmethod
  def __repr__(self) -> str:
    raise NotImplementedError

from array import array
from typing import Generic, Iterable, Tuple, TypeVar, Optional, List
T = TypeVar('T', bound=SupportsLessThan)

class AVLTreeSet3(OrderedSetInterface, Generic[T]):

  key = [0]
  size = array('I', bytes(4))
  left = array('I', bytes(4))
  right = array('I', bytes(4))
  balance = array('i', bytes(4))
  end = 1

  @classmethod
  def reserve(cls, n: int) -> None:
    cls.key += [0] * n
    cls.size += array('I', [1] * n)
    cls.left += array('I', bytes(4 * n))
    cls.right += array('I', bytes(4 * n))
    cls.balance += array('i', bytes(4 * n))

  def __init__(self, a: Iterable[T]=[]) -> None:
    self.node = 0
    if not isinstance(a, list):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    left, right, size, balance = AVLTreeSet3.left, AVLTreeSet3.right, AVLTreeSet3.size, AVLTreeSet3.balance
    def sort(l: int, r: int) -> Tuple[int, int]:
      mid = (l + r) >> 1
      node = mid
      if l != mid:
        left[node], hl = sort(l, mid)
        size[node] += size[left[node]]
      else:
        hl = 0
      if mid + 1 != r:
        right[node], hr = sort(mid+1, r)
        size[node] += size[right[node]]
      else:
        hr = 0
      balance[node] = hl - hr
      return node, max(hl, hr)+1
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(set(a))
    n = len(a)
    end = AVLTreeSet3.end
    AVLTreeSet3.end += n
    AVLTreeSet3.reserve(n)
    AVLTreeSet3.key[end:end+n] = a
    self.node = sort(end, n+end)[0]

  def _rotate_L(self, node: int) -> int:
    left, right, size, balance = AVLTreeSet3.left, AVLTreeSet3.right, AVLTreeSet3.size, AVLTreeSet3.balance
    u = left[node]
    size[u] = size[node]
    size[node] -= size[left[u]] + 1
    left[node] = right[u]
    right[u] = node
    if balance[u] == 1:
      balance[u] = 0
      balance[node] = 0
    else:
      balance[u] = -1
      balance[node] = 1
    return u

  def _rotate_R(self, node: int) -> int:
    left, right, size, balance = AVLTreeSet3.left, AVLTreeSet3.right, AVLTreeSet3.size, AVLTreeSet3.balance
    u = right[node]
    size[u] = size[node]
    size[node] -= size[right[u]] + 1
    right[node] = left[u]
    left[u] = node
    if balance[u] == -1:
      balance[u] = 0
      balance[node] = 0
    else:
      balance[u] = 1
      balance[node] = -1
    return u

  def _update_balance(self, node: int) -> None:
    balance = AVLTreeSet3.balance
    if balance[node] == 1:
      balance[AVLTreeSet3.right[node]] = -1
      balance[AVLTreeSet3.left[node]] = 0
    elif balance[node] == -1:
      balance[AVLTreeSet3.right[node]] = 0
      balance[AVLTreeSet3.left[node]] = 1
    else:
      balance[AVLTreeSet3.right[node]] = 0
      balance[AVLTreeSet3.left[node]] = 0
    balance[node] = 0

  def _rotate_LR(self, node: int) -> int:
    left, right, size = AVLTreeSet3.left, AVLTreeSet3.right, AVLTreeSet3.size
    B = left[node]
    E = right[B]
    size[E] = size[node]
    size[node] -= size[B] - size[right[E]]
    size[B] -= size[right[E]] + 1
    right[B] = left[E]
    left[E] = B
    left[node] = right[E]
    right[E] = node
    self._update_balance(E)
    return E

  def _rotate_RL(self, node: int) -> int:
    left, right, size = AVLTreeSet3.left, AVLTreeSet3.right, AVLTreeSet3.size
    C = right[node]
    D = left[C]
    size[D] = size[node]
    size[node] -= size[C] - size[left[D]]
    size[C] -= size[left[D]] + 1
    left[C] = right[D]
    right[D] = C
    right[node] = left[D]
    left[D] = node
    self._update_balance(D)
    return D

  def _kth_elm(self, k: int) -> T:
    left, right = AVLTreeSet3.left, AVLTreeSet3.right
    size, key = AVLTreeSet3.size, AVLTreeSet3.key
    if k < 0: k += size[self.node]
    assert 0 <= k and k < size[self.node], 'IndexError'
    node = self.node
    while True:
      t = size[left[node]]
      if t == k:
        return key[node]
      elif t < k:
        k -= t + 1
        node = right[node]
      else:
        node = left[node]

  def _make_node(self, key: T) -> int:
    end = AVLTreeSet3.end
    if end >= len(AVLTreeSet3.key):
      AVLTreeSet3.key.append(key)
      AVLTreeSet3.size.append(1)
      AVLTreeSet3.left.append(0)
      AVLTreeSet3.right.append(0)
      AVLTreeSet3.balance.append(0)
    else:
      AVLTreeSet3.key[end] = key
    AVLTreeSet3.end += 1
    return end

  def add(self, key: T) -> bool:
    if self.node == 0:
      self.node = self._make_node(key)
      return True
    left, right, size = AVLTreeSet3.left, AVLTreeSet3.right, AVLTreeSet3.size
    balance, keys = AVLTreeSet3.balance, AVLTreeSet3.key
    pnode = self.node
    path = []
    di = 0
    while pnode:
      if key == keys[pnode]:
        return False
      elif key < keys[pnode]:
        path.append(pnode)
        di <<= 1
        di |= 1
        pnode = left[pnode]
      else:
        path.append(pnode)
        di <<= 1
        pnode = right[pnode]
    if di & 1:
      left[path[-1]] = self._make_node(key)
    else:
      right[path[-1]] = self._make_node(key)
    new_node = 0
    while path:
      pnode = path.pop()
      size[pnode] += 1
      balance[pnode] += 1 if di & 1 else -1
      di >>= 1
      if balance[pnode] == 0:
        break
      if balance[pnode] == 2:
        new_node = self._rotate_LR(pnode) if balance[left[pnode]] == -1 else self._rotate_L(pnode)
        break
      elif balance[pnode] == -2:
        new_node = self._rotate_RL(pnode) if balance[right[pnode]] == 1 else self._rotate_R(pnode)
        break
    if new_node:
      if path:
        gnode = path.pop()
        size[gnode] += 1
        if di & 1:
          left[gnode] = new_node
        else:
          right[gnode] = new_node
      else:
        self.node = new_node
    for p in path:
      size[p] += 1
    return True

  def remove(self, key: T) -> bool:
    if self.discard(key):
      return True
    raise KeyError

  def discard(self, key: T) -> bool:
    left, right, size = AVLTreeSet3.left, AVLTreeSet3.right, AVLTreeSet3.size
    balance, keys = AVLTreeSet3.balance, AVLTreeSet3.key
    di = 0
    path = []
    node = self.node
    while node:
      if key == keys[node]:
        break
      elif key < keys[node]:
        path.append(node)
        di <<= 1
        di |= 1
        node = left[node]
      else:
        path.append(node)
        di <<= 1
        node = right[node]
    else:
      return False
    if left[node] and right[node]:
      path.append(node)
      di <<= 1
      di |= 1
      lmax = left[node]
      while right[lmax]:
        path.append(lmax)
        di <<= 1
        lmax = right[lmax]
      keys[node] = keys[lmax]
      node = lmax
    cnode = right[node] if left[node] == 0 else left[node]
    if path:
      if di & 1:
        left[path[-1]] = cnode
      else:
        right[path[-1]] = cnode
    else:
      self.node = cnode
      return True
    while path:
      new_node = 0
      pnode = path.pop()
      balance[pnode] -= 1 if di & 1 else -1
      di >>= 1
      size[pnode] -= 1
      if balance[pnode] == 2:
        new_node = self._rotate_LR(pnode) if balance[left[pnode]] == -1 else self._rotate_L(pnode)
      elif balance[pnode] == -2:
        new_node = self._rotate_RL(pnode) if balance[right[pnode]] == 1 else self._rotate_R(pnode)
      elif balance[pnode]:
        break
      if new_node:
        if not path:
          self.node = new_node
          return True
        if di & 1:
          left[path[-1]] = new_node
        else:
          right[path[-1]] = new_node
        if balance[new_node]:
          break
    for p in path:
      size[p] -= 1
    return True

  def le(self, key: T) -> Optional[T]:
    keys, left, right = AVLTreeSet3.key, AVLTreeSet3.left, AVLTreeSet3.right
    res = None
    node = self.node
    while node:
      if key == keys[node]:
        res = key
        break
      elif key < keys[node]:
        node = left[node]
      else:
        res = keys[node]
        node = right[node]
    return res

  def lt(self, key: T) -> Optional[T]:
    keys, left, right = AVLTreeSet3.key, AVLTreeSet3.left, AVLTreeSet3.right
    res = None
    node = self.node
    while node:
      if key <= keys[node]:
        node = left[node]
      else:
        res = keys[node]
        node = right[node]
    return res

  def ge(self, key: T) -> Optional[T]:
    keys, left, right = AVLTreeSet3.key, AVLTreeSet3.left, AVLTreeSet3.right
    res = None
    node = self.node
    while node:
      if key == keys[node]:
        res = key
        break
      elif key < keys[node]:
        res = keys[node]
        node = left[node]
      else:
        node = right[node]
    return res

  def gt(self, key: T) -> Optional[T]:
    keys, left, right = AVLTreeSet3.key, AVLTreeSet3.left, AVLTreeSet3.right
    res = None
    node = self.node
    while node:
      if key < keys[node]:
        res = keys[node]
        node = left[node]
      else:
        node = right[node]
    return res

  def index(self, key: T) -> int:
    keys, left, right, size = AVLTreeSet3.key, AVLTreeSet3.left, AVLTreeSet3.right, AVLTreeSet3.size
    k = 0
    node = self.node
    while node:
      if key == keys[node]:
        k += size[left[node]]
        break
      elif key < keys[node]:
        node = left[node]
      else:
        k += size[left[node]] + 1
        node = right[node]
    return k

  def index_right(self, key: T) -> int:
    keys, left, right, size = AVLTreeSet3.key, AVLTreeSet3.left, AVLTreeSet3.right, AVLTreeSet3.size
    k, node = 0, self.node
    while node:
      if key == keys[node]:
        k += size[left[node]] + 1
        break
      elif key < keys[node]:
        node = left[node]
      else:
        k += size[left[node]] + 1
        node = right[node]
    return k

  def get_max(self) -> Optional[T]:
    if not self:
      return
    return self._kth_elm(len(self)-1)

  def get_min(self) -> Optional[T]:
    if not self:
      return
    return self._kth_elm(0)

  def pop(self, k: int=-1) -> T:
    x = self._kth_elm(k)
    self.discard(x)
    return x

  def pop_max(self) -> T:
    return self.pop()

  def pop_min(self) -> T:
    return self.pop(0)

  def clear(self) -> None:
    self.node = 0

  def tolist(self) -> List[T]:
    a = []
    if not self.node:
      return a
    def rec(node):
      if AVLTreeSet3.left[node]:
        rec(AVLTreeSet3.left[node])
      a.append(AVLTreeSet3.key[node])
      if AVLTreeSet3.right[node]:
        rec(AVLTreeSet3.right[node])
    rec(self.node)
    return a

  def __contains__(self, key: T) -> bool:
    keys, left, right = AVLTreeSet3.key, AVLTreeSet3.left, AVLTreeSet3.right
    node = self.node
    while node:
      if key == keys[node]:
        return True
      elif key < keys[node]:
        node = left[node]
      else:
        node = right[node]
    return False

  def __getitem__(self, k: int) -> T:
    return self._kth_elm(k)

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self.__getitem__(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self.__getitem__(-i-1)

  def __len__(self):
    return AVLTreeSet3.size[self.node]

  def __bool__(self):
    return self.node != 0

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'AVLTreeSet3({self})'


