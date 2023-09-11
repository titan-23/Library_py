from Library_py.MyClass.OrderedSetInterface import OrderedSetInterface
from Library_py.MyClass.SupportsLessThan import SupportsLessThan
from typing import Generic, Iterable, Tuple, TypeVar, List, Optional, Sequence
T = TypeVar('T', bound=SupportsLessThan)

class AVLTreeSet(OrderedSetInterface, Generic[T]):

  class Node:

    def __init__(self, key: T):
      self.key: T = key
      self.size: int = 1
      self.left: Optional['AVLTreeSet.Node'] = None
      self.right: Optional['AVLTreeSet.Node'] = None
      self.balance: int = 0

    def __str__(self):
      if self.left is None and self.right is None:
        return f'key:{self.key, self.size}\n'
      return f'key:{self.key, self.size},\n left:{self.left},\n right:{self.right}\n'

  def __init__(self, a: Iterable[T]=[]) -> None:  
    self.node = None
    if not isinstance(a, Sequence):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: Sequence[T]) -> None:
    Node = AVLTreeSet.Node
    def sort(l: int, r: int) -> Tuple[Node, int]:
      mid = (l + r) >> 1
      node = Node(a[mid])
      hl, hr = 0, 0
      if l != mid:
        node.left, hl = sort(l, mid)
        node.size += node.left.size
      if mid+1 != r:
        node.right, hr = sort(mid+1, r)
        node.size += node.right.size
      node.balance = hl - hr
      return node, max(hl, hr)+1
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(set(a))
    self.node = sort(0, len(a))[0]

  def _rotate_L(self, node: Node) -> Node:
    u = node.left
    u.size = node.size
    node.size -= 1 if u.left is None else u.left.size + 1
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
    node.size -= 1 if u.right is None else u.right.size + 1
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
    if E.right is None:
      node.size -= B.size
      B.size -= 1
    else:
      node.size -= B.size - E.right.size
      B.size -= E.right.size + 1
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
    if D.left is None:
      node.size -= C.size
      C.size -= 1
    else:
      node.size -= C.size - D.left.size
      C.size -= D.left.size + 1
    C.left = D.right
    D.right = C
    node.right = D.left
    D.left = node
    self._update_balance(D)
    return D

  def _kth_elm(self, k: int) -> T:
    if k < 0: k += self.node.size
    node = self.node
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        return node.key
      elif t < k:
        k -= t + 1
        node = node.right
      else:
        node = node.left

  def add(self, key: T) -> bool:
    if self.node is None:
      self.node = AVLTreeSet.Node(key)
      return True
    pnode = self.node
    path = []
    di = 0
    while pnode is not None:
      if key == pnode.key:
        return False
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
      path[-1].left = AVLTreeSet.Node(key)
    else:
      path[-1].right = AVLTreeSet.Node(key)
    new_node = None
    while path:
      pnode = path.pop()
      pnode.size += 1
      pnode.balance += 1 if di & 1 else -1
      di >>= 1
      if pnode.balance == 0:
        break
      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance == -1 else self._rotate_L(pnode)
        break
      elif pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance == 1 else self._rotate_R(pnode)
        break
    if new_node is not None:
      if path:
        gnode = path.pop()
        gnode.size += 1
        if di & 1:
          gnode.left = new_node
        else:
          gnode.right = new_node
      else:
        self.node = new_node
    for p in path:
      p.size += 1
    return True

  def discard(self, key: T) -> bool:
    di = 0
    path = []
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
    if node.left is not None and node.right is not None:
      path.append(node)
      di <<= 1
      di |= 1
      lmax = node.left
      while lmax.right is not None:
        path.append(lmax)
        di <<= 1
        lmax = lmax.right
      node.key = lmax.key
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
      di >>= 1
      pnode.size -= 1
      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance == -1 else self._rotate_L(pnode)
      elif pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance == 1 else self._rotate_R(pnode)
      elif pnode.balance != 0:
        break
      if new_node is not None:
        if not path:
          self.node = new_node
          return True
        if di & 1:
          path[-1].left = new_node
        else:
          path[-1].right = new_node
        if new_node.balance != 0:
          break
    for p in path:
      p.size -= 1
    return True

  def remove(self, key: T) -> None:
    if self.discard(key):
      return
    raise KeyError(key)

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
        k += 0 if node.left is None else node.left.size
        break
      elif key < node.key:
        node = node.left
      else:
        k += 1 if node.left is None else node.left.size + 1
        node = node.right
    return k

  def index_right(self, key: T) -> int:
    k = 0
    node = self.node
    while node is not None:
      if key == node.key:
        k += 1 if node.left is None else node.left.size + 1
        break
      elif key < node.key:
        node = node.left
      else:
        k += 1 if node.left is None else node.left.size + 1
        node = node.right
    return k

  def pop(self, k: int=-1) -> T:
    assert self.node is not None, f'IndexError: {self.__class__.__name__}.pop({k}), pop({k}) from Empty {self.__class__.__name__}'
    x = self._kth_elm(k)
    self.discard(x)
    return x

  def pop_max(self) -> T:
    assert self.node is not None, f'IndexError: {self.__class__.__name__}.pop_max(), pop_max from Empty {self.__class__.__name__}'
    return self.pop()

  def pop_min(self) -> T:
    assert self.node is not None, f'IndexError: {self.__class__.__name__}.pop_min(), pop_min from Empty {self.__class__.__name__}'
    return self.pop(0)

  def get_max(self) -> Optional[T]:
    if self.node is None: return
    return self._kth_elm(-1)

  def get_min(self) -> Optional[T]:
    if self.node is None: return
    return self._kth_elm(0)

  def clear(self) -> None:
    self.node = None

  def tolist(self) -> List[T]:
    a = []
    if self.node is None:
      return a
    def rec(node):
      if node.left is not None:
        rec(node.left)  
      a.append(node.key)
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def __contains__(self, key: T) -> bool:
    node = self.node
    while node is not None:
      if key == node.key:
        return True
      elif key < node.key:
        node = node.left
      else:
        node = node.right
    return False

  def __getitem__(self, k: int) -> T:
    assert -len(self) <= k < len(self), \
        f'IndexError: {self.__class__.__name__}.__getitem__({k}), len={len(self)}'
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
    return 0 if self.node is None else self.node.size

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'AVLTreeSet({str(self)})'

