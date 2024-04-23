from typing import Generic, Iterable, TypeVar, Optional
T = TypeVar('T')

class AVLTree():

  def __init__(self):
    self.root = 0
    self.keys = []
    self.left = [0]
    self.right = [0]
    self.par = [0]
    self.size = [0]
    self.height = [0]
    self.unused_indx = []
    self.end = 1

class AVLTreeIterator():

  def __init__(self,
               tree: AVLTree,
               it: int) -> None:
    self.tree: AVLTree = tree
    self.it: int = it

  def _make_iter(self, it) -> 'AVLTreeIterator':
    return AVLTreeIterator(self.tree, it)

  def _min(self, node: int) -> int:
    while self.tree.left[node]:
      node = self.tree.left[node]
    return node

  def _max(self, node: int) -> int:
    while self.tree.right[node]:
      node = self.tree.right[node]
    return node

  def _next(self) -> Optional[int]:
    now = self.it
    pre = None
    flag = self.tree.right[now] is pre
    while self.tree.right[now] is pre:
      pre, now = now, self.tree.par[now]
    if not now:
      return None
    return now if flag and pre is self.tree.left[now] else self._min(self.tree.right[now])

  def _prev(self) -> Optional[int]:
    now, pre = self, None
    flag = self.tree.left[now] is pre
    while self.tree.left[now] is pre:
      pre, now = now, self.tree.par[now]
    if not now:
      return None
    return now if flag and pre is self.tree.right[now] else self._max(self.tree.left[now])

  def __iadd__(self, other: int) -> Optional['AVLTreeIterator']:
    node = self
    for _ in range(other):
      node = self._next(node)
    return node

  def __isub__(self, other: int) -> Optional['AVLTreeIterator']:
    node = self
    for _ in range(other):
      node = self._prev(node)
    return node

  def __add__(self, other: int) -> Optional['AVLTreeIterator']:
    node = self
    for _ in range(other):
      node = self._next(node)
    return self._make_iter(node)

  def __sub__(self, other: int) -> Optional['AVLTreeIterator']:
    node = self
    for _ in range(other):
      node = self._prev(node)
    return self._make_iter(node)

  def __str__(self) -> str:
    return f'{self.__class__.__name__}({self.key})'
  
  def __repr__(self) -> str:
    return str(self)


