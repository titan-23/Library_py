from array import array
from typing import Generic, Iterable, Tuple, TypeVar, Optional, List
T = TypeVar('T')

class AVLTreeSet(Generic[T]):

  key = [0]
  size = array('I', [0])
  left = array('I', [0])
  right = array('I', [0])
  balance = array('i', [0])
  end = 1

  @classmethod
  def reserve(cls, n: int) -> None:
    cls.key += [0] * n
    cls.size += array('I', [1] * n)
    cls.left += array('I', [0] * n)
    cls.right += array('I', [0] * n)
    cls.balance += array('i', [0] * n)

  def __init__(self, a: Iterable[T]=[]) -> None:
    self.node = 0
    if not isinstance(a, list):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    left, right, size, balance = AVLTreeSet.left, AVLTreeSet.right, AVLTreeSet.size, AVLTreeSet.balance
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
    end = AVLTreeSet.end
    AVLTreeSet.end += n
    AVLTreeSet.reserve(n)
    AVLTreeSet.key[end:end+n] = a
    self.node = sort(end, n+end)[0]

  def _rotate_L(self, node: int) -> int:
    left, right, size, balance = AVLTreeSet.left, AVLTreeSet.right, AVLTreeSet.size, AVLTreeSet.balance
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
    left, right, size, balance = AVLTreeSet.left, AVLTreeSet.right, AVLTreeSet.size, AVLTreeSet.balance
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
    balance = AVLTreeSet.balance
    if balance[node] == 1:
      balance[AVLTreeSet.right[node]] = -1
      balance[AVLTreeSet.left[node]] = 0
    elif balance[node] == -1:
      balance[AVLTreeSet.right[node]] = 0
      balance[AVLTreeSet.left[node]] = 1
    else:
      balance[AVLTreeSet.right[node]] = 0
      balance[AVLTreeSet.left[node]] = 0
    balance[node] = 0

  def _rotate_LR(self, node: int) -> int:
    left, right, size = AVLTreeSet.left, AVLTreeSet.right, AVLTreeSet.size
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
    left, right, size = AVLTreeSet.left, AVLTreeSet.right, AVLTreeSet.size
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
    left, right = AVLTreeSet.left, AVLTreeSet.right
    size, key = AVLTreeSet.size, AVLTreeSet.key
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
    end = AVLTreeSet.end
    if end >= len(AVLTreeSet.key):
      AVLTreeSet.key.append(key)
      AVLTreeSet.size.append(1)
      AVLTreeSet.left.append(0)
      AVLTreeSet.right.append(0)
      AVLTreeSet.balance.append(0)
    else:
      AVLTreeSet.key[end] = key
    AVLTreeSet.end += 1
    return end

  def add(self, key: T) -> bool:
    if self.node == 0:
      self.node = self._make_node(key)
      return True
    left, right, size = AVLTreeSet.left, AVLTreeSet.right, AVLTreeSet.size
    balance, keys = AVLTreeSet.balance, AVLTreeSet.key
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
    left, right, size = AVLTreeSet.left, AVLTreeSet.right, AVLTreeSet.size
    balance, keys = AVLTreeSet.balance, AVLTreeSet.key
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
    keys, left, right = AVLTreeSet.key, AVLTreeSet.left, AVLTreeSet.right
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
    keys, left, right = AVLTreeSet.key, AVLTreeSet.left, AVLTreeSet.right
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
    keys, left, right = AVLTreeSet.key, AVLTreeSet.left, AVLTreeSet.right
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
    keys, left, right = AVLTreeSet.key, AVLTreeSet.left, AVLTreeSet.right
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
    keys, left, right, size = AVLTreeSet.key, AVLTreeSet.left, AVLTreeSet.right, AVLTreeSet.size
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
    keys, left, right, size = AVLTreeSet.key, AVLTreeSet.left, AVLTreeSet.right, AVLTreeSet.size
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

  def pop(self, k: int=-1) -> T:
    x = self._kth_elm(k)
    self.discard(x)
    return x

  def pop_min(self) -> T:
    return self.pop(0)

  def clear(self) -> None:
    self.node = 0

  def tolist(self) -> List[T]:
    a = []
    if not self.node:
      return a
    def rec(node):
      if AVLTreeSet.left[node]:
        rec(AVLTreeSet.left[node])
      a.append(AVLTreeSet.key[node])
      if AVLTreeSet.right[node]:
        rec(AVLTreeSet.right[node])
    rec(self.node)
    return a

  def __contains__(self, key: T) -> bool:
    keys, left, right = AVLTreeSet.key, AVLTreeSet.left, AVLTreeSet.right
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
    return AVLTreeSet.size[self.node]

  def __bool__(self):
    return self.node != 0

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'AVLTreeSet({self})'

