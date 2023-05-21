from typing import Generic, Iterator, TypeVar, Callable, Iterable, Optional, Union, Tuple, List, Dict
from types import GeneratorType
T = TypeVar('T')
F = TypeVar('F')

class EulerTourTree(Generic[T, F]):

  class Node():

    def __init__(self, index: Tuple[int, int], key: T, lazy: F):
      self.index = index
      self.key = key
      self.data = key
      self.lazy = lazy
      self.par = None
      self.left = None
      self.right = None

    def is_vertex(self) -> bool:
      return self.index[0] == self.index[1]

    def __str__(self):
      if self.left is None and self.right is None:
        return f'(index,par):{self.index,self.key,self.data,self.lazy,(self.par.index if self.par else None)}\n'
      return f'(index,par):{self.index,self.key,self.data,self.lazy,(self.par.index if self.par else None)},\n left:{self.left},\n right:{self.right}\n'

    __repr__ = __str__


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
    a = [e for _ in range(n_or_a)] if isinstance(n_or_a, int) else list(n_or_a)
    self.ptr_vertex: List[EulerTourTree.Node] = [EulerTourTree.Node((i, i), elem, id) for i, elem in enumerate(a)]
    self.ptr_edge: Dict[Tuple[int, int], EulerTourTree.Node] = {}
    self.n = len(a)
    self._group_numbers = self.n

  def antirec(func, stack=[]):
    # 参考: https://github.com/cheran-senthil/PyRival/blob/master/pyrival/misc/bootstrap.py
    def wrappedfunc(*args, **kwargs):
      if stack:
        return func(*args, **kwargs)
      to = func(*args, **kwargs)
      while True:
        if isinstance(to, GeneratorType):
          stack.append(to)
          to = next(to)
        else:
          stack.pop()
          if not stack:
            break
          to = stack[-1].send(to)
      return to
    return wrappedfunc

  def build(self, G: List[List[int]]) -> None:
    seen = [0] * self.n
    Node = EulerTourTree.Node
    antirec = EulerTourTree.antirec
    ptr_vertex, ptr_edge, e, id = self.ptr_vertex, self.ptr_edge, self.e, self.id

    @antirec
    def dfs(v: int, p: int=-1) -> Iterator:
      a.append((v, v))
      for x in G[v]:
        if x == p:
          continue
        a.append((v, x))
        yield dfs(x, v)
        a.append((x, v))
      yield

    @antirec
    def sort(l: int, r: int) -> Iterator[Node]:
      mid = (l + r) >> 1
      if a[mid][0] == a[mid][1]:
        seen[a[mid][0]] = 1
        node = ptr_vertex[a[mid][0]]
      else:
        node = Node(a[mid], e, id)
        ptr_edge[a[mid]] = node
      if l != mid:
        node.left = yield sort(l, mid)
        node.left.par = node
      if mid + 1 != r:
        node.right = yield sort(mid+1, r)
        node.right.par = node
      self._update(node)
      yield node

    for root in range(self.n):
      if seen[root]:
        continue
      a = []
      dfs(root)
      sort(0, len(a))

  def _popleft(self, v: Node) -> Optional[Node]:
    assert v is not None
    v = self._left_splay(v)
    if v.right:
      v.right.par = None
    return v.right

  def _pop(self, v: Node) -> Optional[Node]:
    assert v is not None
    v = self._right_splay(v)
    if v.left:
      v.left.par = None
    return v.left

  def _split_left(self, v: Node) -> Tuple[Node, Optional[Node]]:
    # x, yに分割する。ただし、xはvを含む
    assert v is not None
    self._splay(v)
    x, y = v, v.right
    if y is not None:
      y.par = None
    x.right = None
    self._update(x)
    return x, y

  def _split_right(self, v: Node) -> Tuple[Optional[Node], Node]:
    # x, yに分割する。ただし、yはvを含む
    assert v is not None
    self._splay(v)
    x, y = v.left, v
    if x is not None:
      x.par = None
    y.left = None
    self._update(y)
    return x, y

  def _merge(self, u: Optional[Node], v: Optional[Node]) -> None:
    if u is None or v is None:
      return
    u = self._right_splay(u)
    self._splay(v)
    u.right = v
    v.par = u
    self._update(u)

  def _splay(self, node: Node) -> None:
    self._propagate(node)
    while node.par is not None and node.par.par is not None:
      pnode = node.par
      gnode = pnode.par
      self._propagate(gnode)
      self._propagate(pnode)
      self._propagate(node)
      node.par = gnode.par
      if (gnode.left is pnode) == (pnode.left is node):
        if pnode.left is node:
          tmp1 = node.right
          pnode.left = tmp1
          node.right = pnode
          pnode.par = node
          tmp2 = pnode.right
          gnode.left = tmp2
          pnode.right = gnode
          gnode.par = pnode
        else:
          tmp1 = node.left
          pnode.right = tmp1
          node.left = pnode
          pnode.par = node
          tmp2 = pnode.left
          gnode.right = tmp2
          pnode.left = gnode
          gnode.par = pnode
        if tmp1:
          tmp1.par = pnode
        if tmp2:
          tmp2.par = gnode
      else:
        if pnode.left is node:
          tmp1 = node.right
          pnode.left = tmp1
          node.right = pnode
          tmp2 = node.left
          gnode.right = tmp2
          node.left = gnode
          pnode.par = node
          gnode.par = node
        else:
          tmp1 = node.left
          pnode.right = tmp1
          node.left = pnode
          tmp2 = node.right
          gnode.left = tmp2
          node.right = gnode
          pnode.par = node
          gnode.par = node
        if tmp1:
          tmp1.par = pnode
        if tmp2:
          tmp2.par = gnode
      self._update(gnode)
      self._update(pnode)
      self._update(node)
      if node.par is None:
        return
      if node.par.left is gnode:
        node.par.left = node
      else:
        node.par.right = node
    if node.par is None:
      return
    pnode = node.par
    self._propagate(pnode)
    self._propagate(node)
    if pnode.left is node:
      pnode.left = node.right
      if pnode.left:
        pnode.left.par = pnode
      node.right = pnode
    else:
      pnode.right = node.left
      if pnode.right:
        pnode.right.par = pnode
      node.left = pnode
    node.par = None
    pnode.par = node
    self._update(pnode)
    self._update(node)

  def _left_splay(self, node: Node) -> Node:
    assert node is not None
    self._splay(node)
    while node.left is not None:
      node = node.left
    self._splay(node)
    return node

  def _right_splay(self, node: Node) -> Node:
    assert node is not None
    self._splay(node)
    while node.right is not None:
      node = node.right
    self._splay(node)
    return node

  def _propagate(self, node: Optional[Node]) -> None:
    if node is None or node.lazy == self.id:
      return
    if node.left is not None:
      node.left.key = self.mapping(node.lazy, node.left.key)
      node.left.data = self.mapping(node.lazy, node.left.data)
      node.left.lazy = self.composition(node.lazy, node.left.lazy)
    if node.right is not None:
      node.right.key = self.mapping(node.lazy, node.right.key)
      node.right.data = self.mapping(node.lazy, node.right.data)
      node.right.lazy = self.composition(node.lazy, node.right.lazy)
    node.lazy = self.id

  def _update(self, node: Node) -> None:
    self._propagate(node.left)
    self._propagate(node.right)
    left_data = self.e if node.left is None else node.left.data
    right_data = self.e if node.right is None else node.right.data
    node.data = self.op(self.op(left_data, node.key), right_data)

  def link(self, u: int, v: int) -> None:
    # add edge{u, v}
    self.reroot(u)
    self.reroot(v)
    assert (u, v) not in self.ptr_edge, f'EulerTourTree.cut(), {(u, v)} in ptr_edge'
    assert (v, u) not in self.ptr_edge, f'EulerTourTree.cut(), {(v, u)} in ptr_edge'
    uv_node = EulerTourTree.Node((u, v), self.e, self.id)
    vu_node = EulerTourTree.Node((v, u), self.e, self.id)
    self.ptr_edge[(u, v)] = uv_node
    self.ptr_edge[(v, u)] = vu_node
    u_node = self.ptr_vertex[u]
    v_node = self.ptr_vertex[v]
    self._merge(u_node, uv_node)
    self._merge(uv_node, v_node)
    self._merge(v_node, vu_node)
    self._group_numbers -= 1

  def cut(self, u: int, v: int) -> None:
    # erace edge{u, v}
    self.reroot(v)
    self.reroot(u)
    assert (u, v) in self.ptr_edge, f'{(u, v)} not in ptr_edge'
    assert (v, u) in self.ptr_edge, f'{(v, u)} not in ptr_edge'
    uv_node = self.ptr_edge.pop((u, v))
    vu_node = self.ptr_edge.pop((v, u))
    a, _ = self._split_left(uv_node)
    _, c = self._split_right(vu_node)
    a = self._pop(a)
    c = self._popleft(c)
    self._merge(a, c)
    self._group_numbers += 1

  def merge(self, u: int, v: int) -> bool:
    # add edge{u, v} unless same(u, v)
    if self.same(u, v):
      return False
    self.link(u, v)
    return True

  def split(self, u: int, v: int) -> bool:
    # erase edge{u, v} if both {u, v} and {v, u} in E
    if (u, v) not in self.ptr_edge or (v, u) not in self.ptr_edge:
      return False
    self.cut(u, v)
    return True

  def leader(self, v: int) -> Node:
    # vを含む木の代表元
    # rerootすると変わるので注意
    return self._left_splay(self.ptr_vertex[v])

  def reroot(self, v: int) -> None:
    node = self.ptr_vertex[v]
    x, y = self._split_right(node)
    self._merge(y, x)
    self._splay(node)

  def same(self, u: int, v: int) -> bool:
    u_node = self.ptr_vertex[u]
    v_node = self.ptr_vertex[v]
    self._splay(u_node)
    self._splay(v_node)
    return u_node.par is not None or u_node is v_node

  def show(self) -> None:
    # for debug
    print('+++++++++++++++++++++++++++')
    for i, v in enumerate(self.ptr_vertex):
      print((i, i), v, end='\n\n')
    for k, v in self.ptr_edge.items():
      print(k, v, end='\n\n')
    print('+++++++++++++++++++++++++++')

  def subtree_apply(self, v: int, p: int, f: F) -> None:
    # 頂点pを親としたときの頂点vの部分木にfを作用
    if p == -1:
      v_node = self.ptr_vertex[v]
      self._splay(v_node)
      v_node.key = self.mapping(f, v_node.key)
      v_node.data = self.mapping(f, v_node.data)
      v_node.lazy = self.composition(f, v_node.lazy)
      return
    self.reroot(v)
    self.reroot(p)
    assert (p, v) in self.ptr_edge, f'{(p, v)} not in ptr_edge'
    assert (v, p) in self.ptr_edge, f'{(v, p)} not in ptr_edge'
    v_node = self.ptr_vertex[v]
    a, b = self._split_right(self.ptr_edge[(p, v)])
    b, d = self._split_left(self.ptr_edge[(v, p)])
    self._splay(v_node)
    v_node.key = self.mapping(f, v_node.key)
    v_node.data = self.mapping(f, v_node.data)
    v_node.lazy = self.composition(f, v_node.lazy)
    self._propagate(v_node)
    self._merge(a, b)
    self._merge(b, d)

  def subtree_sum(self, v: int, p: int) -> T:
    # 頂点pを親としたときの頂点vの部分木に含まれる総和
    if p == -1:
      v_node = self.ptr_vertex[v]
      self._splay(v_node)
      return v_node.data
    self.reroot(v)
    self.reroot(p)
    assert (p, v) in self.ptr_edge, f'{(p, v)} not in ptr_edge'
    assert (v, p) in self.ptr_edge, f'{(v, p)} not in ptr_edge'
    v_node = self.ptr_vertex[v]
    a, b = self._split_right(self.ptr_edge[(p, v)])
    b, d = self._split_left(self.ptr_edge[(v, p)])
    self._splay(v_node)
    res = v_node.data
    self._merge(a, b)
    self._merge(b, d)
    return res

  def group_count(self) -> int:
    return self._group_numbers

  def get_vertex(self, v: int) -> T:
    node = self.ptr_vertex[v]
    self._splay(node)
    return node.key

  def set_vertex(self, v: int, val: T) -> None:
    node = self.ptr_vertex[v]
    self._splay(node)
    node.key = val
    self._update(node)

  def __getitem__(self, v: int) -> T:
    return self.get_vertex(v)

  def __setitem__(self, v: int, val: T) -> None:
    return self.set_vertex(v, val)

def op(s, t):
  return

def mapping(f, s):
  return

def composition(f, g):
  return

e = None
id = None

