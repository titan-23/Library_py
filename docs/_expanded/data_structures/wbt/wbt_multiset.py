# from titan_pylib.data_structures.wbt.wbt_multiset import WBTMultiset
# from titan_pylib.data_structures.wbt._wbt_multiset_node import _WBTMultisetNode
# from titan_pylib.data_structures.wbt._wbt_node_base import _WBTNodeBase
from typing import Generic, TypeVar, Optional, Final

T = TypeVar("T")


class _WBTNodeBase(Generic[T]):
    """WBTノードのベースクラス
    size, par, left, rightをもつ
    """

    __slots__ = "_size", "_par", "_left", "_right"
    DELTA: Final[int] = 3
    GAMMA: Final[int] = 2

    def __init__(self) -> None:
        self._size: int = 1
        self._par: Optional[_WBTNodeBase[T]] = None
        self._left: Optional[_WBTNodeBase[T]] = None
        self._right: Optional[_WBTNodeBase[T]] = None

    def _rebalance(self) -> "_WBTNodeBase[T]":
        """根までを再構築する

        Returns:
            _WBTNodeBase[T]: 根ノード
        """
        node = self
        while True:
            node._update()
            wl, wr = node._weight_left(), node._weight_right()
            if wl * _WBTNodeBase.DELTA < wr:
                if (
                    node._right._weight_left()
                    >= node._right._weight_right() * _WBTNodeBase.GAMMA
                ):
                    node._right = node._right._rotate_right()
                node = node._rotate_left()
            elif wr * _WBTNodeBase.DELTA < wl:
                if (
                    node._left._weight_right()
                    >= node._left._weight_left() * _WBTNodeBase.GAMMA
                ):
                    node._left = node._left._rotate_left()
                node = node._rotate_right()
            if not node._par:
                return node
            node = node._par

    def _copy_from(self, other: "_WBTNodeBase[T]") -> None:
        self._size = other._size
        if other._left:
            other._left._par = self
        if other._right:
            other._right._par = self
        if other._par:
            if other._par._left is other:
                other._par._left = self
            else:
                other._par._right = self
        self._par = other._par
        self._left = other._left
        self._right = other._right

    def _weight_left(self) -> int:
        return self._left._size + 1 if self._left else 1

    def _weight_right(self) -> int:
        return self._right._size + 1 if self._right else 1

    def _update(self) -> None:
        self._size = (
            1
            + (self._left._size if self._left else 0)
            + (self._right._size if self._right else 0)
        )

    def _rotate_right(self) -> "_WBTNodeBase[T]":
        u = self._left
        u._size = self._size
        self._size -= u._left._size + 1 if u._left else 1
        u._par = self._par
        self._left = u._right
        if u._right:
            u._right._par = self
        u._right = self
        self._par = u
        if u._par:
            if u._par._left is self:
                u._par._left = u
            else:
                u._par._right = u
        return u

    def _rotate_left(self) -> "_WBTNodeBase[T]":
        u = self._right
        u._size = self._size
        self._size -= u._right._size + 1 if u._right else 1
        u._par = self._par
        self._right = u._left
        if u._left:
            u._left._par = self
        u._left = self
        self._par = u
        if u._par:
            if u._par._left is self:
                u._par._left = u
            else:
                u._par._right = u
        return u

    def _balance_check(self) -> None:
        if not self._weight_left() * _WBTNodeBase.DELTA >= self._weight_right():
            print(self._weight_left(), self._weight_right(), flush=True)
            print(self)
            assert False, f"self._weight_left() * DELTA >= self._weight_right()"
        if not self._weight_right() * _WBTNodeBase.DELTA >= self._weight_left():
            print(self._weight_left(), self._weight_right(), flush=True)
            print(self)
            assert False, f"self._weight_right() * DELTA >= self._weight_left()"

    def _min(self) -> "_WBTNodeBase[T]":
        node = self
        while node._left:
            node = node._left
        return node

    def _max(self) -> "_WBTNodeBase[T]":
        node = self
        while node._right:
            node = node._right
        return node

    def _next(self) -> Optional["_WBTNodeBase[T]"]:
        if self._right:
            return self._right._min()
        now, pre = self, None
        while now and now._right is pre:
            now, pre = now._par, now
        return now

    def _prev(self) -> Optional["_WBTNodeBase[T]"]:
        if self._left:
            return self._left._max()
        now, pre = self, None
        while now and now._left is pre:
            now, pre = now._par, now
        return now

    def __add__(self, other: int) -> Optional["_WBTNodeBase[T]"]:
        node = self
        for _ in range(other):
            node = node._next()
        return node

    def __sub__(self, other: int) -> Optional["_WBTNodeBase[T]"]:
        node = self
        for _ in range(other):
            node = node._prev()
        return node

    __iadd__ = __add__
    __isub__ = __sub__

    def __str__(self) -> str:
        # if self._left is None and self._right is None:
        #     return f"key:{self._key, self._size}\n"
        # return f"key:{self._key, self._size},\n _left:{self._left},\n _right:{self._right}\n"
        return str(self._key)

    __repr__ = __str__
