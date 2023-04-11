from array import array
from __pypy__ import newlist_hint
from typing import Optional, Generic, Iterable, List, TypeVar
T = TypeVar('T')

class SplayTreeSetTopDown(Generic[T]):

  def __init__(self, a: Iterable[T]=[], e: T=0):
    self.keys: List[T] = [e]
    self.size = array('I', bytes(4))
    self.child = array('I', bytes(8))
    self.end = 1
    self.node = 0
    self.len = 0
    self.e = 0
    if not isinstance(a, list):
      a = list(a)
    if a:
      self._build(a)

  def _build(self, a: List[T]) -> None:
    def sort(l: int, r: int) -> int:
      mid = (l + r) >> 1
      if l != mid:
        child[mid<<1] = sort(l, mid)
      if mid + 1 != r:
        child[mid<<1|1] = sort(mid+1, r)
      size[mid] = 1 + size[child[mid<<1]] + size[child[mid<<1|1]]
      return mid
    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
      a = sorted(set(a))
    n = len(a)
    key, child, size = self.keys, self.child, self.size
    self.reserve(n-len(key)+2)
    self.end += n
    key[1:n+1] = a
    self.node = sort(1, n+1)
    self.len = n

  def _make_node(self, key: T) -> int:
    if self.end >= len(self.keys):
      self.keys.append(key)
      self.size.append(1)
      self.child.append(0)
      self.child.append(0)
    else:
      self.keys[self.end] = key
    self.end += 1
    return self.end - 1

  def _set_search_splay(self, key: T) -> None:
    node = self.node
    keys, child = self.keys, self.child
    if (not node) or keys[node] == key: return
    left, right = 0, 0
    while keys[node] != key:
      if key < keys[node]:
        if not child[node<<1]: break
        if key < keys[child[node<<1]]:
          new = child[node<<1]
          child[node<<1] = child[new<<1|1]
          child[new<<1|1] = node
          node = new
          if not child[node<<1]: break
        child[right<<1] = node
        right = node
        node = child[node<<1]
      else:
        if not child[node<<1|1]: break
        if key > keys[child[node<<1|1]]:
          new = child[node<<1|1]
          child[node<<1|1] = child[new<<1]
          child[new<<1] = node
          node = new
          if not child[node<<1|1]: break
        child[left<<1|1] = node
        left = node
        node = child[node<<1|1]
    child[right<<1] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    self.node = node

  def _get_min_splay(self, node: int) -> int:
    keys, child = self.keys, self.child
    if (not node) or (not child[node<<1]): return node
    right = 0
    while child[node<<1]:
      new = child[node<<1]
      child[node<<1] = child[new<<1|1]
      child[new<<1|1] = node
      node = new
      if not child[node<<1]: break
      child[right<<1] = node
      right = node
      node = child[node<<1]
    child[right<<1] = child[node<<1|1]
    child[1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    return node

  def _get_max_splay(self, node: int) -> int:
    keys, child = self.keys, self.child
    if (not node) or (not child[node<<1|1]): return node
    left = 0
    while child[node<<1|1]:
      new = child[node<<1|1]
      child[node<<1|1] = child[new<<1]
      child[new<<1] = node
      node = new
      if not child[node<<1|1]: break
      child[left<<1|1] = node
      left = node
      node = child[node<<1|1]
    child[0] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    return node

  def reserve(self, n: int) -> None:
    assert n >= 0, f'ValueError'
    self.keys += [self.e] * n
    self.size += array('I', [1] * n)
    self.child += array('I', bytes(8 * n))

  def add(self, key: T) -> bool:
    if not self.node:
      self.node = self._make_node(key)
      self.len += 1
      return True
    keys, child = self.keys, self.child
    self._set_search_splay(key)
    if keys[self.node] == key:
      return False
    node = self._make_node(key)
    f = key > keys[self.node]
    child[node<<1|f] = child[self.node<<1|f]
    child[node<<1|f^1] = self.node
    child[self.node<<1|f] = 0
    self.node = node
    self.len += 1
    return True

  def discard(self, key: T) -> bool:
    if not self.node: return False
    self._set_search_splay(key)
    keys, child = self.keys, self.child
    if keys[self.node] != key: return False
    if not child[self.node<<1]:
      self.node = child[self.node<<1|1]
    elif not child[self.node<<1|1]:
      self.node = child[self.node<<1]
    else:
      node = self._get_min_splay(child[self.node<<1|1])
      child[node<<1] = child[self.node<<1]
      self.node = node
    self.len -= 1
    return True

  def ge(self, key: T) -> Optional[T]:
    node = self.node
    if not node: return None
    keys, child = self.keys, self.child
    if keys[node] == key: return key
    ge = None
    left, right = 0, 0
    while True:
      if keys[node] == key:
        ge = key
        break
      if key < keys[node]:
        ge = keys[node]
        if not child[node<<1]: break
        if key < keys[child[node<<1]]:
          new = child[node<<1]
          child[node<<1] = child[new<<1|1]
          child[new<<1|1] = node
          node = new
          ge = keys[node]
          if not child[node<<1]: break
        child[right<<1] = node
        right = node
        node = child[node<<1]
      else:
        if not child[node<<1|1]: break
        if key > keys[child[node<<1|1]]:
          new = child[node<<1|1]
          child[node<<1|1] = child[new<<1]
          child[new<<1] = node
          node = new
          if not child[node<<1|1]: break
        child[left<<1|1] = node
        left = node
        node = child[node<<1|1]
    child[right<<1] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    self.node = node
    return ge

  def gt(self, key: T) -> Optional[T]:
    node = self.node
    if not node: return None
    gt = None
    keys, child = self.keys, self.child
    left, right = 0, 0
    while True:
      if key < keys[node]:
        gt = keys[node]
        if not child[node<<1]: break
        if key < keys[child[node<<1]]:
          new = child[node<<1]
          child[node<<1] = child[new<<1|1]
          child[new<<1|1] = node
          node = new
          gt = keys[node]
          if not child[node<<1]: break
        child[right<<1] = node
        right = node
        node = child[node<<1]
      else:
        if not child[node<<1|1]: break
        if key > keys[child[node<<1|1]]:
          new = child[node<<1|1]
          child[node<<1|1] = child[new<<1]
          child[new<<1] = node
          node = new
          if not child[node<<1|1]: break
        child[left<<1|1] = node
        left = node
        node = child[node<<1|1]
    child[right<<1] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    self.node = node
    return gt

  def le(self, key: T) -> Optional[T]:
    node = self.node
    if not node: return None
    keys, child = self.keys, self.child
    if keys[node] == key: return key
    le = None
    left, right = 0, 0
    while True:
      if keys[node] == key:
        le = key
        break
      if key < keys[node]:
        if not child[node<<1]: break
        if key < keys[child[node<<1]]:
          new = child[node<<1]
          child[node<<1] = child[new<<1|1]
          child[new<<1|1] = node
          node = new
          if not child[node<<1]: break
        child[right<<1] = node
        right = node
        node = child[node<<1]
      else:
        le = keys[node]
        if not child[node<<1|1]: break
        if key > keys[child[node<<1|1]]:
          new = child[node<<1|1]
          child[node<<1|1] = child[new<<1]
          child[new<<1] = node
          node = new
          le = keys[node]
          if not child[node<<1|1]: break
        child[left<<1|1] = node
        left = node
        node = child[node<<1|1]
    child[right<<1] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    self.node = node
    return le

  def lt(self, key: T) -> Optional[T]:
    node = self.node
    if not node: return None
    lt = None
    keys, child = self.keys, self.child
    left, right = 0, 0
    while True:
      if key <= keys[node]:
        if not child[node<<1]: break
        if key < keys[child[node<<1]]:
          new = child[node<<1]
          child[node<<1] = child[new<<1|1]
          child[new<<1|1] = node
          node = new
          if not child[node<<1]: break
        child[right<<1] = node
        right = node
        node = child[node<<1]
      else:
        lt = keys[node]
        if not child[node<<1|1]: break
        if key > keys[child[node<<1|1]]:
          new = child[node<<1|1]
          child[node<<1|1] = child[new<<1]
          child[new<<1] = node
          node = new
          lt = keys[node]
          if not child[node<<1|1]: break
        child[left<<1|1] = node
        left = node
        node = child[node<<1|1]
    child[right<<1] = child[node<<1|1]
    child[left<<1|1] = child[node<<1]
    child[node<<1] = child[1]
    child[node<<1|1] = child[0]
    self.node = node
    return lt

  def tolist(self) -> List[T]:
    node = self.node
    child, keys = self.child, self.keys
    stack, res = newlist_hint(len(self)), newlist_hint(len(self))
    while stack or node:
      if node:
        stack.append(node)
        node = child[node<<1]
      else:
        node = stack.pop()
        res.append(keys[node])
        node = child[node<<1|1]
    return res

  def get_max(self) -> T:
    assert self.node, 'IndexError: get_max() from empty SplayTreeSetTopDown'
    self.node = self._get_max_splay(self.node)
    return self.keys[self.node]

  def get_min(self) -> T:
    assert self.node, 'IndexError: get_min() from empty SplayTreeSetTopDown'
    self.node = self._get_min_splay(self.node)
    return self.keys[self.node]

  def pop_max(self) -> T:
    assert self.node, 'IndexError: pop_max() from empty SplayTreeSetTopDown'
    node = self._get_max_splay(self.node)
    self.node = self.child[node<<1]
    return self.keys[node]

  def pop_min(self) -> T:
    assert self.node, 'IndexError: pop_min() from empty SplayTreeSetTopDown'
    node = self._get_min_splay(self.node)
    self.node = self.child[node<<1|1]
    return self.keys[node]

  def __contains__(self, key: T):
    self._set_search_splay(key)
    return self.keys[self.node] == key

  def __len__(self):
    return self.len

  def __bool__(self):
    return self.node != 0

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'SplayTreeSetTopDown({self})'

