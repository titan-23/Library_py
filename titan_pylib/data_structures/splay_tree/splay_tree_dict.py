from titan_pylib.my_class.supports_less_than import SupportsLessThan
from array import array
from typing import Generic, Iterator, TypeVar, Any

T = TypeVar("T", bound=SupportsLessThan)


class SplayTreeDict(Generic[T]):

    def __init__(self, e: T, default: Any = 0, reserve: int = 1) -> None:
        # e: keyとして使わない値
        # default: valのdefault値
        if reserve < 1:
            reserve = 1
        self._keys: list[T] = [e] * reserve
        self._vals: list[Any] = [0] * reserve
        self._child = array("I", bytes(8 * reserve))
        self._end: int = 1
        self._root: int = 0
        self._len: int = 0
        self._default: Any = default
        self._e: T = e

    def reserve(self, n: int) -> None:
        assert n >= 0, "ValueError"
        self._keys += [self._e] * n
        self._vals += [0] * n
        self._child += array("I", bytes(8 * n))

    def _make_node(self, key: T, val: Any) -> int:
        if self._end >= len(self._keys):
            self._keys.append(key)
            self._vals.append(val)
            self._child.append(0)
            self._child.append(0)
        else:
            self._keys[self._end] = key
            self._vals[self._end] = val
        self._end += 1
        return self._end - 1

    def _set_search_splay(self, key: T) -> None:
        node = self._root
        keys, child = self._keys, self._child
        if (not node) or keys[node] == key:
            return
        left, right = 0, 0
        while keys[node] != key:
            d = key > keys[node]
            if not child[node << 1 | d]:
                break
            if (d and key > keys[child[node << 1 | 1]]) or (
                d ^ 1 and key < keys[child[node << 1]]
            ):
                new = child[node << 1 | d]
                child[node << 1 | d] = child[new << 1 | (d ^ 1)]
                child[new << 1 | (d ^ 1)] = node
                node = new
                if not child[node << 1 | d]:
                    break
            if d:
                child[left << 1 | 1] = node
                left = node
            else:
                child[right << 1] = node
                right = node
            node = child[node << 1 | d]
        child[right << 1] = child[node << 1 | 1]
        child[left << 1 | 1] = child[node << 1]
        child[node << 1] = child[1]
        child[node << 1 | 1] = child[0]
        self._root = node

    def _get_min_splay(self, node: int) -> int:
        child = self._child
        if (not node) or (not child[node << 1]):
            return node
        right = 0
        while child[node << 1]:
            new = child[node << 1]
            child[node << 1] = child[new << 1 | 1]
            child[new << 1 | 1] = node
            if not child[new << 1]:
                break
            child[right << 1] = new
            right = new
            node = child[new << 1]
        child[right << 1] = child[node << 1 | 1]
        child[1] = child[node << 1]
        child[node << 1] = child[1]
        child[node << 1 | 1] = child[0]
        return node

    def __setitem__(self, key: T, val: Any):
        if not self._root:
            self._root = self._make_node(key, val)
            self._len += 1
            return
        self._set_search_splay(key)
        if self._keys[self._root] == key:
            self._vals[self._root] = val
            return
        node = self._make_node(key, val)
        d = self._keys[self._root] < key
        self._child[node << 1 | (d ^ 1)] = self._root
        self._child[node << 1 | d] = self._child[self._root << 1 | d]
        self._child[self._root << 1 | d] = 0
        self._root = node
        self._len += 1

    def __delitem__(self, key: T) -> None:
        if self._root == 0:
            return
        self._set_search_splay(key)
        if self._keys[self._root] != key:
            return
        if self._child[self._root << 1] == 0:
            self._root = self._child[self._root << 1 | 1]
        elif self._child[self._root << 1 | 1] == 0:
            self._root = self._child[self._root << 1]
        else:
            node = self._get_min_splay(self._child[self._root << 1 | 1])
            self._child[node << 1] = self._child[self._root << 1]
            self._root = node
        self._len -= 1

    def tolist(self) -> list[tuple[T, Any]]:
        node = self._root
        child, keys, vals = self._child, self._keys, self._vals
        stack, res = [], []
        while stack or node:
            if node:
                stack.append(node)
                node = child[node << 1]
            else:
                node = stack.pop()
                res.append((keys[node], vals[node]))
                node = child[node << 1 | 1]
        return res

    def keys(self) -> Iterator[T]:
        node = self._root
        child, keys = self._child, self._keys
        stack = []
        while stack or node:
            if node:
                stack.append(node)
                node = child[node << 1]
            else:
                node = stack.pop()
                yield keys[node]
                node = child[node << 1 | 1]

    def vals(self) -> Iterator[Any]:
        node = self._root
        child, vals = self._child, self._vals
        stack = []
        while stack or node:
            if node:
                stack.append(node)
                node = child[node << 1]
            else:
                node = stack.pop()
                yield vals[node]
                node = child[node << 1 | 1]

    def items(self) -> Iterator[tuple[T, Any]]:
        node = self._root
        child, keys, vals = self._child, self._keys, self._vals
        stack = []
        while stack or node:
            if node:
                stack.append(node)
                node = child[node << 1]
            else:
                node = stack.pop()
                yield (keys[node], vals[node])
                node = child[node << 1 | 1]

    def __getitem__(self, key: T) -> Any:
        self._set_search_splay(key)
        if self._root == 0 or self._keys[self._root] != key:
            return self._default
        return self._vals[self._root]

    def __contains__(self, key: T):
        self._set_search_splay(key)
        return self._keys[self._root] == key

    def __len__(self):
        return self._len

    def __bool__(self):
        return self._root > 0

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __repr__(self):
        return f"SplayTreeDict({self})"
