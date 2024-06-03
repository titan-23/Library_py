from titan_pylib.my_class.ordered_multiset_interface import OrderedMultisetInterface
from typing import Optional, Iterable
from array import array

try:
    from __pypy__ import newlist_hint
except ImportError:
    pass


class BinaryTrieMultiset(OrderedMultisetInterface):

    def __init__(self, u: int, a: Iterable[int] = []):
        self.left = array("I", bytes(8))
        self.right = array("I", bytes(8))
        self.par = array("I", bytes(8))
        self.size = array("I", bytes(8))
        self.end: int = 2
        self.root: int = 1
        self.bit: int = (u - 1).bit_length()
        self.lim: int = 1 << self.bit
        self.xor: int = 0
        for e in a:
            self.add(e)

    def _make_node(self) -> int:
        if self.end >= len(self.left):
            self.left.append(0)
            self.right.append(0)
            self.par.append(0)
            self.size.append(0)
        self.end += 1
        return self.end - 1

    def _find(self, key: int) -> int:
        assert (
            0 <= key < self.lim
        ), f"ValueError: BinaryTrieMultiset._find({key}), lim={self.lim}"
        left, right = self.left, self.right
        key ^= self.xor
        node = self.root
        for i in range(self.bit - 1, -1, -1):
            if key >> i & 1:
                left, right = right, left
            if not left[node]:
                return -1
            node = left[node]
            if key >> i & 1:
                left, right = right, left
        return node

    def reserve(self, n: int) -> None:
        assert n >= 0, f"ValueError: BinaryTrieMultiset.reserve({n})"
        a = array("I", bytes(4 * n))
        self.left += a
        self.right += a
        self.par += a
        self.size += a

    def add(self, key: int, cnt: int = 1) -> None:
        assert (
            0 <= key < self.lim
        ), f"ValueError: BinaryTrieMultiset.add({key}), lim={self.lim}"
        left, right, par, size = self.left, self.right, self.par, self.size
        key ^= self.xor
        node = self.root
        for i in range(self.bit - 1, -1, -1):
            if key >> i & 1:
                left, right = right, left
            if not left[node]:
                left[node] = self._make_node()
                par[left[node]] = node
            node = left[node]
            if key >> i & 1:
                left, right = right, left
        size[node] += cnt
        for i in range(self.bit):
            node = par[node]
            size[node] += cnt

    def _discard(self, node: int) -> None:
        left, right, par, size = self.left, self.right, self.par, self.size
        cnt = size[node]
        for _ in range(self.bit):
            size[node] -= cnt
            if left[par[node]] == node:
                node = par[node]
                left[node] = 0
                if right[node]:
                    break
            else:
                node = par[node]
                right[node] = 0
                if left[node]:
                    break
        while node:
            size[node] -= cnt
            node = par[node]

    def discard(self, key: int, cnt: int = 1) -> bool:
        assert (
            0 <= key < self.lim
        ), f"ValueError: BinaryTrieMultiset.discard({key}), lim={self.lim}"
        par, size = self.par, self.size
        node = self._find(key)
        if node == -1:
            return False
        if size[node] <= cnt:
            self._discard(node)
        else:
            while node:
                size[node] -= cnt
                node = par[node]
        return True

    def discard_all(self, key: int) -> bool:
        return self.discard(key, self.count(key))

    def remove(self, key: int, cnt: int = 1) -> None:
        c = self.count(key)
        if c < cnt:
            raise KeyError(key)
        self.discard(key, cnt)

    def count(self, key: int) -> int:
        node = self._find(key)
        return 0 if node == -1 else self.size[node]

    def pop(self, k: int = -1) -> int:
        assert (
            -len(self) <= k < len(self)
        ), f"IndexError: BinaryTrieMultiset.pop({k}), len={len(self)}"
        if k < 0:
            k += len(self)
        left, right, par, size = self.left, self.right, self.par, self.size
        node = self.root
        res = 0
        for i in range(self.bit - 1, -1, -1):
            b = self.xor >> i & 1
            if b:
                left, right = right, left
            t = size[left[node]]
            res <<= 1
            if not left[node]:
                node = right[node]
                res |= 1
            elif not right[node]:
                node = left[node]
            else:
                t = size[left[node]]
                if t <= k:
                    k -= t
                    res |= 1
                    node = right[node]
                else:
                    node = left[node]
            if b:
                left, right = right, left
        if size[node] == 1:
            self._discard(node)
        else:
            while node:
                size[node] -= 1
                node = par[node]
        return res ^ self.xor

    def pop_min(self) -> int:
        assert self, f"IndexError: BinaryTrieMultiset.pop_min(), len={len(self)}"
        return self.pop(0)

    def pop_max(self) -> int:
        return self.pop()

    def all_xor(self, x: int) -> None:
        assert (
            0 <= x < self.lim
        ), f"ValueError: BinaryTrieMultiset.all_xor({x}), lim={self.lim}"
        self.xor ^= x

    def get_min(self) -> Optional[int]:
        if not self:
            return None
        left, right = self.left, self.right
        key = self.xor
        ans = 0
        node = self.root
        for i in range(self.bit - 1, -1, -1):
            ans <<= 1
            if key >> i & 1:
                if right[node]:
                    node = right[node]
                    ans |= 1
                else:
                    node = left[node]
            else:
                if left[node]:
                    node = left[node]
                else:
                    node = right[node]
                    ans |= 1
        return ans ^ self.xor

    def get_max(self) -> Optional[int]:
        if not self:
            return None
        left, right = self.left, self.right
        key = self.xor
        ans = 0
        node = self.root
        for i in range(self.bit - 1, -1, -1):
            ans <<= 1
            if key >> i & 1:
                if left[node]:
                    node = left[node]
                else:
                    node = right[node]
                    ans |= 1
            else:
                if right[node]:
                    ans |= 1
                    node = right[node]
                else:
                    node = left[node]
        return ans ^ self.xor

    def index(self, key: int) -> int:
        assert (
            0 <= key < self.lim
        ), f"ValueError: BinaryTrieMultiset.index({key}), lim={self.lim}"
        left, right, size = self.left, self.right, self.size
        k = 0
        node = self.root
        key ^= self.xor
        for i in range(self.bit - 1, -1, -1):
            if key >> i & 1:
                k += size[left[node]]
                node = right[node]
            else:
                node = left[node]
            if not node:
                break
        return k

    def index_right(self, key: int) -> int:
        assert (
            0 <= key < self.lim
        ), f"ValueError: BinaryTrieMultiset.index_right({key}), lim={self.lim}"
        left, right, size = self.left, self.right, self.size
        k = 0
        node = self.root
        key ^= self.xor
        for i in range(self.bit - 1, -1, -1):
            if key >> i & 1:
                k += size[left[node]]
                node = right[node]
            else:
                node = left[node]
            if not node:
                break
        else:
            k += size[node]
        return k

    def gt(self, key: int) -> Optional[int]:
        assert (
            0 <= key < self.lim
        ), f"ValueError: BinaryTrieMultiset.gt({key}), lim={self.lim}"
        i = self.index_right(key)
        return None if i >= self.size[self.root] else self.__getitem__(i)

    def lt(self, key: int) -> Optional[int]:
        assert (
            0 <= key < self.lim
        ), f"ValueError: BinaryTrieMultiset.lt({key}), lim={self.lim}"
        i = self.index(key) - 1
        return None if i < 0 else self.__getitem__(i)

    def ge(self, key: int) -> Optional[int]:
        assert (
            0 <= key < self.lim
        ), f"ValueError: BinaryTrieMultiset.ge({key}), lim={self.lim}"
        if key == 0:
            return self.get_min() if self else None
        i = self.index_right(key - 1)
        return None if i >= self.size[self.root] else self.__getitem__(i)

    def le(self, key: int) -> Optional[int]:
        assert (
            0 <= key < self.lim
        ), f"ValueError: BinaryTrieMultiset.le({key}), lim={self.lim}"
        i = self.index(key + 1) - 1
        return None if i < 0 else self.__getitem__(i)

    def tolist(self) -> list[int]:
        a = newlist_hint(len(self))
        if not self:
            return a
        val = self.get_min()
        while val is not None:
            for _ in range(self.count(val)):
                a.append(val)
            val = self.gt(val)
        return a

    def clear(self) -> None:
        self.root = 1

    def __contains__(self, key: int):
        assert (
            0 <= key < self.lim
        ), f"ValueError: BinaryTrieMultiset.__contains__({key}), lim={self.lim}"
        return self._find(key) != -1

    def __getitem__(self, k: int):
        assert (
            -len(self) <= k < len(self)
        ), f"IndexError: BinaryTrieMultiset.__getitem__({k}), len={len(self)}"
        if k < 0:
            k += len(self)
        left, right, size = self.left, self.right, self.size
        node = self.root
        res = 0
        for i in range(self.bit - 1, -1, -1):
            b = self.xor >> i & 1
            if b:
                left, right = right, left
            t = size[left[node]]
            res <<= 1
            if not left[node]:
                node = right[node]
                res |= 1
            elif not right[node]:
                node = left[node]
            else:
                t = size[left[node]]
                if t <= k:
                    k -= t
                    res |= 1
                    node = right[node]
                else:
                    node = left[node]
            if b:
                left, right = right, left
        return res

    def __bool__(self):
        return self.size[self.root] != 0

    def __iter__(self):
        self.it = 0
        return self

    def __next__(self):
        if self.it == len(self):
            raise StopIteration
        self.it += 1
        return self.__getitem__(self.it - 1)

    def __len__(self):
        return self.size[self.root]

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __repr__(self):
        return f"BinaryTrieMultiset({(1<<self.bit)-1}, {self.tolist()})"
