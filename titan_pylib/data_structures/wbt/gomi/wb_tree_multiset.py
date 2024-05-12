from titan_pylib.my_class.supports_less_than import SupportsLessThan
from titan_pylib.my_class.ordered_multiset_interface import OrderedMultisetInterface
from math import sqrt
from array import array
from typing import Generic, Iterable, Optional, TypeVar, Final, Iterator

T = TypeVar("T", bound=SupportsLessThan)


class WBTreeMultiset(OrderedMultisetInterface, Generic[T]):

    ALPHA: Final[float] = 1 - sqrt(2) / 2
    BETA: Final[float] = (1 - 2 * ALPHA) / (1 - ALPHA)

    def __init__(self, a: Iterable[T] = [], e: T = 0) -> None:
        self.root: int = 0
        self.key: list[T] = [e]
        self.val: list[int] = [0]
        self.valsize: list[int] = [0]
        self.size: array[int] = array("I", bytes(4))
        self.left: array[int] = array("I", bytes(4))
        self.right: array[int] = array("I", bytes(4))
        self.end: int = 1
        self.e: T = e
        if not isinstance(a, list):
            a = list(a)
        if a:
            self._build(a)

    def reserve(self, n: int) -> None:
        self.key += [self.e] * n
        self.val += [0] * n
        self.valsize += [0] * n
        a = array("I", bytes(4 * n))
        self.left += a
        self.right += a
        self.size += array("I", [1] * n)

    def _balance(self, node: int) -> float:
        return (self.size[self.left[node]] + 1) / (self.size[node] + 1)

    def _rle(self, L: list[T]) -> tuple[list[T], list[int]]:
        x, y = [L[0]], [1]
        for i, a in enumerate(L):
            if i == 0:
                continue
            if a == x[-1]:
                y[-1] += 1
                continue
            x.append(a)
            y.append(1)
        return x, y

    def _build(self, a: list[T]) -> None:
        left, right, size, valsize = self.left, self.right, self.size, self.valsize

        def rec(l: int, r: int) -> int:
            mid = (l + r) >> 1
            node = mid
            if l != mid:
                left[node] = rec(l, mid)
                size[node] += size[left[node]]
                valsize[node] += valsize[left[node]]
            if mid + 1 != r:
                right[node] = rec(mid + 1, r)
                size[node] += size[right[node]]
                valsize[node] += valsize[right[node]]
            return node

        if not all(a[i] <= a[i + 1] for i in range(len(a) - 1)):
            a = sorted(a)
        if not a:
            return
        x, y = self._rle(a)
        n = len(x)
        end = self.end
        self.end += n
        self.reserve(n)
        self.key[end : end + n] = x
        self.val[end : end + n] = y
        self.valsize[end : end + n] = y
        self.root = rec(end, n + end)

    def _rotate_right(self, node: int) -> int:
        left, right, size, valsize = self.left, self.right, self.size, self.valsize
        u = left[node]
        size[u] = size[node]
        valsize[u] = valsize[node]
        size[node] -= size[left[u]] + 1
        valsize[node] -= valsize[left[u]] + self.val[u]
        left[node] = right[u]
        right[u] = node
        return u

    def _rotate_left(self, node: int) -> int:
        left, right, size, valsize = self.left, self.right, self.size, self.valsize
        u = right[node]
        size[u] = size[node]
        valsize[u] = valsize[node]
        size[node] -= size[right[u]] + 1
        valsize[node] -= valsize[right[u]] + self.val[u]
        right[node] = left[u]
        left[u] = node
        return u

    def _balance_left(self, node: int) -> int:
        right = self.right
        right[node] = right[node]
        u = right[node]
        if self._balance(u) >= self.BETA:
            right[node] = self._rotate_right(u)
        u = self._rotate_left(node)
        return u

    def _make_node(self, key: T, val: int) -> int:
        end = self.end
        if end >= len(self.key):
            self.key.append(key)
            self.val.append(val)
            self.valsize.append(val)
            self.size.append(1)
            self.left.append(0)
            self.right.append(0)
        else:
            self.key[end] = key
            self.val[end] = val
            self.valsize[end] = val
        self.end += 1
        return end

    def _balance_right(self, node: int) -> int:
        left = self.left
        left[node] = left[node]
        u = left[node]
        if self._balance(u) <= 1 - self.BETA:
            left[node] = self._rotate_left(u)
        u = self._rotate_right(node)
        return u

    def add(self, key: T, val: int = 1) -> None:
        if self.root == 0:
            self.root = self._make_node(key, val)
            return
        left, right, size, keys, valsize = (
            self.left,
            self.right,
            self.size,
            self.key,
            self.valsize,
        )
        node = self.root
        path: list[int] = []
        while node:
            if key == keys[node]:
                self.val[node] += val
                valsize[node] += val
                for p in path:
                    valsize[p] += val
                return
            path.append(node)
            node = left[node] if key < keys[node] else right[node]
        if key < keys[path[-1]]:
            left[path[-1]] = self._make_node(key, val)
        else:
            right[path[-1]] = self._make_node(key, val)
        while path:
            new_node = 0
            node = path.pop()
            size[node] += 1
            valsize[node] += val
            b = self._balance(node)
            if b < self.ALPHA:
                new_node = self._balance_left(node)
            elif b > 1 - self.ALPHA:
                new_node = self._balance_right(node)
            if new_node:
                if path:
                    node = path[-1]
                    if keys[new_node] < keys[node]:
                        left[node] = new_node
                    else:
                        right[node] = new_node
                else:
                    self.root = new_node

    def count(self, key: T) -> int:
        keys, left, right = self.key, self.left, self.right
        node = self.root
        while node:
            if keys[node] == key:
                return self.val[node]
            node = left[node] if key < keys[node] else right[node]
        return 0

    def remove(self, key: T, val: int) -> None:
        if self.discard(key, val):
            return
        raise KeyError(key)

    def _discard(self, node: int, path: list[int], d: int) -> bool:
        left, right, size, keys, valsize = (
            self.left,
            self.right,
            self.size,
            self.key,
            self.valsize,
        )
        fd = 0
        if left[node] and right[node]:
            path.append(node)
            lmax = left[node]
            d = 0 if right[lmax] else 1
            while right[lmax]:
                path.append(lmax)
                fd += 1
                lmax = right[lmax]
            lmax_val = self.val[lmax]
            keys[node] = keys[lmax]
            self.val[node] = lmax_val
            node = lmax
        cnode = right[node] if left[node] == 0 else left[node]
        if path:
            if d:
                left[path[-1]] = cnode
            else:
                right[path[-1]] = cnode
        else:
            self.root = cnode
            return True
        while path:
            new_node = 0
            node = path.pop()
            size[node] -= 1
            valsize[node] -= lmax_val if fd > 0 else 1
            fd -= 1
            b = self._balance(node)
            if b < self.ALPHA:
                new_node = self._balance_left(node)
            elif b > 1 - self.ALPHA:
                new_node = self._balance_right(node)
            if new_node:
                if not path:
                    self.root = new_node
                    return True
                if keys[new_node] < keys[path[-1]]:
                    left[path[-1]] = new_node
                else:
                    right[path[-1]] = new_node
        return True

    def discard(self, key: T, val: int = 1) -> bool:
        keys, vals, left, right, valsize = (
            self.key,
            self.val,
            self.left,
            self.right,
            self.valsize,
        )
        path = []
        node = self.root
        d = 0
        while node:
            if key == keys[node]:
                break
            path.append(node)
            d = key < keys[node]
            node = left[node] if d else right[node]
        else:
            return False
        if val > vals[node]:
            val = vals[node] - 1
            vals[node] -= val
            valsize[node] -= val
            for p in path:
                valsize[p] -= val
        if vals[node] == 1:
            self._discard(node, path, d)
        else:
            vals[node] -= val
            valsize[node] -= val
            for p in path:
                valsize[p] -= val
        return True

    def discard_all(self, key: T) -> None:
        self.discard(key, self.count(key))

    def _kth_elm(self, k: int) -> tuple[T, int]:
        left, right, vals, valsize = self.left, self.right, self.val, self.valsize
        if k < 0:
            k += len(self)
        node = self.root
        while True:
            t = vals[node] + valsize[left[node]]
            if t - vals[node] <= k < t:
                return self.key[node], vals[node]
            if t > k:
                node = left[node]
            else:
                node = right[node]
                k -= t

    def _kth_elm_tree(self, k: int) -> tuple[T, int]:
        left, right, vals, size = self.left, self.right, self.val, self.size
        if k < 0:
            k += self.len_elm()
        assert 0 <= k < self.len_elm()
        node = self.root
        while True:
            t = size[left[node]]
            if t == k:
                return self.key[node], vals[node]
            if t > k:
                node = left[node]
            else:
                node = right[node]
                k -= t + 1

    def tolist(self) -> list[T]:
        left, right, keys, vals = self.left, self.right, self.key, self.val
        node = self.root
        stack, a = [], []
        while stack or node:
            if node:
                stack.append(node)
                node = left[node]
            else:
                node = stack.pop()
                x = keys[node]
                for _ in range(vals[node]):
                    a.append(x)
                node = right[node]
        return a

    def tolist_items(self) -> list[tuple[T, int]]:
        left, right, keys, vals = self.left, self.right, self.key, self.val
        node = self.root
        stack, a = [], []
        while stack or node:
            if node:
                stack.append(node)
                node = left[node]
            else:
                node = stack.pop()
                a.append((keys[node], vals[node]))
                node = right[node]
        return a

    def le(self, key: T) -> Optional[T]:
        left, right, keys = self.left, self.right, self.key
        res = None
        node = self.root
        while node:
            if key == keys[node]:
                res = key
                break
            if key < keys[node]:
                node = left[node]
            else:
                res = keys[node]
                node = right[node]
        return res

    def lt(self, key: T) -> Optional[T]:
        left, right, keys = self.left, self.right, self.key
        res = None
        node = self.root
        while node:
            if key > keys[node]:
                res = keys[node]
                node = right[node]
            else:
                node = left[node]
        return res

    def ge(self, key: T) -> Optional[T]:
        left, right, keys = self.left, self.right, self.key
        res = None
        node = self.root
        while node:
            if key == keys[node]:
                res = key
                break
            if key < keys[node]:
                res = keys[node]
                node = left[node]
            else:
                node = right[node]
        return res

    def gt(self, key: T) -> Optional[T]:
        left, right, keys = self.left, self.right, self.key
        res = None
        node = self.root
        while node:
            if key < keys[node]:
                res = keys[node]
                node = left[node]
            else:
                node = right[node]
        return res

    def index(self, key: T) -> int:
        keys, left, right, vals, valsize = (
            self.key,
            self.left,
            self.right,
            self.val,
            self.valsize,
        )
        k = 0
        node = self.root
        while node:
            if key == keys[node]:
                if left[node]:
                    k += valsize[left[node]]
                break
            elif key < keys[node]:
                node = left[node]
            else:
                k += valsize[left[node]] + vals[node]
                node = right[node]
        return k

    def index_right(self, key: T) -> int:
        keys, left, right, vals, valsize = (
            self.key,
            self.left,
            self.right,
            self.val,
            self.valsize,
        )
        k = 0
        node = self.root
        while node:
            if key == keys[node]:
                k += valsize[left[node]] + vals[node]
                break
            elif key < keys[node]:
                node = left[node]
            else:
                k += valsize[left[node]] + vals[node]
                node = right[node]
        return k

    def index_keys(self, key: T) -> int:
        keys, left, right, vals, size = (
            self.key,
            self.left,
            self.right,
            self.val,
            self.size,
        )
        k = 0
        node = self.root
        while node:
            if key == keys[node]:
                if left[node]:
                    k += size[left[node]]
                break
            if key < keys[node]:
                node = left[node]
            else:
                k += size[left[node]] + vals[node]
                node = right[node]
        return k

    def index_right_keys(self, key: T) -> int:
        keys, left, right, vals, size = (
            self.key,
            self.left,
            self.right,
            self.val,
            self.size,
        )
        k = 0
        node = self.root
        while node:
            if key == keys[node]:
                k += size[left[node]] + vals[node]
                break
            if key < keys[node]:
                node = left[node]
            else:
                k += size[left[node]] + vals[node]
                node = right[node]
        return k

    def get_min(self) -> Optional[T]:
        if self.root == 0:
            return
        left = self.left
        node = self.root
        while left[node]:
            node = left[node]
        return self.key[node]

    def get_max(self) -> Optional[T]:
        if self.root == 0:
            return
        right = self.right
        node = self.root
        while right[node]:
            node = right[node]
        return self.key[node]

    def pop(self, k: int = -1) -> T:
        keys, left, right, vals, valsize = (
            self.key,
            self.left,
            self.right,
            self.val,
            self.valsize,
        )
        node = self.root
        if k < 0:
            k += len(self)
        path = []
        d = 0
        while True:
            t = vals[node] + valsize[left[node]]
            if t - vals[node] <= k < t:
                x = keys[node]
                break
            path.append(node)
            if t > k:
                d = 1
                node = left[node]
            else:
                node = right[node]
                k -= t
        if vals[node] == 1:
            self._discard(node, path, d)
        else:
            vals[node] -= 1
            valsize[node] -= 1
            for p in path:
                valsize[p] -= 1
        return x

    def pop_max(self) -> T:
        assert self
        return self.pop()

    def pop_min(self) -> T:
        assert self
        return self.pop(0)

    def items(self) -> Iterator[tuple[T, int]]:
        for i in range(self.len_elm()):
            yield self._kth_elm_tree(i)

    def keys(self) -> Iterator[T]:
        for i in range(self.len_elm()):
            yield self._kth_elm_tree(i)[0]

    def values(self) -> Iterator[int]:
        for i in range(self.len_elm()):
            yield self._kth_elm_tree(i)[1]

    def len_elm(self) -> int:
        return self.size[self.root]

    def clear(self) -> None:
        self.root = 0

    def __contains__(self, key: T) -> bool:
        keys, left, right = self.key, self.left, self.right
        node = self.root
        while node:
            if key == keys[node]:
                return True
            node = left[node] if key < keys[node] else right[node]
        return False

    def __getitem__(self, k: int) -> T:
        return self._kth_elm(k)

    def __iter__(self):
        self.__iter = 0
        return self

    def __next__(self):
        if self.__iter == self.__len__():
            raise StopIteration
        res = self.__getitem__(self.__iter)
        self.__iter += 1
        return res

    def __len__(self):
        return self.valsize[self.root]

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __bool__(self):
        return self.root != 0

    def __repr__(self):
        return f"WBTreeMultiset({self})"

    def isok(self):
        left, right, size, keys = self.left, self.right, self.size, self.key

        def rec(node):
            ls, rs = 0, 0
            height = 0
            if left[node]:
                ls, h = rec(left[node])
                height = max(height, h)
            if right[node]:
                rs, h = rec(right[node])
                height = max(height, h)
            s = ls + rs + 1
            b = (ls + 1) / (s + 1)
            assert s == size[node]
            if not (self.ALPHA <= b <= 1 - self.ALPHA):
                print("NG!")
                print(f"{keys[node]=}, {ls=}, {rs=}, {s=}, {b=}")
                print(f"{self.ALPHA=}, {1-self.ALPHA=}")
                assert False
            return s, height + 1

        if not self.root:
            return
        _, h = rec(self.root)
        # print(f'isok.ok., height={h}')