from typing import TypeVar, Optional

T = TypeVar("T")


class _WBTMultisetNode(_WBTNodeBase[T]):

    __slots__ = "_key", "_count", "_count_size", "_size", "_par", "_left", "_right"

    def __init__(self, key: T, count: int) -> None:
        super().__init__()
        self._key: T = key
        self._count: int = count
        self._count_size: int = count
        self._par: Optional[_WBTMultisetNode[T]]
        self._left: Optional[_WBTMultisetNode[T]]
        self._right: Optional[_WBTMultisetNode[T]]

    @property
    def key(self) -> T:
        return self._key

    @property
    def count(self) -> T:
        return self._count

    def _update(self) -> None:
        super()._update()
        self._count_size = (
            self._count
            + (self._left._count_size if self._left else 0)
            + (self._right._count_size if self._right else 0)
        )

    def _rotate_right(self) -> "_WBTMultisetNode[T]":
        u = self._left
        u._size = self._size
        u._count_size = self._count_size
        self._size -= u._left._size + 1 if u._left else 1
        self._count_size -= u._left._count_size + u._count if u._left else u._count
        u._par = self._par
        self._left = u._right
        if u._right:
            u._right._par = self
        u._right = self
        self._par = u
        if u._par:
            if u._par._left is self:
                u._par._left = u
            else:
                u._par._right = u
        return u

    def _rotate_left(self) -> "_WBTMultisetNode[T]":
        u = self._right
        u._size = self._size
        u._count_size = self._count_size
        self._size -= u._right._size + 1 if u._right else 1
        self._count_size -= u._right._count_size + u._count if u._right else u._count
        u._par = self._par
        self._right = u._left
        if u._left:
            u._left._par = self
        u._left = self
        self._par = u
        if u._par:
            if u._par._left is self:
                u._par._left = u
            else:
                u._par._right = u
        return u

    def _copy_from(self, other: "_WBTMultisetNode[T]") -> None:
        super()._copy_from(other)
        self._count = other._count
        self._count_size = other._count_size
from typing import Generic, TypeVar, Optional, Iterable, Iterator

T = TypeVar("T")


