from Library_py.DataStructures.BitVector.BitVectorInterface import BitVectorInterface
from array import array
from typing import Iterable, List, Sequence
from __pypy__ import newlist_hint

class AVLTreeBitVector(BitVectorInterface):

  @staticmethod
  def _popcount(x: int) -> int:
    x = x - ((x >> 1) & 0x55555555)
    x = (x & 0x33333333) + ((x >> 2) & 0x33333333)
    x = x + (x >> 4) & 0x0f0f0f0f
    x += x >> 8
    x += x >> 16
    return x & 0x0000007f

  def __init__(self, a: Iterable[int]=[]):
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

  def _build(self, a: Iterable[int]) -> None:
    key, bit_len, left, right, size, balance, total = self.key, self.bit_len, self.left, self.right, self.size, self.balance, self.total
    _popcount = AVLTreeBitVector._popcount
    def rec(lr: int) -> int:
      l, r = lr>>bit, lr&msk
      mid = (l + r) >> 1
      hl, hr = 0, 0
      if l != mid:
        le = rec(l<<bit|mid)
        left[mid], hl = le>>bit, le&msk
        size[mid] += size[left[mid]]
        total[mid] += total[left[mid]]
      if mid + 1 != r:
        ri = rec((mid+1)<<bit|r)
        right[mid], hr = ri>>bit, ri&msk
        size[mid] += size[right[mid]]
        total[mid] += total[right[mid]]
      balance[mid] = hl - hr
      return mid<<bit|(max(hl, hr)+1)
    if not isinstance(a, Sequence):
      a = list(a)
    n = len(a)
    bit = n.bit_length() + 2
    msk = (1 << bit) - 1
    end = self.end
    self.reserve(n)
    i = 0
    indx = end
    for i in range(0, n, self.w):
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
    self.end = indx
    self.root = rec(end<<bit|self.end)>>bit

  def _rotate_L(self, node: int) -> int:
    left, right, size, balance, total = self.left, self.right, self.size, self.balance, self.total
    u = left[node]
    size[u] = size[node]
    total[u] = total[node]
    size[node] -= size[left[u]] + self.bit_len[u]
    total[node] -= total[left[u]] + AVLTreeBitVector._popcount(self.key[u])
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
    left, right, size, balance, total = self.left, self.right, self.size, self.balance, self.total
    u = right[node]
    size[u] = size[node]
    total[u] = total[node]
    size[node] -= size[right[u]] + self.bit_len[u]
    total[node] -= total[right[u]] + AVLTreeBitVector._popcount(self.key[u])
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
    left, right, size, total = self.left, self.right, self.size, self.total
    B = left[node]
    E = right[B]
    size[E] = size[node]
    size[node] -= size[B] - size[right[E]]
    size[B] -= size[right[E]] + self.bit_len[E]
    total[E] = total[node]
    total[node] -= total[B] - total[right[E]]
    total[B] -= total[right[E]] + AVLTreeBitVector._popcount(self.key[E])
    right[B] = left[E]
    left[E] = B
    left[node] = right[E]
    right[E] = node
    self._update_balance(E)
    return E

  def _rotate_RL(self, node: int) -> int:
    left, right, size, total = self.left, self.right, self.size, self.total
    C = right[node]
    D = left[C]
    size[D] = size[node]
    size[node] -= size[C] - size[left[D]]
    size[C] -= size[left[D]] + self.bit_len[D]
    total[D] = total[node]
    total[node] -= total[C] - total[left[D]]
    total[C] -= total[left[D]] + AVLTreeBitVector._popcount(self.key[D])
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
      if t - bit_len[node] < r <= t:
        r -= size[left[node]]
        s += total[left[node]] + AVLTreeBitVector._popcount(key[node] >> (bit_len[node] - r))
        break
      if t > r:
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
      if t - bit_len[node] <= k <= t:
        break
      d <<= 1
      size[node] += 1
      total[node] += key
      path.append(node)
      node = left[node] if t > k else right[node]
      if t > k:
        d |= 1
      else:
        k -= t
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
    bl = self.w - k
    v = (((v >> bl) << 1 | key) << bl) | (v & ((1<<bl)-1))
    left_key = v >> self.w
    left_key_popcount = left_key & 1
    keys[node] = v & ((1 << self.w) - 1)
    node = left[node]
    d <<= 1
    d |= 1
    if not node:
      if bit_len[path[-1]] < self.w:
        bit_len[path[-1]] += 1
        keys[path[-1]] = (keys[path[-1]] << 1) | left_key
        return
      else:
        left[path[-1]] = self._make_node(left_key, 1)
    else:
      path.append(node)
      size[node] += 1
      total[node] += left_key_popcount
      d <<= 1
      while right[node]:
        node = right[node]
        path.append(node)
        size[node] += 1
        total[node] += left_key_popcount
        d <<= 1
      if bit_len[node] < self.w:
        bit_len[node] += 1
        keys[node] = (keys[node] << 1) | left_key
        return
      else:
        right[node] = self._make_node(left_key, 1)
    new_node = 0
    while path:
      node = path.pop()
      balance[node] += 1 if d & 1 else -1
      d >>= 1
      if balance[node] == 0:
        break
      if balance[node] == 2:
        new_node = self._rotate_LR(node) if balance[left[node]] == -1 else self._rotate_L(node)
        break
      elif balance[node] == -2:
        new_node = self._rotate_RL(node) if balance[right[node]] == 1 else self._rotate_R(node)
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
    assert 0 <= k < len(self)
    left, right, size = self.left, self.right, self.size
    bit_len, balance, keys, total = self.bit_len, self.balance, self.key, self.total
    node = self.root
    d = 0
    path = []
    while node:
      t = size[left[node]] + bit_len[node]
      if t - bit_len[node] <= k < t:
        break
      path.append(node)
      node = left[node] if t > k else right[node]
      d <<= 1
      if t > k:
        d |= 1
      else:
        k -= t
    k -= size[left[node]]
    v = keys[node]
    res = v >> (bit_len[node] - k - 1) & 1
    if bit_len[node] == 1:
      self._pop_under(path, d, node, res)
      return res
    keys[node] = ((v >> (bit_len[node]-k)) << ((bit_len[node]-k-1))) | (v & ((1<<(bit_len[node]-k-1))-1))
    bit_len[node] -= 1
    size[node] -= 1
    total[node] -= res
    for p in path:
      size[p] -= 1
      total[p] -= res
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

  def _insert_and_rank1(self, k: int, key: int) -> int:
    if self.root == 0:
      self.root = self._make_node(key, 1)
      return 0
    left, right, size, bit_len, balance, keys, total = self.left, self.right, self.size, self.bit_len, self.balance, self.key, self.total
    node = self.root
    s = 0
    path = []
    d = 0
    while node:
      t = size[left[node]] + bit_len[node]
      if t - bit_len[node] <= k <= t:
        break
      if t <= k:
        s += total[left[node]] + AVLTreeBitVector._popcount(keys[node])
      d <<= 1
      size[node] += 1
      total[node] += key
      path.append(node)
      node = left[node] if t > k else right[node]
      if t > k:
        d |= 1
      else:
        k -= t
    k -= size[left[node]]
    s += total[left[node]] + AVLTreeBitVector._popcount(keys[node] >> (bit_len[node] - k))
    if bit_len[node] < self.w:
      v = keys[node]
      bl = bit_len[node] - k
      keys[node] = (((v >> bl) << 1 | key) << bl) | (v & ((1<<bl)-1))
      bit_len[node] += 1
      size[node] += 1
      total[node] += key
      return s
    path.append(node)
    size[node] += 1
    total[node] += key
    v = keys[node]
    bl = self.w - k
    v = (((v >> bl) << 1 | key) << bl) | (v & ((1<<bl)-1))
    left_key = v >> self.w
    left_key_popcount = left_key & 1
    keys[node] = v & ((1 << self.w) - 1)
    node = left[node]
    d <<= 1
    d |= 1
    if not node:
      if bit_len[path[-1]] < self.w:
        bit_len[path[-1]] += 1
        keys[path[-1]] = (keys[path[-1]] << 1) | left_key
        return s
      else:
        left[path[-1]] = self._make_node(left_key, 1)
    else:
      path.append(node)
      size[node] += 1
      total[node] += left_key_popcount
      d <<= 1
      while right[node]:
        node = right[node]
        path.append(node)
        size[node] += 1
        total[node] += left_key_popcount
        d <<= 1
      if bit_len[node] < self.w:
        bit_len[node] += 1
        keys[node] = (keys[node] << 1) | left_key
        return s
      else:
        right[node] = self._make_node(left_key, 1)
    new_node = 0
    while path:
      node = path.pop()
      balance[node] += 1 if d & 1 else -1
      d >>= 1
      if balance[node] == 0:
        break
      if balance[node] == 2:
        new_node = self._rotate_LR(node) if balance[left[node]] == -1 else self._rotate_L(node)
        break
      elif balance[node] == -2:
        new_node = self._rotate_RL(node) if balance[right[node]] == 1 else self._rotate_R(node)
        break
    if new_node:
      if path:
        if d & 1:
          left[path[-1]] = new_node
        else:
          right[path[-1]] = new_node
      else:
        self.root = new_node
    return s

  def _access_pop_and_rank1(self, k: int) -> int:
    assert 0 <= k < len(self)
    left, right, size = self.left, self.right, self.size
    bit_len, balance, keys, total = self.bit_len, self.balance, self.key, self.total
    s = 0
    node = self.root
    d = 0
    path = []
    while node:
      t = size[left[node]] + bit_len[node]
      if t - bit_len[node] <= k < t:
        break
      if t <= k:
        s += total[left[node]] + AVLTreeBitVector._popcount(keys[node])
      path.append(node)
      node = left[node] if t > k else right[node]
      d <<= 1
      if t > k:
        d |= 1
      else:
        k -= t
    k -= size[left[node]]
    s += total[left[node]] + AVLTreeBitVector._popcount(keys[node] >> (bit_len[node] - k))
    v = keys[node]
    res = v >> (bit_len[node] - k - 1) & 1
    if bit_len[node] == 1:
      self._pop_under(path, d, node, res)
      return s << 1 | res
    keys[node] = ((v >> (bit_len[node]-k)) << ((bit_len[node]-k-1))) | (v & ((1<<(bit_len[node]-k-1))-1))
    bit_len[node] -= 1
    size[node] -= 1
    total[node] -= res
    for p in path:
      size[p] -= 1
      total[p] -= res
    return s << 1 | res

  def __getitem__(self, k: int) -> int:
    assert 0 <= k < len(self)
    left, right, bit_len, size, key = self.left, self.right, self.bit_len, self.size, self.key
    node = self.root
    while True:
      t = size[left[node]] + bit_len[node]
      if t - bit_len[node] <= k < t:
        k -= size[left[node]]
        return key[node] >> (bit_len[node] - k - 1) & 1
      elif t > k:
        node = left[node]
      else:
        node = right[node]
        k -= t

  def __setitem__(self, k: int, v: int):
    left, right, bit_len, size, key = self.left, self.right, self.bit_len, self.size, self.key
    assert v == 0 or v == 1, f'ValueError'
    node = self.root
    while True:
      t = size[left[node]] + bit_len[node]
      if t - bit_len[node] <= k < t:
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

