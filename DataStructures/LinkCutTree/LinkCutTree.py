from array import array
from typing import Generic, List, TypeVar, Callable, Iterable, Optional, Union
T = TypeVar('T')
F = TypeVar('F')

class LinkCutTree(Generic[T, F]):

  # パスクエリ全部載せLinkCutTree
  # - link / cut / merge / split
  # - prod / apply / getitem / setitem
  # - root / same
  # - lca / path_kth_elm
  # など

  # opがいらないならupdateを即returnするように変更したり、
  # 可換opならupdateを短縮したりなど

  # opをするならeは必須 <- 場合分けしてもよさそう?
  # idは無くてもよいが、あると(strategyの問題で)速くなるため推奨

  def __init__(self, n_or_a: Union[int, Iterable[T]], \
              op: Callable[[T, T], T]=lambda x, y: None, \
              mapping: Callable[[F, T], T]=lambda x, y: None, \
              composition: Callable[[F, F], F]=lambda x, y: None, \
              e: T=None, id: F=None):
    self.op = op
    self.mapping = mapping
    self.composition = composition
    self.e = e
    self.id = id
    self.key: List[T] = [e] * (n_or_a) if isinstance(n_or_a, int) else list(n_or_a)
    self.n = len(self.key)
    self.key.append(e)
    self.data : List[T] = [x for x in self.key for _ in range(2)]
    self.lazy : List[F] = [id] * (self.n+1)
    self.arr  : array[int] = array('I', [self.n, self.n, self.n, 0] * (self.n+1))
    # node.left  : arr[node<<2|0]
    # node.right : arr[node<<2|1]
    # node.par   : arr[node<<2|2]
    # node.rev   : arr[node<<2|3]
    self.size : array[int] = array('I', [1] * (self.n+1))
    self.size[-1] = 0
    self.group_cnt = self.n

  def _is_root(self, node: int) -> bool:
    return (self.arr[node<<2|2] == self.n) or not (self.arr[self.arr[node<<2|2]<<2] == node or self.arr[self.arr[node<<2|2]<<2|1] == node)

  def _propagate(self, node: int) -> None:
    if node == self.n: return
    arr = self.arr
    if arr[node<<2|3]:
      self.data[node<<1], self.data[node<<1|1] = self.data[node<<1|1], self.data[node<<1]
      arr[node<<2|3] = 0
      ln, rn = arr[node<<2], arr[node<<2|1]
      arr[node<<2] = rn
      arr[node<<2|1] = ln
      arr[ln<<2|3] ^= 1
      arr[rn<<2|3] ^= 1
    if self.lazy[node] == self.id:
      return
    lazy, data, key = self.lazy, self.data, self.key
    nlazy = lazy[node]
    lnode, rnode = arr[node<<2], arr[node<<2|1]
    if lnode != self.n:
      data[lnode<<1] = self.mapping(nlazy, data[lnode<<1])
      data[lnode<<1|1] = self.mapping(nlazy, data[lnode<<1|1])
      key[lnode] = self.mapping(nlazy, key[lnode])
      lazy[lnode] = nlazy if lazy[lnode] == self.id else self.composition(nlazy, lazy[lnode])
    if rnode != self.n:
      data[rnode<<1] = self.mapping(nlazy, data[rnode<<1])
      data[rnode<<1|1] = self.mapping(nlazy, data[rnode<<1|1])
      key[rnode] = self.mapping(nlazy, key[rnode])
      lazy[rnode] = nlazy if lazy[rnode] == self.id else self.composition(nlazy, lazy[rnode])
    lazy[node] = self.id

  def _update(self, node: int) -> None:
    if node == self.n: return
    ln, rn = self.arr[node<<2], self.arr[node<<2|1]
    self._propagate(ln)
    self._propagate(rn)
    self.data[node<<1] = self.op(self.op(self.data[ln<<1], self.key[node]), self.data[rn<<1])
    self.data[node<<1|1] = self.op(self.op(self.data[rn<<1|1], self.key[node]), self.data[ln<<1|1])
    self.size[node] = 1 + self.size[ln] + self.size[rn]

  def _update_triple(self, x: int, y: int, z: int) -> None:
    data, key, arr, size = self.data, self.key, self.arr, self.size
    lx, rx = arr[x<<2], arr[x<<2|1]
    ly, ry = arr[y<<2], arr[y<<2|1]
    self._propagate(lx)
    self._propagate(rx)
    self._propagate(ly)
    self._propagate(ry)
    data[z<<1] = data[x<<1]
    data[x<<1] = self.op(self.op(data[lx<<1], key[x]), data[rx<<1])
    data[y<<1] = self.op(self.op(data[ly<<1], key[y]), data[ry<<1])
    data[z<<1|1] = data[x<<1|1]
    data[x<<1|1] = self.op(self.op(data[rx<<1|1], key[x]), data[lx<<1|1])
    data[y<<1|1] = self.op(self.op(data[ry<<1|1], key[y]), data[ly<<1|1])
    size[z] = size[x]
    size[x] = 1 + size[lx] + size[rx]
    size[y] = 1 + size[ly] + size[ry]

  def _update_double(self, x: int, y: int) -> None:
    data, key, arr, size = self.data, self.key, self.arr, self.size
    lx, rx = arr[x<<2], arr[x<<2|1]
    self._propagate(lx)
    self._propagate(rx)
    data[y<<1] = data[x<<1]
    data[x<<1] = self.op(self.op(data[lx<<1], key[x]), data[rx<<1])
    data[y<<1|1] = data[x<<1|1]
    data[x<<1|1] = self.op(self.op(data[rx<<1|1], key[x]), data[lx<<1|1])
    size[y] = size[x]
    size[x] = 1 + size[lx] + size[rx]

  def _splay(self, node: int) -> None:
    # splayを抜けた後、nodeは遅延伝播済みにするようにする
    # (splay後のnodeのleft,rightにアクセスしやすいと非常にラクなはず)
    if node == self.n: return
    _propagate, _is_root, _update_triple = self._propagate, self._is_root, self._update_triple
    _propagate(node)
    if _is_root(node): return
    n, arr = self.n, self.arr
    pnode = arr[node<<2|2]
    while not _is_root(pnode):
      gnode = arr[pnode<<2|2]
      _propagate(gnode)
      _propagate(pnode)
      _propagate(node)
      f = arr[pnode<<2] == node
      g = (arr[gnode<<2|f] == pnode) ^ (arr[pnode<<2|f] == node)
      nnode = (node if g else pnode) << 2 | f ^ g
      arr[pnode<<2|f^1] = arr[node<<2|f]
      arr[gnode<<2|f^g^1] = arr[nnode]
      arr[node<<2|f] = pnode
      arr[nnode] = gnode
      arr[node<<2|2] = arr[gnode<<2|2]
      arr[gnode<<2|2] = nnode>>2
      arr[arr[pnode<<2|f^1]<<2|2] = pnode
      arr[arr[gnode<<2|f^g^1]<<2|2] = gnode
      arr[pnode<<2|2] = node
      _update_triple(gnode, pnode, node)
      pnode = arr[node<<2|2]
      if arr[pnode<<2] == gnode:
        arr[pnode<<2] = node
      elif arr[pnode<<2|1] == gnode:
        arr[pnode<<2|1] = node
      else:
        return
    _propagate(pnode)
    _propagate(node)
    f = arr[pnode<<2] == node
    arr[pnode<<2|f^1] = arr[node<<2|f]
    arr[node<<2|f] = pnode
    arr[arr[pnode<<2|f^1]<<2|2] = pnode
    arr[node<<2|2] = arr[pnode<<2|2]
    arr[pnode<<2|2] = node
    self._update_double(pnode, node)

  def expose(self, v: int) -> int:
    ''' vが属する木において、その木の根->vのパスを構築
    '''
    arr, n, _splay, _update = self.arr, self.n, self._splay, self._update
    pre = v
    while arr[v<<2|2] != n:
      _splay(v)
      arr[v<<2|1] = n
      _update(v)
      if arr[v<<2|2] == n:
        break
      pre = arr[v<<2|2]
      _splay(pre)
      arr[pre<<2|1] = v
      _update(pre)
    arr[v<<2|1] = n
    _update(v)
    return pre

  def lca(self, root: int, u: int, v: int) -> int:
    self.evert(root)
    self.expose(u)
    return self.expose(v)

  def link(self, c: int, p: int) -> None:
    ''' c->pの辺を追加する / cは元の木の根でなければならない
    (元の木の根とself._is_root()はまったくの別物)
    '''
    assert not self.same(c, p)
    self.expose(c)
    self.expose(p)
    self.arr[c<<2|2] = p
    self.arr[p<<2|1] = c
    self._update(p)
    self.group_cnt -= 1

  def cut(self, c: int) -> None:
    ''' cとpar[c]の間の辺を削除する / cは元の木の根であってはいけない
    '''
    arr = self.arr
    self.expose(c)
    assert arr[c<<2] != self.n
    arr[arr[c<<2]<<2|2] = self.n
    arr[c<<2] = self.n
    self._update(c)
    self.group_cnt += 1

  def group_count(self) -> int:
    return self.group_cnt

  def root(self, v: int) -> int:
    ''' vが属する木の根を返す
    '''
    self.expose(v)
    arr, n = self.arr, self.n
    while arr[v<<2] != n:
      v = arr[v<<2]
      self._propagate(v)
    self._splay(v)
    return v

  def same(self, u: int, v: int) -> bool:
    ''' uとvが同じ連結成分であるかを返す
    '''
    return self.root(u) == self.root(v)

  def evert(self, v: int) -> None:
    ''' vが属する元の木の根をvにする
    expose→一番右→反転フラグ
    evert後、vは遅延伝播済み(何かと便利なので)
    '''
    self.expose(v)
    self.arr[v<<2|3] ^= 1
    self._propagate(v)

  def prod(self, u: int, v: int) -> T:
    ''' パス[u -> v]間の総積を返す
    非可換に対応
    '''
    self.evert(u)
    self.expose(v)
    return self.data[v<<1]

  def apply(self, u: int, v: int, f: F) -> None:
    self.evert(u)
    self.expose(v)
    self.key[v] = self.mapping(f, self.key[v])
    self.data[v<<1] = self.mapping(f, self.data[v<<1])
    self.data[v<<1|1] = self.mapping(f, self.data[v<<1|1])
    self.lazy[v] = f if self.lazy[v] == self.id else self.composition(f, self.lazy[v])
    self._propagate(v)

  def merge(self, u: int, v: int) -> bool:
    ''' 辺[u - v]を追加する
    '''
    if self.same(u, v): return False
    self.evert(u)
    self.expose(v)
    self.arr[u<<2|2] = v
    self.arr[v<<2|1] = u
    self._update(v)
    self.group_cnt -= 1
    return True

  def split(self, u: int, v: int) -> bool:
    ''' 辺[u - v]を削除する
    '''
    if not self.same(v, u): return False
    self.evert(u)
    self.cut(v)
    return True

  def path_kth_elm(self, s: int, t: int, k: int) -> Optional[int]:
    ''' path[s -> t]のk番目を取得する
    '''
    self.evert(s)
    self.expose(t)
    if self.size[t] <= k:
      return None
    size, arr = self.size, self.arr
    while True:
      self._propagate(t)
      s = size[arr[t<<2]]
      if s == k:
        self._splay(t)
        return t
      t = arr[t<<2|(s<k)]
      if s < k:
        k -= s + 1

  def __setitem__(self, k: int, v: T):
    self._splay(k)
    self.key[k] = v
    self._update(k)

  def __getitem__(self, k: int) -> T:
    self._splay(k)
    return self.key[k]

  def __str__(self):
    # 後でやる
    return 'LinkCutTree()'

  def __repr__(self):
    # 後でやる
    return 'LinkCutTree()'