class AVLTreeSet(Generic[T]):

  __slots__ = ('unused_indx', 'root', 'keys', 'left', 'right', 'par', 'size', 'height', 'end', '__iter')

  def __init__(self, a: Iterable[T]=[]) -> None:
    self.root = 0
    self.keys = []
    self.left = [0]
    self.right = [0]
    self.par = [0]
    self.size = [0]
    self.height = [0]
    self.unused_indx = []
    self.end = 1
    if not isinstance(a, list):
      a = list(a)
    if a:
      self._build(a)

  def _update(self, node: int) -> None:
    self.size[node] = 1 + self.size[self.left[node]] + self.size[self.right[node]]
    self.height[node] = 1 + max(self.height[self.left[node]], self.height[self.right[node]])

  def _build(self, a: list[T]) -> None:
    left, right, par = self.left, self.right, self.par
    def build(l: int, r: int) -> int:
      mid = (l + r) >> 1
      node = mid
      if l != mid:
        left[node] = build(l, mid)
        par[left[node]] = node
      if mid + 1 != r:
        right[node] = build(mid+1, r)
        par[right[node]] = node
      self._update(node)
      return node
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

    self.keys = a
    self.left += [0] * n
    self.right += [0] * n
    self.par += [0] * n
    self.size += [1] * n
    self.height += [1] * n

    self.root = build(end, n+end)

  def _remove_balance(self, node: int) -> None:
    left, right, par, keys = self.left, self.right, self.par, self.keys
    while node:
      new_node = 0
      self._update(node)
      b = self._balance(node)
      if b == 2:
        new_node = self._rotate_LR(node) if self._balance(left[node]) == -1 else self._rotate_right(node)
      elif b == -2:
        new_node = self._rotate_RL(node) if self._balance(right[node]) == 1 else self._rotate_left(node)
      elif b != 0:
        node = par[node]
        break
      if not new_node:
        node = par[node]
        continue
      if not par[new_node]:
        self.root = new_node
        return
      node = par[new_node]
      if keys[new_node-1] < keys[node-1]:
        left[node] = new_node
      else:
        right[node] = new_node
      if self._balance(new_node) != 0:
        break
    while node:
      self._update(node)
      node = par[node]

  def _balance(self, node: int) -> int:
    return self.height[self.left[node]] - self.height[self.right[node]]

  def _add_balance(self, node: int) -> None:
    left, right, par, keys = self.left, self.right, self.par, self.keys
    new_node = 0
    while node:
      self._update(node)
      b = self._balance(node)
      if b == 0:
        node = par[node]
        break
      if b == 2:
        new_node = self._rotate_LR(node) if self._balance(left[node]) == -1 else self._rotate_right(node)
        break
      elif b == -2:
        new_node = self._rotate_RL(node) if self._balance(right[node]) == 1 else self._rotate_left(node)
        break
      node = par[node]
    if new_node:
      node = par[new_node]
      if node:
        if keys[new_node-1] < keys[node-1]:
          left[node] = new_node
        else:
          right[node] = new_node
      else:
        self.root = new_node
    while node:
      self._update(node)
      node = par[node]

  def add(self, key: T) -> bool:
    if not self.root:
      self.root = self._make_node(key)
      return True
    left, right, par, keys = self.left, self.right, self.par, self.keys
    pnode = 0
    node = self.root
    while node:
      if key == keys[node-1]:
        return False
      pnode = node
      node = left[node] if key < keys[node-1] else right[node]
    if key < keys[pnode-1]:
      left[pnode] = self._make_node(key)
      par[left[pnode]] = pnode
    else:
      right[pnode] = self._make_node(key)
      par[right[pnode]] = pnode
    self._add_balance(pnode)
    return True

  def remove_iter(self, node: int) -> None:
    left, right, par, keys = self.left, self.right, self.par, self.keys
    pnode = par[node]
    if left[node] and right[node]:
      pnode = node
      mnode = left[node]
      while right[mnode]:
        pnode = mnode
        mnode = right[mnode]
      keys[node-1] = keys[mnode-1]
      node = mnode
    self.unused_indx.append(node)
    cnode = right[node] if not left[node] else left[node]
    if cnode:
      par[cnode] = pnode
    if pnode:
      if keys[node-1] <= keys[pnode-1]:
        left[pnode] = cnode
      else:
        right[pnode] = cnode
      self._remove_balance(pnode)
    else:
      self.root = cnode

  def discard(self, key: T) -> bool:
    node = self.find_key(key)
    if not node:
      return False
    self.remove_iter(node)
    return True

  def remove(self, key: T) -> None:
    node = self.find_key(key)
    self.remove_iter(node)

  def _rotate_right(self, node: int) -> int:
    left, right, par = self.left, self.right, self.par
    u = left[node]
    par[u] = par[node]
    left[node] = right[u]
    if right[u]:
      par[right[u]] = node
    right[u] = node
    par[node] = u
    self._update(node)
    self._update(u)
    return u

  def _rotate_left(self, node) -> int:
    left, right, par = self.left, self.right, self.par
    u = right[node]
    par[u] = par[node]
    right[node] = left[u]
    if left[u]:
      par[left[u]] = node
    left[u] = node
    par[node] = u
    self._update(node)
    self._update(u)
    return u

  def _rotate_LR(self, node) -> int:
    self.left[node] = self._rotate_left(self.left[node])
    return self._rotate_right(node)

  def _rotate_RL(self, node) -> int:
    self.right[node] = self._rotate_right(self.right[node])
    return self._rotate_left(node)

  def _make_node(self, key: T) -> int:
    end = self.end
    if self.unused_indx:
      node = self.unused_indx.pop()
      self.keys[node-1] = key
      self.size[node] = 1
      self.par[node] = 0
      self.left[node] = 0
      self.right[node] = 0
      self.height[node] = 1
      return node
    if end >= len(self.size):
      self.keys.append(key)
      self.size.append(1)
      self.par.append(0)
      self.left.append(0)
      self.right.append(0)
      self.height.append(1)
    else:
      self.keys[end-1] = key
    self.end += 1
    return end

  def le(self, key: T) -> Optional[T]:
    keys, left, right = self.keys, self.left, self.right
    res = None
    node = self.root
    while node:
      if key == keys[node-1]:
        return keys[node-1]
      if key < keys[node-1]:
        node = left[node]
      else:
        res = keys[node-1]
        node = right[node]
    return res

  def lt(self, key: T) -> Optional[T]:
    keys, left, right = self.keys, self.left, self.right
    res = None
    node = self.root
    while node:
      if key <= keys[node-1]:
        node = left[node]
      else:
        res = keys[node-1]
        node = right[node]
    return res

  def ge(self, key: T) -> Optional[T]:
    keys, left, right = self.keys, self.left, self.right
    res = None
    node = self.root
    while node:
      if key == keys[node-1]:
        return keys[node-1]
      if key < keys[node-1]:
        res = keys[node-1]
        node = left[node]
      else:
        node = right[node]
    return res

  def gt(self, key: T) -> Optional[T]:
    keys, left, right = self.keys, self.left, self.right
    res = None
    node = self.root
    while node:
      if key < keys[node-1]:
        res = keys[node-1]
        node = left[node]
      else:
        node = right[node]
    return res

  def index(self, key: T) -> int:
    keys, left, right, size = self.keys, self.left, self.right, self.size
    k = 0
    node = self.root
    while node:
      if key == keys[node-1]:
        k += size[left[node]]
        break
      if key < keys[node-1]:
        node = left[node]
      else:
        k += size[left[node]] + 1
        node = right[node]
    return k

  def index_right(self, key: T) -> int:
    keys, left, right, size = self.keys, self.left, self.right, self.size
    k, node = 0, self.root
    while node:
      if key == keys[node-1]:
        k += size[left[node]] + 1
        break
      if key < keys[node-1]:
        node = left[node]
      else:
        k += size[left[node]] + 1
        node = right[node]
    return k

  def find_key(self, key: T) -> Optional[int]:
    left, right, keys = self.left, self.right, self.keys
    node = self.root
    while node:
      if key == keys[node-1]:
        return node
      node = left[node] if key < keys[node-1] else right[node]
    return None

  def find_kth(self, k: int) -> int:
    left, right, size = self.left, self.right, self.size
    node = self.root
    while True:
      t = size[left[node]]
      if t == k:
        return node
      if t < k:
        k -= t + 1
        node = right[node]
      else:
        node = left[node]

  def pop(self, k: int=-1) -> T:
    assert self.root, f'IndexError: {self.__class__.__name__}.pop({k}), pop({k}) from Empty {self.__class__.__name__}'
    node = self.find_kth(k)
    key = self.keys[node-1]
    self.remove_iter(node)
    return key

  def clear(self) -> None:
    self.root = 0

  def tolist(self) -> list[T]:
    left, right, keys = self.left, self.right, self.keys
    node = self.root
    stack, a = [], []
    while stack or node:
      if node:
        stack.append(node)
        node = left[node]
      else:
        node = stack.pop()
        a.append(keys[node-1])
        node = right[node]
    return a

  def __contains__(self, key: T) -> bool:
    return self.find_key(key) is not None

  def __getitem__(self, k: int) -> T:
    return self.keys[self.find_kth(k)-1]

  def __iter__(self):
    self.__iter = 0
    return self

  def __next__(self):
    if self.__iter == self.__len__():
      raise StopIteration
    res = self[self.__iter]
    self.__iter += 1
    return res

  def __reversed__(self):
    for i in range(self.__len__()):
      yield self[-i-1]

  def __len__(self):
    return self.size[self.root]

  def __bool__(self):
    return self.root != 0

  def __str__(self):
    return '{' + ', '.join(map(str, self.tolist())) + '}'

  def __repr__(self):
    return f'AVLTreeSet({self})'

  def check(self) -> None:
    if not self.root:
      print('height=0')
      print('check ok empty.')
      return
    # print(f'height={self.root.height}')
    def dfs(node: int):
      h = 0
      b = 0
      s = 1
      if self.left[node]:
        assert self.par[self.left[node]] == node
        assert self.keys[node-1] > self.keys[self.left[node]-1]
        dfs(self.left[node])
        h = max(h, self.height[self.left[node]])
        b += self.height[self.left[node]]
        s += self.size[self.left[node]]
      if self.right[node]:
        assert self.par[self.right[node]] == node
        assert self.keys[node-1] < self.keys[self.right[node]-1]
        dfs(self.right[node])
        h = max(h, self.height[self.right[node]])
        b -= self.height[self.right[node]]
        s += self.size[self.right[node]]
      assert self.height[node] == h+1
      assert -1 <= b <= 1, f'{b=}'
      assert self.size[node] == s
    dfs(self.root)
    # print('check ok.')


