import sys
from typing import Optional, Generic, Iterable, List, TypeVar, Tuple
T = TypeVar('T')

class Node:

  def __init__(self, key, val) -> None:
    self.key = key
    self.size = 1
    self.val = val
    self.valsize = val
    self.left = None
    self.right = None

  def __str__(self) -> str:
    if self.left is None and self.right is None:
      return f'key:{self.key, self.size, self.val, self.valsize}\n'
    return f'key:{self.key, self.size, self.val, self.valsize},\n left:{self.left},\n right:{self.right}\n'

class SplayTreeMultiset(Generic[T]):

  def __init__(self, a: Iterable[T]=[]) -> None:
    self.node = None
    if not (hasattr(a, '__getitem__') and hasattr(a, '__len__')):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: Iterable[T]) -> None:
    def sort(l: int, r: int):
      mid = (l + r) >> 1
      node = Node(a[mid][0], a[mid][1])
      if l != mid:
        node.left = sort(l, mid)
      if mid+1 != r:
        node.right = sort(mid+1, r)
      self._update(node)
      return node
    a = self._rle(sorted(a))
    self.node = sort(0, len(a))

  def _rle(self, a: list) -> list:
    now = a[0]
    ret = [[now, 1]]
    for i in a[1:]:
      if i == now:
        ret[-1][1] += 1
        continue
      ret.append([i, 1])
      now = i
    return ret

  def _update(self, node: Node) -> None:
    if node.left is None:
      if node.right is None:
        node.size = 1
        node.valsize = node.val
      else:
        node.size = 1 + node.right.size
        node.valsize = node.val + node.right.valsize
    else:
      if node.right is None:
        node.size = 1 + node.left.size
        node.valsize = node.val + node.left.valsize
      else:
        node.size = 1 + node.left.size + node.right.size
        node.valsize = node.val + node.left.valsize + node.right.valsize

  def _splay(self, path: List[Node], d: int) -> Node:
    for _ in range(len(path)>>1):
      node = path.pop()
      pnode = path.pop()
      if d&1 == d>>1&1:
        if d & 1:
          tmp = node.left
          node.left = tmp.right
          tmp.right = node
          pnode.left = node.right
          node.right = pnode
        else:
          tmp = node.right
          node.right = tmp.left
          tmp.left = node
          pnode.right = node.left
          node.left = pnode
      else:
        if d & 1:
          tmp = node.left
          node.left = tmp.right
          pnode.right = tmp.left
          tmp.right = node
          tmp.left = pnode
        else:
          tmp = node.right
          node.right = tmp.left
          pnode.left = tmp.right
          tmp.left = node
          tmp.right = pnode
      self._update(pnode)
      self._update(node)
      self._update(tmp)
      if not path:
        return tmp
      d >>= 2
      if d & 1:
        path[-1].left = tmp
      else:
        path[-1].right = tmp
    gnode = path[0]
    if d & 1:
      node = gnode.left
      gnode.left = node.right
      node.right = gnode
    else:
      node = gnode.right
      gnode.right = node.left
      node.left = gnode
    self._update(gnode)
    self._update(node)
    return node

  def _set_search_splay(self, key: T) -> None:
    node = self.node
    if node is None or node.key == key:
      return
    path = []
    d = 0
    while True:
      if node.key == key:
        break
      elif key < node.key:
        if node.left is None:
          break
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        if node.right is None:
          break
        path.append(node)
        d <<= 1
        node = node.right
    if path:
      self.node = self._splay(path, d)

  def _set_kth_elm_splay(self, k: int) -> None:
    if k < 0: k += self.__len__()
    d = 0
    node = self.node
    path = []
    while True:
      t = node.val if node.left is None else node.val + node.left.valsize
      if t-node.val <= k < t:
        if path:
          self.node = self._splay(path, d)
        break
      elif t > k:
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        path.append(node)
        d <<= 1
        node = node.right
        k -= t

  def _set_kth_elm_tree_splay(self, k: int) -> None:
    if k < 0:
      k += self.len_elm()
    assert 0 <= k < self.len_elm()
    d = 0
    node = self.node
    path = []
    while True:
      t = 0 if node.left is None else node.left.size
      if t == k:
        if path:
          self.node = self._splay(path, d)
        return
      elif t > k:
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        path.append(node)
        d <<= 1
        node = node.right
        k -= t + 1

  def _get_min_splay(self, node: Node) -> Node:
    if node is None or node.left is None:
      return node
    path = []
    while node.left is not None:
      path.append(node)
      node = node.left
    return self._splay(path, (1<<len(path))-1)

  def _get_max_splay(self, node: Node) -> Node:
    if node is None or node.right is None:
      return node
    path = []
    while node.right is not None:
      path.append(node)
      node = node.right
    return self._splay(path, 0)

  def add(self, key: T, val: int=1) -> None:
    if self.node is None:
      self.node = Node(key, val)
      return
    self._set_search_splay(key)
    if self.node.key == key:
      self.node.val += val
      self._update(self.node)
      return
    node = Node(key, val)
    if key < self.node.key:
      node.left = self.node.left
      node.right = self.node
      self.node.left = None
      self._update(node.right)
    else:
      node.left = self.node
      node.right = self.node.right
      self.node.right = None
      self._update(node.left)
    self._update(node)
    self.node = node
    return

  def discard(self, key: T, val: int=1) -> bool:
    if self.node is None: return False
    self._set_search_splay(key)
    if self.node.key != key: return False
    if self.node.val > val:
      self.node.val -= val
      self._update(self.node)
      return True
    if self.node.left is None:
      self.node = self.node.right
    elif self.node.right is None:
      self.node = self.node.left
    else:
      node = self._get_min_splay(self.node.right)
      node.left = self.node.left
      self._update(node)
      self.node = node
    return True

  def discard_all(self, key: T) -> bool:
    return self.discard(key, self.count(key))

  def count(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    return self.node.val if self.node.key == key else 0

  def le(self, key: T) -> Optional[T]:
    node = self.node
    if node is None: return None
    path = []
    d = 0
    res = None
    while True:
      if node.key == key:
        res = key
        break
      elif key < node.key:
        if node.left is None:
          break
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        res = node.key
        if node.right is None:
          break
        path.append(node)
        d <<= 1
        node = node.right
    if path:
      self.node = self._splay(path, d)
    return res

  def lt(self, key: T) -> Optional[T]:
    node = self.node
    path = []
    d = 0
    res = None
    while node is not None:
      if key <= node.key:
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        path.append(node)
        d <<= 1
        res = node.key
        node = node.right
    else:
      if path:
        path.pop()
        d >>= 1
    if path:
      self.node = self._splay(path, d)
    return res

  def ge(self, key: T) -> Optional[T]:
    node = self.node
    if node is None: return None
    path = []
    d = 0
    res = None
    while True:
      if node.key == key:
        res = node.key
        break
      elif key < node.key:
        res = node.key
        if node.left is None:
          break
        path.append(node)
        d <<= 1
        d |= 1
        node = node.left
      else:
        if node.right is None:
          break
        path.append(node)
        d <<= 1
        node = node.right
    if path:
      self.node = self._splay(path, d)
    return res

  def gt(self, key: T) -> Optional[T]:
    node = self.node
    path = []
    d = 0
    res = None
    while node is not None:
      if key < node.key:
        path.append(node)
        d <<= 1
        d |= 1
        res = node.key
        node = node.left
      else:
        path.append(node)
        d <<= 1
        node = node.right
    else:
      if path:
        path.pop()
        d >>= 1
    if path:
      self.node = self._splay(path, d)
    return res

  def index(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.valsize
    if self.node.key < key:
      res += self.node.val
    return res

  def index_right(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.valsize
    if self.node.key <= key:
      res += self.node.val
    return res

  def index_keys(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.size
    if self.node.key < key:
      res += 1
    return res

  def index_right_keys(self, key: T) -> int:
    if self.node is None: return 0
    self._set_search_splay(key)
    res = 0 if self.node.left is None else self.node.left.size
    if self.node.key <= key:
      res += 1
    return res

  def pop(self, k: int=-1) -> T:
    self._set_kth_elm_splay(k)
    res = self.node.key
    self.discard(res)
    return res

  def pop_min(self) -> T:
    return self.pop(0)

  def tolist(self) -> List[T]:
    a = []
    if self.node is None:
      return a
    if sys.getrecursionlimit() < self.len_elm():
      sys.setrecursionlimit(self.len_elm()+1)
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
    if sys.getrecursionlimit() < self.len_elm():
      sys.setrecursionlimit(self.len_elm()+1)
    def rec(node):
      if node.left is not None:
        rec(node.left)
      a.append((node.key, node.val))
      if node.right is not None:
        rec(node.right)
    rec(self.node)
    return a

  def get_elm(self, k: int) -> T:
    self._set_kth_elm_tree_splay(k)
    return self.node.key

  def items(self):
    for i in range(self.len_elm()):
      self._set_kth_elm_tree_splay(i)
      yield self.node.key, self.node.val

  def keys(self):
    for i in range(self.len_elm()):
      self._set_kth_elm_tree_splay(i)
      yield self.node.key

  def values(self):
    for i in range(self.len_elm()):
      self._set_kth_elm_tree_splay(i)
      yield self.node.val

  def len_elm(self) -> int:
    return 0 if self.node is None else self.node.size

  def show(self) -> None:
    print('{' + ', '.join(map(lambda x: f'{x[0]}: {x[1]}', self.tolist_items())) + '}')

  def clear(self) -> None:
    self.node = None

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

  def __contains__(self, key: T) -> bool:
    self._set_search_splay(key)
    return self.node is not None and self.node.key == key

  def __getitem__(self, p) -> T:
    self._set_kth_elm_splay(p)
    return self.node.key

  def __len__(self):
    return 0 if self.node is None else self.node.valsize

  def __bool__(self):
    return self.node is not None

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return 'SplayTreeMultiset(' + str(self) + ')'