class WBTMultiset(Generic[T]):

    __slots__ = "_root", "_min", "_max"

    def __init__(self, a: Iterable[T] = []) -> None:
        self._root: Optional[_WBTMultisetNode[T]] = None
        self._min: Optional[_WBTMultisetNode[T]] = None
        self._max: Optional[_WBTMultisetNode[T]] = None
        self.__build(a)

    def __build(self, a: Iterable[T]) -> None:
        def build(
            l: int, r: int, pnode: Optional[_WBTMultisetNode[T]] = None
        ) -> _WBTMultisetNode[T]:
            if l == r:
                return None
            mid = (l + r) // 2
            node = _WBTMultisetNode(keys[mid], vals[mid])
            node._left = build(l, mid, node)
            node._right = build(mid + 1, r, node)
            node._par = pnode
            node._update()
            return node

        a = list(a)
        if not a:
            return
        if not all(a[i] <= a[i + 1] for i in range(len(a) - 1)):
            a.sort()
        # RLE
        keys, vals = [a[0]], [1]
        for i, elm in enumerate(a):
            if i == 0:
                continue
            if elm == keys[-1]:
                vals[-1] += 1
                continue
            keys.append(elm)
            vals.append(1)
        self._root = build(0, len(keys))
        self._max = self._root._max()
        self._min = self._root._min()

    def add(self, key: T, count: int = 1) -> None:
        if not self._root:
            self._root = _WBTMultisetNode(key, count)
            self._max = self._root
            self._min = self._root
            return
        pnode = None
        node = self._root
        while node:
            node._count_size += count
            if key == node._key:
                node._count += count
                return
            pnode = node
            node = node._left if key < node._key else node._right
        if key < pnode._key:
            pnode._left = _WBTMultisetNode(key, count)
            if key < self._min._key:
                self._min = pnode._left
            pnode._left._par = pnode
        else:
            pnode._right = _WBTMultisetNode(key, count)
            if key > self._max._key:
                self._max = pnode._right
            pnode._right._par = pnode
        self._root = pnode._rebalance()

    def find_key(self, key: T) -> Optional[_WBTMultisetNode[T]]:
        node = self._root
        while node:
            if key == node._key:
                return node
            node = node._left if key < node._key else node._right
        return None

    def find_order(self, k: int) -> _WBTMultisetNode[T]:
        node = self._root
        while True:
            t = node._left._count_size + node._count if node._left else node._count
            if t - node._count <= k < t:
                return node
            if t > k:
                node = node._left
            else:
                node = node._right
                k -= t

    def remove_iter(self, node: _WBTMultisetNode[T]) -> None:
        if node is self._min:
            self._min = self._min._next()
        if node is self._max:
            self._max = self._max._prev()
        delnode = node
        pnode, mnode = node._par, None
        if node._left and node._right:
            pnode, mnode = node, node._left
            while mnode._right:
                pnode, mnode = mnode, mnode._right
            node._count = mnode._count
            node = mnode
        cnode = node._right if not node._left else node._left
        if cnode:
            cnode._par = pnode
        if pnode:
            if pnode._left is node:
                pnode._left = cnode
            else:
                pnode._right = cnode
            self._root = pnode._rebalance()
        else:
            self._root = cnode
        if mnode:
            if self._root is delnode:
                self._root = mnode
            mnode._copy_from(delnode)
        del delnode

    def remove(self, key: T, count: int = 1) -> None:
        node = self.find_key(key)
        node._count -= count
        if node._count <= 0:
            self.remove_iter(node)

    def discard(self, key: T, count: int = 1) -> bool:
        node = self.find_key(key)
        if node is None:
            return False
        node._count -= count
        if node._count <= 0:
            self.remove_iter(node)
        else:
            while node:
                node._count_size -= count
                node = node._par
        return True

    def pop(self, k: int = -1) -> T:
        node = self.find_order(k)
        key = node._key
        node._count -= 1
        if node._count == 0:
            self.remove_iter(node)
        return key

    def le_iter(self, key: T) -> Optional[_WBTMultisetNode[T]]:
        res = None
        node = self._root
        while node:
            if key == node._key:
                res = node
                break
            if key < node._key:
                node = node._left
            else:
                res = node
                node = node._right
        return res

    def lt_iter(self, key: T) -> Optional[_WBTMultisetNode[T]]:
        res = None
        node = self._root
        while node:
            if key <= node._key:
                node = node._left
            else:
                res = node
                node = node._right
        return res

    def ge_iter(self, key: T) -> Optional[_WBTMultisetNode[T]]:
        res = None
        node = self._root
        while node:
            if key == node._key:
                res = node
                break
            if key < node._key:
                res = node
                node = node._left
            else:
                node = node._right
        return res

    def gt_iter(self, key: T) -> Optional[_WBTMultisetNode[T]]:
        res = None
        node = self._root
        while node:
            if key < node._key:
                res = node
                node = node._left
            else:
                node = node._right
        return res

    def le(self, key: T) -> Optional[T]:
        res = None
        node = self._root
        while node:
            if key == node._key:
                res = key
                break
            if key < node._key:
                node = node._left
            else:
                res = node._key
                node = node._right
        return res

    def lt(self, key: T) -> Optional[T]:
        res = None
        node = self._root
        while node:
            if key <= node._key:
                node = node._left
            else:
                res = node._key
                node = node._right
        return res

    def ge(self, key: T) -> Optional[T]:
        res = None
        node = self._root
        while node:
            if key == node._key:
                res = key
                break
            if key < node._key:
                res = node._key
                node = node._left
            else:
                node = node._right
        return res

    def gt(self, key: T) -> Optional[T]:
        res = None
        node = self._root
        while node:
            if key < node._key:
                res = node._key
                node = node._left
            else:
                node = node._right
        return res

    def index(self, key: T) -> int:
        k = 0
        node = self._root
        while node:
            if key == node._key:
                k += node._left._count_size if node._left else 0
                break
            if key < node._key:
                node = node._left
            else:
                k += node._left._count_size + node._count if node._left else node._count
                node = node._right
        return k

    def index_right(self, key: T) -> int:
        k = 0
        node = self._root
        while node:
            if key == node._key:
                k += node._left._count_size + node._count if node._left else node._count
                break
            if key < node._key:
                node = node._left
            else:
                k += node._left._count_size + node._count if node._left else node._count
                node = node._right
        return k

    def tolist(self) -> list[T]:
        return list(self)

    def get_min(self) -> T:
        assert self._min
        return self._min._key

    def get_max(self) -> T:
        assert self._max
        return self._max._key

    def pop_min(self) -> T:
        assert self._min
        key = self._min._key
        self._min._count -= 1
        if self._min._count == 0:
            self.remove_iter(self._min)
        return key

    def pop_max(self) -> T:
        assert self._max
        key = self._max._key
        self._max._count -= 1
        if self._max._count == 0:
            self.remove_iter(self._max)
        return key

    def check(self) -> None:
        if self._root is None:
            # print("ok. 0 (empty)")
            return

        # _size, count_size, height
        def dfs(node: _WBTMultisetNode[T]) -> tuple[int, int, int]:
            h = 0
            s = 1
            cs = node.count
            if node._left:
                assert node._key > node._left._key
                ls, lcs, lh = dfs(node._left)
                s += ls
                cs += lcs
                h = max(h, lh)
            if node._right:
                assert node._key < node._right._key
                rs, rcs, rh = dfs(node._right)
                s += rs
                cs += rcs
                h = max(h, rh)
            assert node._size == s
            assert node._count_size == cs
            node._balance_check()
            return s, cs, h + 1

        _, _, h = dfs(self._root)
        # print(f"ok. {h}")

    def __contains__(self, key: T) -> bool:
        return self.find_key(key) is not None

    def __getitem__(self, k: int) -> T:
        assert (
            -len(self) <= k < len(self)
        ), f"IndexError: {self.__class__.__name__}[{k}], len={len(self)}"
        if k < 0:
            k += len(self)
        if k == 0:
            return self.get_min()
        if k == len(self) - 1:
            return self.get_max()
        return self.find_order(k)._key

    def __delitem__(self, k: int) -> None:
        node = self.find_order(k)
        node._count -= 1
        if node._count == 0:
            self.remove_iter(node)

    def __len__(self) -> int:
        return self._root._count_size if self._root else 0

    def __iter__(self) -> Iterator[T]:
        stack: list[_WBTMultisetNode[T]] = []
        node = self._root
        while stack or node:
            if node:
                stack.append(node)
                node = node._left
            else:
                node = stack.pop()
                for _ in range(node._count):
                    yield node._key
                node = node._right

    def __reversed__(self) -> Iterator[T]:
        stack: list[_WBTMultisetNode[T]] = []
        node = self._root
        while stack or node:
            if node:
                stack.append(node)
                node = node._right
            else:
                node = stack.pop()
                for _ in range(node._count):
                    yield node._key
                node = node._left

    def __str__(self) -> str:
        return "{" + ", ".join(map(str, self)) + "}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            + "["
            + ", ".join(map(str, self.tolist()))
            + "])"
        )