#  -----------------------  #

import sys
input = lambda: sys.stdin.readline().rstrip()

#  -----------------------  #

def pred():
  n, q = map(int, input().split())
  s = input()
  s = AVLTreeSet(i for i, c in enumerate(s) if c == '1')
  # print(s)
  for _ in range(q):
    c, k = map(int, input().split())
    if c == 0:
      # print(f'add({k})')
      s.add(k)
    elif c == 1:
      # print(f'discard({k})')
      s.discard(k)
    elif c == 2:
      print(1 if k in s else 0)
    elif c == 3:
      ans = s.ge(k)
      print(-1 if ans is None else ans)
    else:
      ans = s.le(k)
      print(-1 if ans is None else ans)
    # print(s)

def test():
  import random
  random.seed(0)
  s = AVLTreeSet(range(10))
  ts = set(s)
  Q = 10**4
  for i in range(Q):
    if i % (Q//10) == 0:
      print(f'query={i}')
    # print(len(s))
    com = random.randint(0, 50)
    x = random.randint(0, 10)
    if com <= 0:
      # insert
      print(f'add({x})')
      s.add(x)
      ts.add(x)
    else:
      # delete
      print(f'discard({x})')
      s.discard(x)
      ts.discard(x)
    print(s, ts)
    assert s.tolist() == sorted(ts)
    s.check()
  s.check()
  exit()

def data():
  q = int(input())
  s = AVLTreeSet()
  ans = []
  for _ in range(q):
    t, x = map(int, input().split())
    if t == 1:
      s.add(x)
    else:
      ans.append(s.pop(x-1))
  if ans:
    print('\n'.join(map(str, ans)))
  exit()

def wood():
  l, q = map(int, input().split())
  s = AVLTreeSet([0, l])
  for _ in range(q):
    c, x = map(int, input().split())
    if c == 1:
      s.add(x)
    else:
      print(s.gt(x) - s.lt(x))
  exit()

n = int(input())
A = list(map(lambda x: int(x)-1, input().split()))
s = AVLTreeSet(range(n))
for i in range(n):
  if i in s:
    s.discard(A[i])
a = s.tolist()
print(len(a))
print(' '.join(map(lambda x: str(x+1), a)))
exit()

# test()
wood()
data()
pred()

