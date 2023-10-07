from typing import Protocol

class SupportsLessThan(Protocol):

  def __lt__(self, other) -> bool: ...

from abc import ABC, abstractmethod
from typing import Iterable, Optional, Iterator, TypeVar, Generic, List
T = TypeVar('T', bound=SupportsLessThan)

class OrderedMultisetInterface(ABC, Generic[T]):

  @abstractmethod
  def __init__(self, a: Iterable[T]) -> None:
    raise NotImplementedError

  @abstractmethod
  def add(self, key: T, cnt: int) -> None:
    raise NotImplementedError

  @abstractmethod
  def discard(self, key: T, cnt: int) -> bool:
    raise NotImplementedError

  @abstractmethod
  def discard_all(self, key: T) -> bool:
    raise NotImplementedError

  @abstractmethod
  def count(self, key: T) -> int:
    raise NotImplementedError

  @abstractmethod
  def remove(self, key: T, cnt: int) -> None:
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

from typing import Generic, Iterable, Iterator, Tuple, TypeVar, List, Optional
T = TypeVar('T', bound=SupportsLessThan)

class AVLTreeMultiset3(OrderedMultisetInterface, Generic[T]):

  class Node():

    def __init__(self, key: T, val: int):
      self.key: T = key
      self.val: int = val
      self.valsize: int = val
      self.size: int = 1
      self.left: Optional['AVLTreeMultiset3.Node'] = None
      self.right: Optional['AVLTreeMultiset3.Node'] = None
      self.balance: int = 0

    def __str__(self):
      if self.left is None and self.right is None:
        return f'key:{self.key, self.val, self.size, self.valsize}\n'
      return f'key:{self.key, self.val, self.size, self.valsize},\n left:{self.left},\n right:{self.right}\n'

  def __init__(self, a: Iterable[T]=[]):  
    self.node: Optional['AVLTreeMultiset3.Node'] = None
    if a:
      self._build(a)

  def _rle(self, L: List[T]) -> Tuple[List[T], List[int]]:
    x, y = [L[0]], [1]
    for i, a in enumerate(L):
      if i == 0:
        continue
      if a == x[-1]:
        y[-1] += 1
        continue
      x.append(a)
      y.append(1)
    return x, y

  def _build(self, a: Iterable[T]) -> None:
    Node = AVLTreeMultiset3.Node
    def sort(l: int, r: int) -> Tuple[Node, int]:
      mid = (l + r) >> 1
      node = Node(x[mid], y[mid])
      h = 0
      if l != mid:
        left, hl = sort(l, mid)
        node.left = left
        node.size += left.size
        node.valsize += left.valsize
        node.balance = hl
        h = hl
      if mid+1 != r:
        right, hr = sort(mid+1, r)
        node.right = right
        node.size += right.size
        node.valsize += right.valsize
        node.balance -= hr
        if hr > h:
          h = hr
      return node, h+1
    a = sorted(a)
    if not a:
      return
    x, y = self._rle(a)
    self.node = sort(0, len(x))[0]

  def _rotate_L(self, node: Node) -> Node:
    u = node.left
    u.size = node.size
    u.valsize = node.valsize
    if u.left is None:
      node.size -= 1
      node.valsize -= u.val
    else:
      node.size -= u.left.size + 1
      node.valsize -= u.left.valsize + u.val
    node.left = u.right
    u.right = node
    if u.balance == 1:
      u.balance = 0
      node.balance = 0
    else:
      u.balance = -1
      node.balance = 1
    return u

  def _rotate_R(self, node: Node) -> Node:
    u = node.right
    u.size = node.size
    u.valsize = node.valsize
    if u.right is None:
      node.size -= 1
      node.valsize -= u.val
    else:
      node.size -= u.right.size + 1
      node.valsize -= u.right.valsize + u.val
    node.right = u.left
    u.left = node
    if u.balance == -1:
      u.balance = 0
      node.balance = 0
    else:
      u.balance = 1
      node.balance = -1
    return u

  def _update_balance(self, node: Node) -> None:
    if node.balance == 1:
      node.right.balance = -1
      node.left.balance = 0
    elif node.balance == -1:
      node.right.balance = 0
      node.left.balance = 1
    else:
      node.right.balance = 0
      node.left.balance = 0
    node.balance = 0

  def _rotate_LR(self, node: Node) -> Node:
    B = node.left
    E = B.right
    E.size = node.size
    E.valsize = node.valsize
    if E.right is None:
      node.size -= B.size
      node.valsize -= B.valsize
      B.size -= 1
      B.valsize -= E.val
    else:
      node.size -= B.size - E.right.size
      node.valsize -= B.valsize - E.right.valsize
      B.size -= E.right.size + 1
      B.valsize -= E.right.valsize + E.val
    B.right = E.left
    E.left = B
    node.left = E.right
    E.right = node
    self._update_balance(E)
    return E

  def _rotate_RL(self, node: Node) -> Node:
    C = node.right
    D = C.left
    D.size = node.size
    D.valsize = node.valsize
    if D.left is None:
      node.size -= C.size
      node.valsize -= C.valsize
      C.size -= 1
      C.valsize -= D.val
    else:
      node.size -= C.size - D.left.size
      node.valsize -= C.valsize - D.left.valsize
      C.size -= D.left.size + 1
      C.valsize -= D.left.valsize + D.val
    C.left = D.right
    D.right = C
    node.right = D.left
    D.left = node
    self._update_balance(D)
    return D

  def _kth_elm(self, k: int) -> Tuple[T, int]:
    if k < 0: k += len(self)
    node = self.node
    while True:
      t = node.val if node.left is None else node.val + node.left.valsize
      if t-node.val <= k < t:
        return node.key, node.val
      elif t > k:
        node = node.left
      else:
        node = node.right
        k -= t

  def _kth_elm_tree(self, k: int) -> Tuple[T, int]:
    if k < 0:
      k += self.len_elm()
    assert 0 <= k < self.len_elm()
    node = self.node
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key, node.val
      elif t > k:
        node = node.left
      else:
        node = node.right
        k -= t + 1

  def _discard(self, node: Node, path: List[Node], di: int) -> bool:
    fdi = 0
    if node.left is not None and node.right is not None:
      path.append(node)
      di <<= 1
      di |= 1
      lmax = node.left
      while lmax.right is not None:
        path.append(lmax)
        di <<= 1
        fdi <<= 1
        fdi |= 1
        lmax = lmax.right
      lmax_val = lmax.val
      node.key = lmax.key
      node.val = lmax_val
      node = lmax
    cnode = node.right if node.left is None else node.left
    if path:
      if di & 1:
        path[-1].left = cnode
      else:
        path[-1].right = cnode
    else:
      self.node = cnode
      return True
    while path:
      new_node = None
      pnode = path.pop()
      pnode.balance -= 1 if di & 1 else -1
      pnode.size -= 1
      pnode.valsize -= lmax_val if fdi & 1 else 1
      di >>= 1
      fdi >>= 1
      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance < 0 else self._rotate_L(pnode)
      elif pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance> 0 else self._rotate_R(pnode)
      elif pnode.balance != 0:
        break
      if new_node is not None:
        if not path:
          self.node = new_node
          return    
        if di & 1:
          path[-1].left = new_node
        else:
          path[-1].right = new_node
        if new_node.balance != 0:
          break
    while path:
      pnode = path.pop()
      pnode.size -= 1
      pnode.valsize -= lmax_val if fdi & 1 else 1
      fdi >>= 1
    return True

  def discard(self, key: T, val: int=1) -> bool:
    path = []
    di = 0
    node = self.node
    while node is not None:
      if key == node.key:
        break
      elif key < node.key:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
    else:
      return False
    if val > node.val:
      val = node.val - 1
      node.val -= val
      node.valsize -= val
      for p in path:
        p.valsize -= val
    if node.val == 1:
      self._discard(node, path, di)
    else:
      node.val -= val
      node.valsize -= val
      for p in path:
        p.valsize -= val
    return True

  def discard_all(self, key: T) -> None:
    self.discard(key, self.count(key))

  def remove(self, key: T, val: int=1) -> None:
    if self.discard(key, val):
      return
    raise KeyError(key)

  def add(self, key: T, val: int=1) -> None:
    if self.node is None:
      self.node = AVLTreeMultiset3.Node(key, val)
      return
    pnode = self.node
    di = 0
    path = []
    while pnode is not None:
      if key == pnode.key:
        pnode.val += val
        pnode.valsize += val
        for p in path:
          p.valsize += val
        return
      elif key < pnode.key:
        path.append(pnode)
        di <<= 1
        di |= 1
        pnode = pnode.left
      else:
        path.append(pnode)
        di <<= 1
        pnode = pnode.right
    if di & 1:
      path[-1].left = AVLTreeMultiset3.Node(key, val)
    else:
      path[-1].right = AVLTreeMultiset3.Node(key, val)
    new_node = None
    while path:
      pnode = path.pop()
      pnode.size += 1
      pnode.valsize += val
      pnode.balance += 1 if di & 1 else -1
      di >>= 1
      if pnode.balance == 0:
        break
      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance < 0 else self._rotate_L(pnode)
        break
      elif pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance> 0 else self._rotate_R(pnode)
        break
    if new_node is not None:
      if path:
        if di & 1:
          path[-1].left = new_node
        else:
          path[-1].right = new_node
      else:
        self.node = new_node
    for p in path:
      p.size += 1
      p.valsize += val

  def count(self, key: T) -> int:
    node = self.node
    while node is not None:
      if node.key == key:
        return node.val
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return 0

  def le(self, key: T) -> Optional[T]:
    res = None
    node = self.node
    while node is not None:
      if key == node.key:
        res = key
        break
      elif key < node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  def lt(self, key: T) -> Optional[T]:
    res = None
    node = self.node
    while node is not None:
      if key <= node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  def ge(self, key: T) -> Optional[T]:
    res = None
    node = self.node
    while node is not None:
      if key == node.key:
        res = key
        break
      elif key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  def gt(self, key: T) -> Optional[T]:
    res = None
    node = self.node
    while node is not None:
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  def index(self, key: T) -> int:
    k = 0
    node = self.node
    while node is not None:
      if key == node.key:
        if node.left is not None:
          k += node.left.valsize
        break
      elif key < node.key:
        node = node.left
      else:
        k += node.val if node.left is None else node.left.valsize + node.val
        node = node.right
    return k

  def index_right(self, key: T) -> int:
    k = 0
    node = self.node
    while node is not None:
      if key == node.key:
        k += node.val if node.left is None else node.left.valsize + node.val
        break
      elif key < node.key:
        node = node.left
      else:
        k += node.val if node.left is None else node.left.valsize + node.val
        node = node.right
    return k

  def index_keys(self, key: T) -> int:
    k = 0
    node = self.node
    while node:
      if key == node.key:
        if node.left is not None:
          k += node.left.size
        break
      elif key < node.key:
        node = node.left
      else:
        k += node.val if node.left is None else node.left.size + node.val
        node = node.right
    return k

  def index_right_keys(self, key: T) -> int:
    k = 0
    node = self.node
    while node:
      if key == node.key:
        k += node.val if node.left is None else node.left.size + node.val
        break
      elif key < node.key:
        node = node.left
      else:
        k += node.val if node.left is None else node.left.size + node.val
        node = node.right
    return k

  def get_min(self) -> Optional[T]:
    if self.node is None:
      return
    node = self.node
    while node.left is not None:
      node = node.left
    return node.key

  def get_max(self) -> Optional[T]:
    if self.node is None:
      return
    node = self.node
    while node.right is not None:
      node = node.right
    return node.key

  def pop(self, k: int=-1) -> T:
    if k < 0: k += self.node.valsize
    node = self.node
    path = []
    if k == self.node.valsize-1:
      while node.right is not None:
        path.append(node)
        node = node.right
      x = node.key
      if node.val == 1:
        self._discard(node, path, 0)
      else:
        node.val -= 1
        node.valsize -= 1
        for p in path:
          p.valsize -= 1
      return x
    di = 0
    while True:
      t = node.val if node.left is None else node.val + node.left.valsize
      if t-node.val <= k < t:
        x = node.key
        break
      elif t > k:
        path.append(node)
        di <<= 1
        di |= 1
        node = node.left
      else:
        path.append(node)
        di <<= 1
        node = node.right
        k -= t
    if node.val == 1:
      self._discard(node, path, di)
    else:
      node.val -= 1
      node.valsize -= 1
      for p in path:
        p.valsize -= 1
    return x

  def pop_max(self) -> T:
    assert self
    return self.pop()

  def pop_min(self) -> T:
    node = self.node
    path = []
    while node.left is not None:
      path.append(node)
      node = node.left
    x = node.key
    if node.val == 1:
      self._discard(node, path, (1<<len(path))-1)
    else:
      node.val -= 1
      node.valsize -= 1
      for p in path:
        p.valsize -= 1
    return x

  def items(self) -> Iterator[Tuple[T, int]]:
    for i in range(self.len_elm()):
      yield self._kth_elm_tree(i)

  def keys(self) -> Iterator[T]:
    for i in range(self.len_elm()):
      yield self._kth_elm_tree(i)[0]

  def values(self) -> Iterator[int]:
    for i in range(self.len_elm()):
      yield self._kth_elm_tree(i)[1]

  def len_elm(self) -> int:
    return 0 if self.node is None else self.node.size

  def show(self) -> None:
    print('{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.tolist_items())) + '}')

  def clear(self) -> None:
    self.node = None

  def get_elm(self, k: int) -> T:
    return self._kth_elm_tree(k)[0]

  def tolist(self) -> List[T]:
    a = []
    if self.node is None:
      return a
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.extend([node.key]*node.val)
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def tolist_items(self) -> List[Tuple[T, int]]:
    a = []
    if self.node is None:
      return a
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.append((node.key, node.val))
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def __getitem__(self, k: int):
    return self._kth_elm(k)[0]

  def __contains__(self, key: T):
    node = self.node
    while node:
      if node.key == key:
        return True
      node = node.left if key < node.key else node.right
    return False

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == len(self):
      raise StopIteration
    res = self._kth_elm(self.__iter)
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(len(self)):
      yield self._kth_elm(-i-1)[0]

  def __len__(self):
    return 0 if self.node is None else self.node.valsize

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'AVLTreeMultiset3({self.tolist()})'


