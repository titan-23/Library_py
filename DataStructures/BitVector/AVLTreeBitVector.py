from array import array
from typing import Tuple, List, Iterable
from __pypy__ import newlist_hint

class AVLTreeBitVector():

  def __init__(self, a: Iterable[int]):
    self.root = 0
    self.bit_len = array('B', bytes(1))
    self.key = array('I', bytes(4))
    self.size = array('I', bytes(4))
    self.total = array('I', bytes(4))
    self.left = array('I', bytes(4))
    self.right = array('I', bytes(4))
    self.balance = array('b', bytes(1))
    self.end = 1
    self.w = 32
    if a:
      self._build(a)

  def reserve(self, n: int) -> None:
    n = n // self.w + 1
    a = array('I', bytes(4 * n))
    self.bit_len += array('B', bytes(n))
    self.key += a
    self.size += a
    self.total += a
    self.left += a
    self.right += a
    self.balance += array('b', bytes(n))

  @staticmethod
  def _popcount(x: int) -> int:
    x = x - ((x >> 1) & 0x55555555)
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
    x = x + (x >> 4) & 0x0f0f0f0f
    x = x + (x >> 8)
    x = x + (x >> 16)
    return x & 0x0000007f

  def _build(self, a: Iterable[int]) -> None:
    key, bit_len, left, right, size, balance, total = self.key, self.bit_len, self.left, self.right, self.size, self.balance, self.total
    _popcount = AVLTreeBitVector._popcount
    def sort(l: int, r: int) -> Tuple[int, int]:
      mid = (l + r) >> 1
      if l != mid:
        left[mid], hl = sort(l, mid)
        size[mid] += size[left[mid]]
        total[mid] += total[left[mid]]
      else:
        hl = 0
      if mid + 1 != r:
        right[mid], hr = sort(mid+1, r)
        size[mid] += size[right[mid]]
        total[mid] += total[right[mid]]
      else:
        hr = 0
      balance[mid] = hl - hr
      return mid, max(hl, hr)+1
    if not isinstance(a, list):
      a = list(a)
    n = len(a)
    end = self.end
    self.reserve(n)
    i = 0
    indx = end
    while i < n:
      j = 0
      v = 0
      while j < self.w and i + j < n:
        v <<= 1
        v |= a[i+j]
        j += 1
      key[indx] = v
      bit_len[indx] = j
      size[indx] = j
      total[indx] = _popcount(v)
      indx += 1
      i += self.w
    self.end = indx
    self.root = sort(end, self.end)[0]

  def _rotate_L(self, node: int) -> int:
    left, right, size, balance, total, key = self.left, self.right, self.size, self.balance, self.total, self.key
    u = left[node]
    size[u] = size[node]
    total[u] = total[node]
    size[node] -= size[left[u]] + self.bit_len[u]
    total[node] -= total[left[u]] + AVLTreeBitVector._popcount(key[u])
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
    left, right, size, balance, total, key = self.left, self.right, self.size, self.balance, self.total, self.key
    u = right[node]
    size[u] = size[node]
    total[u] = total[node]
    size[node] -= size[right[u]] + self.bit_len[u]
    total[node] -= total[right[u]] + AVLTreeBitVector._popcount(key[u])
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
    left, right, size, total, key = self.left, self.right, self.size, self.total, self.key
    B = left[node]
    E = right[B]
    size[E] = size[node]
    size[node] -= size[B] - size[right[E]]
    size[B] -= size[right[E]] + self.bit_len[E]
    total[E] = total[node]
    total[node] -= total[B] - total[right[E]]
    total[B] -= total[right[E]] + AVLTreeBitVector._popcount(key[E])
    right[B] = left[E]
    left[E] = B
    left[node] = right[E]
    right[E] = node
    self._update_balance(E)
    return E

  def _rotate_RL(self, node: int) -> int:
    left, right, size, total, key = self.left, self.right, self.size, self.total, self.key
    C = right[node]
    D = left[C]
    size[D] = size[node]
    size[node] -= size[C] - size[left[D]]
    size[C] -= size[left[D]] + self.bit_len[D]
    total[D] = total[node]
    total[node] -= total[C] - total[left[D]]
    total[C] -= total[left[D]] + AVLTreeBitVector._popcount(key[D])
    left[C] = right[D]
    right[D] = C
    right[node] = left[D]
    left[D] = node
    self._update_balance(D)
    return D

  def _pref(self, r: int) -> int:
    left, right, bit_len, size, key, total = self.left, self.right, self.bit_len, self.size, self.key, self.total
    node = self.root
    s = 0
    while r > 0:
      t = size[left[node]] + bit_len[node]
      if size[left[node]] < r <= t:
        r -= size[left[node]]
        s += total[left[node]] + AVLTreeBitVector._popcount(key[node] >> (bit_len[node] - r))
        break
      elif t > r:
        node = left[node]
      else:
        s += total[left[node]] + AVLTreeBitVector._popcount(key[node])
        node = right[node]
        r -= t
    return s

  def _make_node(self, key: int, bit_len: int) -> int:
    end = self.end
    if end >= len(self.key):
      self.key.append(key)
      self.bit_len.append(bit_len)
      self.size.append(bit_len)
      self.total.append(AVLTreeBitVector._popcount(key))
      self.left.append(0)
      self.right.append(0)
      self.balance.append(0)
    else:
      self.key[end] = key
      self.bit_len[end] = bit_len
      self.size[end] = bit_len
      self.total[end] = AVLTreeBitVector._popcount(key)
    self.end += 1
    return end

  def insert(self, k: int, key: int) -> None:
    if self.root == 0:
      self.root = self._make_node(key, 1)
      return
    left, right, size, bit_len, balance, keys, total = self.left, self.right, self.size, self.bit_len, self.balance, self.key, self.total
    node = self.root
    path = []
    d = 0
    while node:
      t = size[left[node]] + bit_len[node]
      if size[left[node]] <= k <= t:
        break
      d <<= 1
      size[node] += 1
      total[node] += key
      path.append(node)
      if t > k:
        d |= 1
        node = left[node]
      else:
        k -= t
        node = right[node]
    k -= size[left[node]]
    if bit_len[node] < self.w:
      v = keys[node]
      bl = bit_len[node] - k
      keys[node] = (((v >> bl) << 1 | key) << bl) | (v & ((1<<bl)-1))
      bit_len[node] += 1
      size[node] += 1
      total[node] += key
      return
    path.append(node)
    size[node] += 1
    total[node] += key
    v = keys[node]
    bl = bit_len[node] - k
    v = (((v >> bl) << 1 | key) << bl) | (v & ((1<<bl)-1))
    left_key = v >> (self.w//2)
    left_key_popcount = AVLTreeBitVector._popcount(left_key)
    keys[node] = v & ((1 << (self.w // 2)) - 1)
    bit_len[node] = self.w//2
    node = left[node]
    d <<= 1
    d |= 1
    if not node:
      if bit_len[path[-1]] + self.w//2+1 <= self.w:
        bit_len[path[-1]] += self.w//2+1
        keys[path[-1]] = (keys[path[-1]] << (self.w//2+1)) | left_key
        return
      else:
        left[path[-1]] = self._make_node(left_key, (self.w//2+1))
    else:
      path.append(node)
      size[node] += (self.w//2+1)
      total[node] += left_key_popcount
      d <<= 1
      while right[node]:
        node = right[node]
        path.append(node)
        size[node] += (self.w//2+1)
        total[node] += left_key_popcount
        d <<= 1
      if bit_len[path[-1]] + self.w//2+1 <= self.w:
        bit_len[path[-1]] += self.w//2+1
        keys[path[-1]] = (keys[path[-1]] << (self.w//2+1)) | left_key
        return
      else:
        right[node] = self._make_node(left_key, self.w//2+1)
    new_node = 0
    while path:
      pnode = path.pop()
      balance[pnode] += 1 if d & 1 else -1
      d >>= 1
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
        if d & 1:
          left[path[-1]] = new_node
        else:
          right[path[-1]] = new_node
      else:
        self.root = new_node

  def _pop_under(self, path: List[int], d: int, node: int, res: int) -> None:
    left, right, size, bit_len, balance, keys, total = self.left, self.right, self.size, self.bit_len, self.balance, self.key, self.total
    fd, lmax_total, lmax_bit_len = 0, 0, 0
    if left[node] and right[node]:
      path.append(node)
      d <<= 1
      d |= 1
      lmax = left[node]
      while right[lmax]:
        path.append(lmax)
        d <<= 1
        fd <<= 1
        fd |= 1
        lmax = right[lmax]
      lmax_total = AVLTreeBitVector._popcount(keys[lmax])
      lmax_bit_len = bit_len[lmax]
      keys[node] = keys[lmax]
      bit_len[node] = lmax_bit_len
      node = lmax
    cnode = right[node] if left[node] == 0 else left[node]
    if path:
      if d & 1:
        left[path[-1]] = cnode
      else:
        right[path[-1]] = cnode
    else:
      self.root = cnode
      return
    while path:
      new_node = 0
      node = path.pop()
      balance[node] -= 1 if d & 1 else -1
      size[node] -= lmax_bit_len if fd & 1 else 1
      total[node] -= lmax_total if fd & 1 else res
      d >>= 1
      fd >>= 1
      if balance[node] == 2:
        new_node = self._rotate_LR(node) if balance[left[node]] < 0 else self._rotate_L(node)
      elif balance[node] == -2:
        new_node = self._rotate_RL(node) if balance[right[node]] > 0 else self._rotate_R(node)
      elif balance[node] != 0:
        break
      if new_node:
        if not path:
          self.root = new_node
          return
        if d & 1:
          left[path[-1]] = new_node
        else:
          right[path[-1]] = new_node
        if balance[new_node] != 0:
          break
    while path:
      node = path.pop()
      size[node] -= lmax_bit_len if fd & 1 else 1
      total[node] -= lmax_total if fd & 1 else res
      fd >>= 1

  def pop(self, k: int) -> int:
    left, right, size = self.left, self.right, self.size
    bit_len, balance, keys, total = self.bit_len, self.balance, self.key, self.total
    pnode = self.root
    d = 0
    path = []
    while pnode:
      t = size[left[pnode]] + bit_len[pnode]
      if size[left[pnode]] <= k < t:
        break
      path.append(pnode)
      d <<= 1
      if t > k:
        d |= 1
        pnode = left[pnode]
      else:
        k -= t
        pnode = right[pnode]
    k -= size[left[pnode]]
    if bit_len[pnode] > 1:
      v = keys[pnode]
      res = v >> (bit_len[pnode] - k - 1) & 1
      v = ((v >> (bit_len[pnode]-k)) << ((bit_len[pnode]-k-1))) | (v & ((1<<(bit_len[pnode]-k-1))-1))
      keys[pnode] = v
      bit_len[pnode] -= 1
      size[pnode] -= 1
      total[pnode] -= res
      for p in path:
        size[p] -= 1
        total[p] -= res
      return res
    v = keys[pnode]
    res = v >> (bit_len[pnode] - k - 1) & 1
    self._pop_under(path, d, pnode, res)
    return res

  def set(self, k: int, v: int) -> None:
    self.__setitem__(k, v)

  def tolist(self) -> List[int]:
    left, right, key, bit_len = self.left, self.right, self.key, self.bit_len
    a = newlist_hint(len(self))
    if not self.root:
      return a
    def rec(node):
      if left[node]:
        rec(left[node])
      for i in range(bit_len[node]-1, -1, -1):
        a.append(key[node] >> i & 1)
      if right[node]:
        rec(right[node])
    rec(self.root)
    return a

  def tree_debug(self):
    return
    left, right = self.left, self.right
    print(f'tree_debug() $$$$$$$$$$$$$$')
    key, bit_len, size = self.key, self.bit_len, self.size
    def rec(node):
      if left[node]: print('left'); rec(left[node])
      print(f'key={key[node]}, bit_len={bit_len[node]}, size={size[node]}')
      if right[node]: print('right'); rec(right[node])
    rec(self.root)
    print()

  def debug(self) -> None:
    self.tree_debug()
    print(f'debug ##########')
    print(f'{self.root=}')
    print(f'{len(self.key)=}')
    print(f'bit_length():', [bin(x).count('1') for x in self.key])
    print(f'{self.key=}')
    print(f'{self.bit_len=}')
    print(f'{self.size=}')
    print(f'{self.total=}')
    print(f'{self.balance=}')
    print(f'{self.left=}')
    print(f'{self.right=}')

  def debug_acc(self) -> None:
    left, right = self.left, self.right
    key = self.key
    def rec(node):
      acc = self._popcount(key[node])
      if left[node]:
        acc += rec(left[node])
      if right[node]:
        acc += rec(right[node])
      if acc != self.total[node]:
        # self.debug()
        assert False, 'acc Error'
      return acc
    rec(self.root)

  def debug_height(self) -> int:
    left, right = self.left, self.right
    h = 0
    def rec(node, dep):
      nonlocal h
      h = max(h, dep)
      if left[node]:
        rec(left[node], dep+1)
      if right[node]:
        rec(right[node], dep+1)
    rec(self.root, 0)
    return h

  def access(self, k: int) -> int:
    return self.__getitem__(k)

  def rank0(self, r: int) -> int:
    # a[0, r) に含まれる 0 の個数
    return r - self._pref(r)

  def rank1(self, r: int) -> int:
    # a[0, r) に含まれる 1 の個数
    return self._pref(r)

  def rank(self, r: int, v: int) -> int:
    # a[0, r) に含まれる v の個数
    return self.rank1(r) if v else self.rank0(r)

  def select0(self, k: int) -> int:
    # k 番目の 0 のindex
    # O(log(N))
    if k < 0 or self.rank0(len(self)) <= k:
      return -1
    l, r = 0, len(self)
    while r - l > 1:
      m = (l + r) >> 1
      if m - self._pref(m) > k:
        r = m
      else:
        l = m
    return l

  def select1(self, k: int) -> int:
    # k 番目の 1 のindex
    # O(log(N))
    if k < 0 or self.rank1(len(self)) <= k:
      return -1
    l, r = 0, len(self)
    while r - l > 1:
      m = (l + r) >> 1
      if self._pref(m) > k:
        r = m
      else:
        l = m
    return l

  def select(self, k: int, v: int) -> int:
    # k 番目の v のindex
    # O(log(N))
    return self.select1(k) if v else self.select0(k)

  def __getitem__(self, k: int) -> int:
    left, right, bit_len, size, key = self.left, self.right, self.bit_len, self.size, self.key
    node = self.root
    while True:
      t = size[left[node]] + bit_len[node]
      if size[left[node]] <= k < t:
        k -= size[left[node]]
        return key[node] >> (bit_len[node] - k - 1) & 1
      elif t > k:
        node = left[node]
      else:
        node = right[node]
        k -= t

  def __setitem__(self, k: int, v: int):
    left, right, bit_len, size, key = self.left, self.right, self.bit_len, self.size, self.key
    node = self.root
    while True:
      t = size[left[node]] + bit_len[node]
      if size[left[node]] <= k < t:
        k -= size[left[node]]
        if v:
          key[node] |= 1 << k
        else:
          key[node] &= ~(1 << k)
        return
      elif t > k:
        node = left[node]
      else:
        node = right[node]
        k -= t

  def __str__(self):
    return str(self.tolist())

  def __len__(self):
    return self.size[self.root]

  def __repr__(self):
    return f'AVLTreeBitVector({self})'

