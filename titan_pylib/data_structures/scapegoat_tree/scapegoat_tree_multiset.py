from titan_pylib.my_class.ordered_multiset_interface import OrderedMultisetInterface
from titan_pylib.my_class.supports_less_than import SupportsLessThan
from titan_pylib.data_structures.bst_base.bst_multiset_node_base import (
    BSTMultisetNodeBase,
)
import math
from typing import Final, TypeVar, Generic, Iterable, Optional, Iterator

T = TypeVar("T", bound=SupportsLessThan)


class ScapegoatTreeMultiset(OrderedMultisetInterface, Generic[T]):

    ALPHA: Final[float] = 0.75
    BETA: Final[float] = math.log2(1 / ALPHA)

    class Node:

        def __init__(self, key: T, val: int):
            self.key: T = key
            self.val: int = val
            self.size: int = 1
            self.valsize: int = val
            self.left: Optional[ScapegoatTreeMultiset.Node] = None
            self.right: Optional[ScapegoatTreeMultiset.Node] = None

        def __str__(self):
            if self.left is None and self.right is None:
                return f"key:{self.key, self.val, self.size, self.valsize}\n"
            return f"key:{self.key, self.val, self.size, self.valsize},\n left:{self.left},\n right:{self.right}\n"

    def __init__(self, a: Iterable[T] = []):
        self.root = None
        if not isinstance(a, list):
            a = list(a)
        self._build(a)

    def _build(self, a: list[T]) -> None:
        Node = ScapegoatTreeMultiset.Node

        def rec(l: int, r: int) -> ScapegoatTreeMultiset.Node:
            mid = (l + r) >> 1
            node = Node(x[mid], y[mid])
            if l != mid:
                node.left = rec(l, mid)
                node.size += node.left.size
                node.valsize += node.left.valsize
            if mid + 1 != r:
                node.right = rec(mid + 1, r)
                node.size += node.right.size
                node.valsize += node.right.valsize
            return node

        if not all(a[i] <= a[i + 1] for i in range(len(a) - 1)):
            a = sorted(a)
        if not a:
            return
        x, y = BSTMultisetNodeBase[T, ScapegoatTreeMultiset.Node]._rle(a)
        self.root = rec(0, len(x))

    def _rebuild(self, node: Node) -> Node:
        def rec(l: int, r: int) -> ScapegoatTreeMultiset.Node:
            mid = (l + r) >> 1
            node = a[mid]
            node.size = 1
            node.valsize = node.val
            if l != mid:
                node.left = rec(l, mid)
                node.size += node.left.size
                node.valsize += node.left.valsize
            else:
                node.left = None
            if mid + 1 != r:
                node.right = rec(mid + 1, r)
                node.size += node.right.size
                node.valsize += node.right.valsize
            else:
                node.right = None
            return node

        a = []
        stack = []
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                a.append(node)
                node = node.right
        return rec(0, len(a))

    def _kth_elm(self, k: int) -> tuple[T, int]:
        if k < 0:
            k += len(self)
        node = self.root
        while node:
            t = (node.val + node.left.valsize) if node.left else node.val
            if t - node.val <= k and k < t:
                return node.key, node.val
            elif t > k:
                node = node.left
            else:
                node = node.right
                k -= t

    def _kth_elm_tree(self, k: int) -> tuple[T, int]:
        if k < 0:
            k += self.len_elm()
        node = self.root
        while node:
            t = node.left.size if node.left else 0
            if t == k:
                return node.key, node.val
            if t > k:
                node = node.left
            else:
                node = node.right
                k -= t + 1
        assert False, "IndexError"

    def add(self, key: T, val: int = 1) -> None:
        if val <= 0:
            return
        if not self.root:
            self.root = ScapegoatTreeMultiset.Node(key, val)
            return
        node = self.root
        path = []
        while node:
            path.append(node)
            if key == node.key:
                node.val += val
                for p in path:
                    p.valsize += val
                return
            node = node.left if key < node.key else node.right
        if key < path[-1].key:
            path[-1].left = ScapegoatTreeMultiset.Node(key, val)
        else:
            path[-1].right = ScapegoatTreeMultiset.Node(key, val)
        if len(path) * ScapegoatTreeMultiset.BETA > math.log(self.len_elm()):
            node_size = 1
            while path:
                pnode = path.pop()
                pnode_size = pnode.size + 1
                if ScapegoatTreeMultiset.ALPHA * pnode_size < node_size:
                    break
                node_size = pnode_size
            new_node = self._rebuild(pnode)
            if not path:
                self.root = new_node
                return
            if new_node.key < path[-1].key:
                path[-1].left = new_node
            else:
                path[-1].right = new_node
        for p in path:
            p.size += 1
            p.valsize += val

    def _discard(self, key: T) -> bool:
        path = []
        node = self.root
        di, cnt = 1, 0
        while node:
            if key == node.key:
                break
            path.append(node)
            di = key < node.key
            node = node.left if di else node.right
        if node.left and node.right:
            path.append(node)
            lmax = node.left
            di = 0 if lmax.right else 1
            while lmax.right:
                cnt += 1
                path.append(lmax)
                lmax = lmax.right
            lmax_val = lmax.val
            node.key = lmax.key
            node.val = lmax_val
            node = lmax
        cnode = node.left if node.left else node.right
        if path:
            if di == 1:
                path[-1].left = cnode
            else:
                path[-1].right = cnode
        else:
            self.root = cnode
            return True
        for _ in range(cnt):
            p = path.pop()
            p.size -= 1
            p.valsize -= lmax_val
        for p in path:
            p.size -= 1
            p.valsize -= 1
        return True

    def discard(self, key: T, val=1) -> bool:
        if val <= 0:
            return True
        path = []
        node = self.root
        while node:
            path.append(node)
            if key == node.key:
                break
            node = node.left if key < node.key else node.right
        else:
            return False
        if val > node.val:
            val = node.val - 1
            if val > 0:
                node.val -= val
                while path:
                    path.pop().valsize -= val
        if node.val == 1:
            self._discard(key)
        else:
            node.val -= val
            while path:
                path.pop().valsize -= val
        return True

    def remove(self, key: T, val: int = 1) -> None:
        c = self.count(key)
        if c > val:
            raise KeyError(key)
        self.discard(key, val)

    def count(self, key: T) -> int:
        node = self.root
        while node:
            if key == node.key:
                return node.val
            node = node.left if key < node.key else node.right
        return 0

    def discard_all(self, key: T) -> bool:
        return self.discard(key, self.count(key))

    def le(self, key: T) -> Optional[T]:
        return BSTMultisetNodeBase[T, ScapegoatTreeMultiset.Node].le(self.root, key)

    def lt(self, key: T) -> Optional[T]:
        return BSTMultisetNodeBase[T, ScapegoatTreeMultiset.Node].lt(self.root, key)

    def ge(self, key: T) -> Optional[T]:
        return BSTMultisetNodeBase[T, ScapegoatTreeMultiset.Node].ge(self.root, key)

    def gt(self, key: T) -> Optional[T]:
        return BSTMultisetNodeBase[T, ScapegoatTreeMultiset.Node].gt(self.root, key)

    def index(self, key: T) -> int:
        return BSTMultisetNodeBase[T, ScapegoatTreeMultiset.Node].index(self.root, key)

    def index_right(self, key: T) -> int:
        return BSTMultisetNodeBase[T, ScapegoatTreeMultiset.Node].index_right(
            self.root, key
        )

    def index_keys(self, key: T) -> int:
        k = 0
        node = self.root
        while node:
            if key == node.key:
                if node.left:
                    k += node.left.size
                break
            elif key < node.key:
                node = node.left
            else:
                k += node.val if node.left is None else node.left.size + node.val
                node = node.right
        return k

    def index_right_keys(self, key: T) -> int:
        k = 0
        node = self.root
        while node:
            if key == node.key:
                k += node.val if node.left is None else node.left.size + node.val
                break
            if key < node.key:
                node = node.left
            else:
                k += node.val if node.left is None else node.left.size + node.val
                node = node.right
        return k

    def pop(self, k: int = -1) -> T:
        if k < 0:
            k += self.root.valsize
        x = self[k]
        self.discard(x)
        return x

    def pop_min(self) -> T:
        return self.pop(0)

    def pop_max(self) -> T:
        return self.pop(-1)

    def items(self) -> Iterator[tuple[T, int]]:
        for i in range(self.len_elm()):
            yield self._kth_elm_tree(i)

    def keys(self) -> Iterator[T]:
        for i in range(self.len_elm()):
            yield self._kth_elm_tree(i)[0]

    def values(self) -> Iterator[int]:
        for i in range(self.len_elm()):
            yield self._kth_elm_tree(i)[1]

    def show(self) -> None:
        print(
            "{" + ", ".join(map(lambda x: f"{x[0]}: {x[1]}", self.tolist_items())) + "}"
        )

    def get_elm(self, k: int) -> T:
        assert (
            -self.len_elm() <= k < self.len_elm()
        ), f"IndexError: {self.__class__.__name__}.get_elm({k}), len_elm=({self.len_elm()})"
        return self._kth_elm_tree(k)[0]

    def len_elm(self) -> int:
        return self.root.size if self.root else 0

    def tolist(self) -> list[T]:
        return BSTMultisetNodeBase[T, ScapegoatTreeMultiset.Node].tolist(self.root)

    def tolist_items(self) -> list[tuple[T, int]]:
        return BSTMultisetNodeBase[T, ScapegoatTreeMultiset.Node].tolist_items(
            self.root
        )

    def clear(self) -> None:
        self.root = None

    def get_max(self) -> T:
        return self._kth_elm_tree(-1)[0]

    def get_min(self) -> T:
        return self._kth_elm_tree(0)[0]

    def __contains__(self, key: T):
        return BSTMultisetNodeBase[T, ScapegoatTreeMultiset.Node].contains(
            self.root, key
        )

    def __getitem__(self, k: int) -> T:
        assert (
            -len(self) <= k < len(self)
        ), f"IndexError: {self.__class__.__name__}[{k}], len={len(self)}"
        return self._kth_elm(k)[0]

    def __iter__(self):
        self.__iter = 0
        return self

    def __next__(self):
        if self.__iter == len(self):
            raise StopIteration
        res = self._kth_elm(self.__iter)[0]
        self.__iter += 1
        return res

    def __reversed__(self):
        for i in range(len(self)):
            yield self._kth_elm(-i - 1)[0]

    def __len__(self):
        return self.root.valsize if self.root else 0

    def __bool__(self):
        return self.root is not None

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.tolist})"
