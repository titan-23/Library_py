from titan_pylib.my_class.supports_less_than import SupportsLessThan
from titan_pylib.my_class.ordered_multiset_interface import OrderedMultisetInterface
from array import array
from typing import Optional, Generic, Iterable, List, Sequence, TypeVar, Tuple
from __pypy__ import newlist_hint

T = TypeVar("T", bound=SupportsLessThan)


class SplayTreeMultisetTopDown(OrderedMultisetInterface, Generic[T]):

    def __init__(self, a: Iterable[T] = [], e: T = 0):
        self.keys: List[T] = [e]
        self.vals: List[int] = [0]
        self.child = array("I", bytes(8))
        self.end: int = 1
        self.root: int = 0
        self.len: int = 0
        self.e: T = e
        if not isinstance(a, list):
            a = list(a)
        if a:
            self._build(a)

    def _rle(self, a: Sequence[T]) -> Tuple[List[T], List[int]]:
        x = newlist_hint(len(a))
        y = newlist_hint(len(a))
        x.append(a[0])
        y.append(1)
        for i, e in enumerate(a):
            if i == 0:
                continue
            if e == x[-1]:
                y[-1] += 1
                continue
            x.append(e)
            y.append(1)
        return x, y

    def _build(self, a: Sequence[T]) -> None:
        def rec(l: int, r: int) -> int:
            mid = (l + r) >> 1
            if l != mid:
                child[mid << 1] = rec(l, mid)
            if mid + 1 != r:
                child[mid << 1 | 1] = rec(mid + 1, r)
            return mid

        if not all(a[i] <= a[i + 1] for i in range(len(a) - 1)):
            a = sorted(a)
        x, y = self._rle(a)
        n = len(x)
        keys, vals, child = self.keys, self.vals, self.child
        self.reserve(n - len(keys) + 2)
        self.end += n
        keys[1 : n + 1] = x
        vals[1 : n + 1] = y
        self.root = rec(1, n + 1)
        self.len = len(a)

    def _make_node(self, key: T, val: int) -> int:
        if self.end >= len(self.keys):
            self.keys.append(key)
            self.vals.append(val)
            self.child.append(0)
            self.child.append(0)
        else:
            self.keys[self.end] = key
            self.vals[self.end] = val
        self.end += 1
        return self.end - 1

    def _rotate_left(self, node: int) -> int:
        child = self.child
        u = child[node << 1]
        child[node << 1] = child[u << 1 | 1]
        child[u << 1 | 1] = node
        return u

    def _rotate_right(self, node: int) -> int:
        child = self.child
        u = child[node << 1 | 1]
        child[node << 1 | 1] = child[u << 1]
        child[u << 1] = node
        return u

    def _set_search_splay(self, key: T) -> None:
        node = self.root
        keys, child = self.keys, self.child
        if (not node) or keys[node] == key:
            return
        left, right = 0, 0
        while keys[node] != key:
            f = key > keys[node]
            if not child[node << 1 | f]:
                break
            if f:
                if key > keys[child[node << 1 | 1]]:
                    node = self._rotate_right(node)
                    if not child[node << 1 | 1]:
                        break
                child[left << 1 | 1] = node
                left = node
            else:
                if key < keys[child[node << 1]]:
                    node = self._rotate_left(node)
                    if not child[node << 1]:
                        break
                child[right << 1] = node
                right = node
            node = child[node << 1 | f]
        child[right << 1] = child[node << 1 | 1]
        child[left << 1 | 1] = child[node << 1]
        child[node << 1] = child[1]
        child[node << 1 | 1] = child[0]
        self.root = node

    def _get_min_splay(self, node: int) -> int:
        child = self.child
        if (not node) or (not child[node << 1]):
            return node
        right = 0
        while child[node << 1]:
            node = self._rotate_left(node)
            if not child[node << 1]:
                break
            child[right << 1] = node
            right = node
            node = child[node << 1]
        child[right << 1] = child[node << 1 | 1]
        child[1] = child[node << 1]
        child[node << 1] = child[1]
        child[node << 1 | 1] = child[0]
        return node

    def _get_max_splay(self, node: int) -> int:
        child = self.child
        if (not node) or (not child[node << 1 | 1]):
            return node
        left = 0
        while child[node << 1 | 1]:
            node = self._rotate_right(node)
            if not child[node << 1 | 1]:
                break
            child[left << 1 | 1] = node
            left = node
            node = child[node << 1 | 1]
        child[0] = child[node << 1 | 1]
        child[left << 1 | 1] = child[node << 1]
        child[node << 1] = child[1]
        child[node << 1 | 1] = child[0]
        return node

    def reserve(self, n: int) -> None:
        assert n >= 0, "ValueError"
        self.keys += [self.e] * n
        self.vals += [0] * n
        self.child += array("I", bytes(8 * n))

    def add(self, key: T, val: int = 1) -> bool:
        self.len += val
        if not self.root:
            self.root = self._make_node(key, val)
            return
        keys, vals, child = self.keys, self.vals, self.child
        self._set_search_splay(key)
        if keys[self.root] == key:
            vals[self.root] += val
            return
        node = self._make_node(key, val)
        f = key > keys[self.root]
        child[node << 1 | f] = child[self.root << 1 | f]
        child[node << 1 | f ^ 1] = self.root
        child[self.root << 1 | f] = 0
        self.root = node

    def discard(self, key: T, val: int = 1) -> bool:
        if not self.root:
            return False
        self._set_search_splay(key)
        keys, vals, child = self.keys, self.vals, self.child
        if keys[self.root] != key:
            return False
        if vals[self.root] > val:
            vals[self.root] -= val
            self.len -= val
            return True
        self.len -= vals[self.root]
        if not child[self.root << 1]:
            self.root = child[self.root << 1 | 1]
        elif not child[self.root << 1 | 1]:
            self.root = child[self.root << 1]
        else:
            node = self._get_min_splay(child[self.root << 1 | 1])
            child[node << 1] = child[self.root << 1]
            self.root = node
        return True

    def discard_all(self, key: T) -> bool:
        return self.discard(key, self.count(key))

    def remove(self, key: T, val: int = 1) -> None:
        c = self.count(key)
        if c < val:
            raise KeyError(key)
        self.discard(key, val)

    def count(self, key: T) -> int:
        if not self.root:
            return 0
        self._set_search_splay(key)
        return self.vals[self.root]

    def ge(self, key: T) -> Optional[T]:
        node = self.root
        if not node:
            return None
        keys, child = self.keys, self.child
        if keys[node] == key:
            return key
        ge = None
        left, right = 0, 0
        while True:
            if keys[node] == key:
                ge = key
                break
            if key < keys[node]:
                ge = keys[node]
                if not child[node << 1]:
                    break
                if key < keys[child[node << 1]]:
                    node = self._rotate_left(node)
                    ge = keys[node]
                    if not child[node << 1]:
                        break
                child[right << 1] = node
                right = node
                node = child[node << 1]
            else:
                if not child[node << 1 | 1]:
                    break
                if key > keys[child[node << 1 | 1]]:
                    node = self._rotate_right(node)
                    if not child[node << 1 | 1]:
                        break
                child[left << 1 | 1] = node
                left = node
                node = child[node << 1 | 1]
        child[right << 1] = child[node << 1 | 1]
        child[left << 1 | 1] = child[node << 1]
        child[node << 1] = child[1]
        child[node << 1 | 1] = child[0]
        self.root = node
        return ge

    def gt(self, key: T) -> Optional[T]:
        node = self.root
        if not node:
            return None
        gt = None
        keys, child = self.keys, self.child
        left, right = 0, 0
        while True:
            if key < keys[node]:
                gt = keys[node]
                if not child[node << 1]:
                    break
                if key < keys[child[node << 1]]:
                    node = self._rotate_left(node)
                    gt = keys[node]
                    if not child[node << 1]:
                        break
                child[right << 1] = node
                right = node
                node = child[node << 1]
            else:
                if not child[node << 1 | 1]:
                    break
                if key > keys[child[node << 1 | 1]]:
                    node = self._rotate_right(node)
                    if not child[node << 1 | 1]:
                        break
                child[left << 1 | 1] = node
                left = node
                node = child[node << 1 | 1]
        child[right << 1] = child[node << 1 | 1]
        child[left << 1 | 1] = child[node << 1]
        child[node << 1] = child[1]
        child[node << 1 | 1] = child[0]
        self.root = node
        return gt

    def le(self, key: T) -> Optional[T]:
        node = self.root
        if not node:
            return None
        keys, child = self.keys, self.child
        if keys[node] == key:
            return key
        le = None
        left, right = 0, 0
        while True:
            if keys[node] == key:
                le = key
                break
            if key < keys[node]:
                if not child[node << 1]:
                    break
                if key < keys[child[node << 1]]:
                    node = self._rotate_left(node)
                    if not child[node << 1]:
                        break
                child[right << 1] = node
                right = node
                node = child[node << 1]
            else:
                le = keys[node]
                if not child[node << 1 | 1]:
                    break
                if key > keys[child[node << 1 | 1]]:
                    node = self._rotate_right(node)
                    le = keys[node]
                    if not child[node << 1 | 1]:
                        break
                child[left << 1 | 1] = node
                left = node
                node = child[node << 1 | 1]
        child[right << 1] = child[node << 1 | 1]
        child[left << 1 | 1] = child[node << 1]
        child[node << 1] = child[1]
        child[node << 1 | 1] = child[0]
        self.root = node
        return le

    def lt(self, key: T) -> Optional[T]:
        node = self.root
        if not node:
            return None
        lt = None
        keys, child = self.keys, self.child
        left, right = 0, 0
        while True:
            if not keys[node] > key:
                if not child[node << 1]:
                    break
                if key < keys[child[node << 1]]:
                    node = self._rotate_left(node)
                    if not child[node << 1]:
                        break
                child[right << 1] = node
                right = node
                node = child[node << 1]
            else:
                lt = keys[node]
                if not child[node << 1 | 1]:
                    break
                if key > keys[child[node << 1 | 1]]:
                    node = self._rotate_right(node)
                    lt = keys[node]
                    if not child[node << 1 | 1]:
                        break
                child[left << 1 | 1] = node
                left = node
                node = child[node << 1 | 1]
        child[right << 1] = child[node << 1 | 1]
        child[left << 1 | 1] = child[node << 1]
        child[node << 1] = child[1]
        child[node << 1 | 1] = child[0]
        self.root = node
        return lt

    def tolist(self) -> List[T]:
        node = self.root
        child, vals, keys = self.child, self.vals, self.keys
        stack, res = [], []
        while stack or node:
            if node:
                stack.append(node)
                node = child[node << 1]
            else:
                node = stack.pop()
                for _ in range(vals[node]):
                    res.append(keys[node])
                node = child[node << 1 | 1]
        return res

    def get_max(self) -> T:
        assert self.root, "IndexError: get_max() from empty SplayTreeMultisetTopDown"
        self.root = self._get_max_splay(self.root)
        return self.keys[self.root]

    def get_min(self) -> T:
        assert self.root, "IndexError: get_min() from empty SplayTreeMultisetTopDown"
        self.root = self._get_min_splay(self.root)
        return self.keys[self.root]

    def pop_max(self) -> T:
        assert self.root, "IndexError: pop_max() from empty SplayTreeMultisetTopDown"
        node = self._get_max_splay(self.root)
        self.len -= 1
        if self.vals[node] > 1:
            self.vals[node] -= 1
            self.root = node
        else:
            self.root = self.child[node << 1]
        return self.keys[node]

    def pop_min(self) -> T:
        assert self.root, "IndexError: pop_min() from empty SplayTreeMultisetTopDown"
        node = self._get_min_splay(self.root)
        self.len -= 1
        if self.vals[node] > 1:
            self.vals[node] -= 1
            self.root = node
        else:
            self.root = self.child[node << 1 | 1]
        return self.keys[node]

    def clear(self) -> None:
        self.root = 0
        self.len = 0

    def __contains__(self, key: T):
        self._set_search_splay(key)
        return self.keys[self.root] == key

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError

    def __len__(self):
        return self.len

    def __bool__(self):
        return self.root != 0

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __repr__(self):
        return f"SplayTreeMultisetTopDown({self})"
