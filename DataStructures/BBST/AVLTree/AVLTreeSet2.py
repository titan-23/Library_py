from typing import Generic, Iterable, Tuple, TypeVar, Union, List
T = TypeVar('T')

class Node:
  
  def __init__(self, key):
    self.key = key
    self.left = None
    self.right = None
    self.balance = 0

  def __str__(self) -> str:
    if self.left is None and self.right is None:
      return f'key:{self.key}\n'
    return f'key:{self.key},\n left:{self.left},\n right:{self.right}\n'

class AVLTreeSet2(Generic[T]):

  def __init__(self, a: Iterable[T]=[]):  
    self.node = None
    self.len = 0
    a = sorted(set(a))
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    def sort(l: int, r: int) -> Tuple[Node, int]:
      mid = (l + r) >> 1
      node = Node(a[mid])
      h = 0
      if l != mid:
        node.left, hl = sort(l, mid)
        node.balance += hl
        h = hl
      if mid+1 != r:
        node.right, hr = sort(mid+1, r)
        node.balance -= hr
        if h < hr:
          h = hr
      return node, h+1
    self.len = len(a)
    self.node = sort(0, len(a))[0]

  def _rotate_L(self, node: Node) -> Node:
    u = node.left
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
    B.right = E.left
    E.left = B
    node.left = E.right
    E.right = node
    self._update_balance(E)
    return E

  def _rotate_RL(self, node: Node) -> Node:
    C = node.right
    D = C.left
    C.left = D.right
    D.right = C
    node.right = D.left
    D.left = node
    self._update_balance(D)
    return D

  def add(self, key: T) -> bool:
    if self.node is None:
      self.node = Node(key)
      self.len += 1
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
      path[-1].left = Node(key)
    else:
      path[-1].right = Node(key)
    new_node = None
    while path:
      pnode = path.pop()
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
        if di & 1:
          path[-1].left = new_node
        else:
          path[-1].right = new_node
      else:
        self.node = new_node
    self.len += 1
    return True

  def remove(self, key: T) -> bool:
    if self.discard(key):
      return True
    raise KeyError

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
    self.len -= 1
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
      pnode = path[-1]
      if di & 1:
        pnode.left = cnode
      else:
        pnode.right = cnode
    else:
      self.node = cnode
      return True
    while path:
      new_node = None
      pnode = path.pop()
      pnode.balance -= 1 if di & 1 else -1
      di >>= 1
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
    return True

  '''Find the largest element <= key, or None if it doesn't exist. / O(logN)'''
  def le(self, key: T) -> Union[T, None]:
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

  '''Find the largest element < key, or None if it doesn't exist. / O(logN)'''
  def lt(self, key: T) -> Union[T, None]:
    res = None
    node = self.node
    while node is not None:
      if key <= node.key:
        node = node.left
      else:
        res = node.key
        node = node.right
    return res

  '''Find the smallest element >= key, or None if it doesn't exist. / O(logN)'''
  def ge(self, key: T) -> Union[T, None]:
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

  '''Find the smallest element > key, or None if it doesn't exist. / O(logN)'''
  def gt(self, key: T) -> Union[T, None]:
    res = None
    node = self.node
    while node is not None:
      if key < node.key:
        res = node.key
        node = node.left
      else:
        node = node.right
    return res

  def pop(self) -> T:
    path = []
    node = self.node
    while node.right is not None:
      path.append(node)
      node = node.right
    res = node.key
    self.len -= 1
    cnode = node.right if node.left is None else node.left
    if path:
      path[-1].right = cnode
    else:
      self.node = cnode
      return res
    while path:
      new_node = None
      pnode = path.pop()
      pnode.balance += 1
      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance == -1 else self._rotate_L(pnode)
      elif pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance == 1 else self._rotate_R(pnode)
      elif pnode.balance != 0:
        break
      if new_node is not None:
        if not path:
          self.node = new_node
          return res
        path[-1].right = new_node
        if new_node.balance != 0:
          break
    return res

  def pop_min(self) -> T:
    path = []
    node = self.node
    while node.left is not None:
      path.append(node)
      node = node.left
    res = node.key
    self.len -= 1
    cnode = node.right if node.left is None else node.left
    if path:
      path[-1].left = cnode
    else:
      self.node = cnode
      return res
    while path:
      new_node = None
      pnode = path.pop()
      pnode.balance -= 1
      if pnode.balance == 2:
        new_node = self._rotate_LR(pnode) if pnode.left.balance == -1 else self._rotate_L(pnode)
      elif pnode.balance == -2:
        new_node = self._rotate_RL(pnode) if pnode.right.balance == 1 else self._rotate_R(pnode)
      elif pnode.balance != 0:
        break
      if new_node is not None:
        if not path:
          self.node = new_node
          return res
        path[-1].left = new_node
        if new_node.balance != 0:
          break
    return res

  def get_min(self) -> T:
    node = self.node
    while node.left is not None:
      node = node.left
    return node.key

  def get_max(self) -> T:
    node = self.node
    while node.right is not None:
      node = node.right
    return node.key

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

  def __getitem__(self, k):  # 先頭と末尾しか対応していない
    if k == -1 or k == self.len-1:
      return self.get_max()
    elif k == 0:
      return self.get_min()
    raise IndexError

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

  def __len__(self):
    return self.len

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return 'AVLTreeSet2(' + str(self) + ')'


