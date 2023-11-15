# from Library_py.DataStructures.AVLTree.AVLTreeSet import AVLTreeSet
# from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

# from Library_py.MyClass.OrderedSetInterface import OrderedSetInterface
from abc import ABC, abstractmethod
from typing import Iterable, Optional, Iterator, TypeVar, Generic, List
T = TypeVar('T', bound=SupportsLessThan)

class OrderedSetInterface(ABC, Generic[T]):

  @abstractmethod
  def __init__(self, a: Iterable[T]) -> None:
    raise NotImplementedError

  @abstractmethod
  def add(self, key: T) -> bool:
    raise NotImplementedError

  @abstractmethod
  def discard(self, key: T) -> bool:
    raise NotImplementedError

  @abstractmethod
  def remove(self, key: T) -> None:
    raise NotImplementedError

  @abstractmethod
  def le(self, key: T) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def lt(self, key: T) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def ge(self, key: T) -> Optional[T]:
    raise NotImplementedError

  @abstractmethod
  def gt(self, key: T) -> Optional[T]:
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
  def __contains__(self, key: T) -> bool:
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

class AVLTreeSet(OrderedSetInterface, Generic[T]):

  def __init__(self, a: Iterable[T]=[]) -> None:
    self.root = 0
    self.key = [0]
    self.size = array('I', bytes(4))
    self.left = array('I', bytes(4))
    self.right = array('I', bytes(4))
    self.balance = array('b', bytes(1))
    self.end = 1
    if not isinstance(a, list):
      a = list(a)
    if a:
      self._build(a)

  def reserve(self, n: int) -> None:
    self.key += [0] * n
    a = array('I', bytes(4*n))
    self.left += a
    self.right += a
    self.size += array('I', [1] * n)
    self.balance += array('b', bytes(n))

  def _build(self, a: List[T]) -> None:
    left, right, size, balance = self.left, self.right, self.size, self.balance
    def sort(l: int, r: int) -> Tuple[int, int]:
      mid = (l + r) >> 1
      node = mid
      hl, hr = 0, 0
      if l != mid:
        left[node], hl = sort(l, mid)
        size[node] += size[left[node]]
      if mid + 1 != r:
        right[node], hr = sort(mid+1, r)
        size[node] += size[right[node]]
      balance[node] = hl - hr
      return node, max(hl, hr)+1
    n = len(a)
    if n == 0: return
    if not all(a[i] < a[i + 1] for i in range(n - 1)):
      b = sorted(a)
      a = [b[0]]
      for i in range(1, n):
        if b[i] != a[-1]:
          a.append(b[i])
    n = len(a)
    end = self.end
    self.end += n
    self.reserve(n)
    self.key[end:end+n] = a
    self.root = sort(end, n+end)[0]

  def _rotate_L(self, node: int) -> int:
    left, right, size, balance = self.left, self.right, self.size, self.balance
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
    left, right, size, balance = self.left, self.right, self.size, self.balance
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
    balance = self.balance
    if balance[node] == 1:
      balance[self.right[node]] = -1
      balance[self.left[node]] = 0
    elif balance[node] == -1:
      balance[self.right[node]] = 0
      balance[self.left[node]] = 1
    else:
      balance[self.right[node]] = 0
      balance[self.left[node]] = 0
    balance[node] = 0

  def _rotate_LR(self, node: int) -> int:
    left, right, size = self.left, self.right, self.size
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
    left, right, size = self.left, self.right, self.size
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

  def _make_node(self, key: T) -> int:
    end = self.end
    if end >= len(self.key):
      self.key.append(key)
      self.size.append(1)
      self.left.append(0)
      self.right.append(0)
      self.balance.append(0)
    else:
      self.key[end] = key
    self.end += 1
    return end

  def add(self, key: T) -> bool:
    if self.root == 0:
      self.root = self._make_node(key)
      return True
    left, right, size, balance, keys = self.left, self.right, self.size, self.balance, self.key
    node = self.root
    path = []
    di = 0
    while node:
      if key == keys[node]:
        return False
      di <<= 1
      path.append(node)
      if key < keys[node]:
        di |= 1
        node = left[node]
      else:
        node = right[node]
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
        self.root = new_node
    for p in path:
      size[p] += 1
    return True

  def remove(self, key: T) -> bool:
    if self.discard(key):
      return True
    raise KeyError(key)

  def discard(self, key: T) -> bool:
    left, right, size, balance, keys = self.left, self.right, self.size, self.balance, self.key
    di = 0
    path = []
    node = self.root
    while node:
      if key == keys[node]:
        break
      path.append(node)
      di <<= 1
      if key < keys[node]:
        di |= 1
        node = left[node]
      else:
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
      self.root = cnode
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
          self.root = new_node
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
    keys, left, right = self.key, self.left, self.right
    res = None
    node = self.root
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
    keys, left, right = self.key, self.left, self.right
    res = None
    node = self.root
    while node:
      if key <= keys[node]:
        node = left[node]
      else:
        res = keys[node]
        node = right[node]
    return res

  def ge(self, key: T) -> Optional[T]:
    keys, left, right = self.key, self.left, self.right
    res = None
    node = self.root
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
    keys, left, right = self.key, self.left, self.right
    res = None
    node = self.root
    while node:
      if key < keys[node]:
        res = keys[node]
        node = left[node]
      else:
        node = right[node]
    return res

  def index(self, key: T) -> int:
    keys, left, right, size = self.key, self.left, self.right, self.size
    k = 0
    node = self.root
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
    keys, left, right, size = self.key, self.left, self.right, self.size
    k, node = 0, self.root
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
    return self.__getitem__(len(self)-1)

  def get_min(self) -> Optional[T]:
    if not self:
      return
    return self.__getitem__(0)

  def pop(self, k: int=-1) -> T:
    left, right, size, key, balance  = self.left, self.right, self.size, self.key, self.balance
    if k < 0:
      k += size[self.root]
    assert 0 <= k and k < size[self.root], 'IndexError'
    path = []
    di = 0
    node = self.root
    while True:
      t = size[left[node]]
      if t == k:
        res = key[node]
        break
      path.append(node)
      di <<= 1
      if t < k:
        k -= t + 1
        node = right[node]
      else:
        di |= 1
        node = left[node]
    if left[node] and right[node]:
      path.append(node)
      di <<= 1
      di |= 1
      lmax = left[node]
      while right[lmax]:
        path.append(lmax)
        di <<= 1
        lmax = right[lmax]
      key[node] = key[lmax]
      node = lmax
    cnode = right[node] if left[node] == 0 else left[node]
    if path:
      if di & 1:
        left[path[-1]] = cnode
      else:
        right[path[-1]] = cnode
    else:
      self.root = cnode
      return res
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
          self.root = new_node
          return res
        if di & 1:
          left[path[-1]] = new_node
        else:
          right[path[-1]] = new_node
        if balance[new_node]:
          break
    for p in path:
      size[p] -= 1
    return res

  def pop_max(self) -> T:
    return self.pop()

  def pop_min(self) -> T:
    return self.pop(0)

  def clear(self) -> None:
    self.root = 0

  def tolist(self) -> List[T]:
    left, right, keys = self.left, self.right, self.key
    node = self.root
    stack, a = [], []
    while stack or node:
      if node:
        stack.append(node)
        node = left[node]
      else:
        node = stack.pop()
        a.append(keys[node])
        node = right[node]
    return a

  def __contains__(self, key: T) -> bool:
    keys, left, right = self.key, self.left, self.right
    node = self.root
    while node:
      if key == keys[node]:
        return True
      node = left[node] if key < keys[node] else right[node]
    return False

  def __getitem__(self, k: int) -> T:
    left, right, size, key  = self.left, self.right, self.size, self.key
    if k < 0:
      k += size[self.root]
    assert 0 <= k and k < size[self.root], 'IndexError'
    node = self.root
    while True:
      t = size[left[node]]
      if t == k:
        return key[node]
      elif t < k:
        k -= t + 1
        node = right[node]
      else:
        node = left[node]

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
    return self.size[self.root]

  def __bool__(self):
    return self.root != 0

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'AVLTreeSet({self})'


