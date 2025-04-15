from array import array
from typing import Generic, Iterable, TypeVar, Optional, Final

T = TypeVar("T")

DELTA: Final[int] = 3
GAMMA: Final[int] = 2


class WBTSet(Generic[T]):

    def __init__(self, a: Iterable[T] = []) -> None:
        self.root = 0
        self.key = [0]
        self.size = array("I", bytes(4))
        self.left = array("I", bytes(4))
        self.right = array("I", bytes(4))
        self.end = 1
        if not isinstance(a, list):
            a = list(a)
        if a:
            self._build(a)

    def reserve(self, n: int) -> None:
        if n <= 0:
            return
        self.key += [0] * n
        a = array("I", bytes(4 * n))
        self.left += a
        self.right += a
        self.size += array("I", [1] * n)

    def _build(self, a: list[T]) -> None:
        left, right, size = self.left, self.right, self.size

        def sort(l: int, r: int) -> int:
            mid = (l + r) >> 1
            node = mid
            if l != mid:
                left[node] = sort(l, mid)
                size[node] += size[left[node]]
            if mid + 1 != r:
                right[node] = sort(mid + 1, r)
                size[node] += size[right[node]]
            return node

        n = len(a)
        if n == 0:
            return
        if not all(a[i] < a[i + 1] for i in range(n - 1)):
            b = sorted(a)
            a = [b[0]]
            for i in range(1, n):
                if b[i] != a[-1]:
                    a.append(b[i])
        n = len(a)
        end = self.end
        self.end += n
        self.reserve(n)
        self.key[end : end + n] = a
        self.root = sort(end, n + end)

    def _rotate_left(self, node: int) -> int:
        left, right, size = self.left, self.right, self.size
        u = right[node]
        size[u] = size[node]
        size[node] -= size[right[u]] + 1
        right[node] = left[u]
        left[u] = node
        return u

    def _rotate_right(self, node: int) -> int:
        left, right, size = self.left, self.right, self.size
        u = left[node]
        size[u] = size[node]
        size[node] -= size[left[u]] + 1
        left[node] = right[u]
        right[u] = node
        return u

    def _make_node(self, key: T) -> int:
        end = self.end
        if end >= len(self.key):
            self.key.append(key)
            self.size.append(1)
            self.left.append(0)
            self.right.append(0)
        else:
            self.key[end] = key
        self.end += 1
        return end

    def _weight_left(self, node: int) -> int:
        return self.size[self.left[node]] + 1

    def _weight_right(self, node: int) -> int:
        return self.size[self.right[node]] + 1

    def ave_height(self):
        if not self.root:
            return 0
        left, right, size, keys = self.left, self.right, self.size, self.key
        ans = 0

        def dfs(node, dep):
            nonlocal ans
            ans += dep
            if left[node]:
                dfs(left[node], dep + 1)
            if right[node]:
                dfs(right[node], dep + 1)

        dfs(self.root, 1)
        ans /= len(self)
        return ans

    def debug(self, root):
        left, right, size, keys = self.left, self.right, self.size, self.key

        def dfs(node, indent):
            if not node:
                return
            s = " " * indent
            print(f"{s}key={keys[node]}, idx={node}")
            if left[node]:
                print(f"{s}left: {keys[left[node]]}, idx={left[node]}")
                dfs(left[node], indent + 2)
            if right[node]:
                print(f"{s}righ: {keys[right[node]]}, idx={right[node]}")
                dfs(right[node], indent + 2)

        dfs(root, 0)

    def add(self, key: T) -> bool:
        if self.root == 0:
            self.root = self._make_node(key)
            return True
        left, right, size, keys = self.left, self.right, self.size, self.key
        node = self.root
        path = []
        di = 0
        while node:
            if key == keys[node]:
                return False
            path.append(node)
            di <<= 1
            if key < keys[node]:
                di |= 1
                node = left[node]
            else:
                node = right[node]
        # self.debug(self.root)
        if di & 1:
            left[path[-1]] = self._make_node(key)
        else:
            right[path[-1]] = self._make_node(key)
        while path:
            node = path.pop()
            size[node] += 1
            di >>= 1
            wl = self._weight_left(node)
            wr = self._weight_right(node)
            if wl * DELTA < wr:
                # print("wl * DELTA < wr")
                # self.debug(node)
                if (
                    self._weight_left(right[node])
                    >= self._weight_right(right[node]) * GAMMA
                ):
                    right[node] = self._rotate_right(right[node])
                node = self._rotate_left(node)
                # self.debug(node)
                # assert node
            elif wr * DELTA < wl:
                # print("wr * DELTA < wl")
                if (
                    self._weight_right(left[node])
                    >= self._weight_left(left[node]) * GAMMA
                ):
                    # print("left")
                    left[node] = self._rotate_left(left[node])
                # print("right")
                node = self._rotate_right(node)
                # assert node
            if path:
                if di & 1:
                    left[path[-1]] = node
                else:
                    right[path[-1]] = node
            else:
                self.root = node
        return True

    def remove(self, key: T) -> bool:
        if self.discard(key):
            return True
        raise KeyError(key)

    def discard(self, key: T) -> bool:
        left, right, size, keys = self.left, self.right, self.size, self.key
        di = 0
        path = []
        node = self.root
        while node:
            if key == keys[node]:
                break
            path.append(node)
            di <<= 1
            if key < keys[node]:
                di |= 1
                node = left[node]
            else:
                node = right[node]
        else:
            return False
        if left[node] and right[node]:
            path.append(node)
            di <<= 1
            di |= 1
            lmax = left[node]
            while right[lmax]:
                path.append(lmax)
                di <<= 1
                lmax = right[lmax]
            keys[node] = keys[lmax]
            node = lmax
        cnode = right[node] if left[node] == 0 else left[node]
        if path:
            if di & 1:
                left[path[-1]] = cnode
            else:
                right[path[-1]] = cnode
        else:
            self.root = cnode
            return True
        while path:
            node = path.pop()
            size[node] -= 1
            di >>= 1
            wl = self._weight_left(node)
            wr = self._weight_right(node)
            if wl * DELTA < wr:
                if (
                    self._weight_left(right[node])
                    >= self._weight_right(right[node]) * GAMMA
                ):
                    right[node] = self._rotate_right(right[node])
                node = self._rotate_left(node)
            elif wr * DELTA < wl:
                if (
                    self._weight_right(left[node])
                    >= self._weight_left(left[node]) * GAMMA
                ):
                    left[node] = self._rotate_left(left[node])
                node = self._rotate_right(node)
            if path:
                if di & 1:
                    left[path[-1]] = node
                else:
                    right[path[-1]] = node
            else:
                self.root = node
        return True

    def le(self, key: T) -> Optional[T]:
        keys, left, right = self.key, self.left, self.right
        res = None
        node = self.root
        while node:
            if key == keys[node]:
                return keys[node]
            if key < keys[node]:
                node = left[node]
            else:
                res = keys[node]
                node = right[node]
        return res

    def lt(self, key: T) -> Optional[T]:
        keys, left, right = self.key, self.left, self.right
        res = None
        node = self.root
        while node:
            if key <= keys[node]:
                node = left[node]
            else:
                res = keys[node]
                node = right[node]
        return res

    def ge(self, key: T) -> Optional[T]:
        keys, left, right = self.key, self.left, self.right
        res = None
        node = self.root
        while node:
            if key == keys[node]:
                return keys[node]
            if key < keys[node]:
                res = keys[node]
                node = left[node]
            else:
                node = right[node]
        return res

    def gt(self, key: T) -> Optional[T]:
        keys, left, right = self.key, self.left, self.right
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
        keys, left, right, size = self.key, self.left, self.right, self.size
        k = 0
        node = self.root
        while node:
            if key == keys[node]:
                k += size[left[node]]
                break
            if key < keys[node]:
                node = left[node]
            else:
                k += size[left[node]] + 1
                node = right[node]
        return k

    def index_right(self, key: T) -> int:
        keys, left, right, size = self.key, self.left, self.right, self.size
        k, node = 0, self.root
        while node:
            if key == keys[node]:
                k += size[left[node]] + 1
                break
            if key < keys[node]:
                node = left[node]
            else:
                k += size[left[node]] + 1
                node = right[node]
        return k

    def get_max(self) -> Optional[T]:
        if not self:
            return
        return self[len(self) - 1]

    def get_min(self) -> Optional[T]:
        if not self:
            return
        return self[0]

    def pop(self, k: int = -1) -> T:
        left, right, size, key = self.left, self.right, self.size, self.key
        if k < 0:
            k += size[self.root]
        assert 0 <= k and k < size[self.root], "IndexError"
        path = []
        di = 0
        node = self.root
        while True:
            t = size[left[node]]
            if t == k:
                res = key[node]
                break
            path.append(node)
            di <<= 1
            if t < k:
                k -= t + 1
                node = right[node]
            else:
                di |= 1
                node = left[node]
        if left[node] and right[node]:
            path.append(node)
            di <<= 1
            di |= 1
            lmax = left[node]
            while right[lmax]:
                path.append(lmax)
                di <<= 1
                lmax = right[lmax]
            key[node] = key[lmax]
            node = lmax
        cnode = right[node] if left[node] == 0 else left[node]
        if path:
            if di & 1:
                left[path[-1]] = cnode
            else:
                right[path[-1]] = cnode
        else:
            self.root = cnode
            return res
        while path:
            node = path.pop()
            size[node] -= 1
            di >>= 1
            wl = self._weight_left(node)
            wr = self._weight_right(node)
            if wl * DELTA < wr:
                if (
                    self._weight_left(right[node])
                    >= self._weight_right(right[node]) * GAMMA
                ):
                    right[node] = self._rotate_right(right[node])
                node = self._rotate_left(node)
            elif wr * DELTA < wl:
                if (
                    self._weight_right(left[node])
                    >= self._weight_left(left[node]) * GAMMA
                ):
                    left[node] = self._rotate_left(left[node])
                node = self._rotate_right(node)
            if path:
                if di & 1:
                    left[path[-1]] = node
                else:
                    right[path[-1]] = node
            else:
                self.root = node
        return res

    def pop_max(self) -> T:
        return self.pop()

    def pop_min(self) -> T:
        return self.pop(0)

    def clear(self) -> None:
        self.root = 0

    def tolist(self) -> list[T]:
        left, right, keys = self.left, self.right, self.key
        node = self.root
        stack, a = [], []
        while stack or node:
            if node:
                stack.append(node)
                node = left[node]
            else:
                node = stack.pop()
                a.append(keys[node])
                node = right[node]
        return a

    def check(self) -> int:
        """作業用デバック関数"""
        if self.root == 0:
            return 0

        def _balance_check(node: int) -> None:
            if node == 0:
                return
            if not self._weight_left(node) * DELTA >= self._weight_right(node):
                print(self._weight_left(node), self._weight_right(node), flush=True)
                assert False, f"self._weight_left() * DELTA >= self._weight_right()"
            if not self._weight_right(node) * DELTA >= self._weight_left(node):
                print(self._weight_left(node), self._weight_right(node), flush=True)
                assert False, f"self._weight_right() * DELTA >= self._weight_left()"

        keys = self.key

        # _size, height
        def dfs(node) -> tuple[int, int]:
            _balance_check(node)
            h = 0
            s = 1
            if self.left[node]:
                assert keys[self.left[node]] < keys[node]
                ls, lh = dfs(self.left[node])
                s += ls
                h = max(h, lh)
            if self.right[node]:
                assert keys[node] < keys[self.right[node]]
                rs, rh = dfs(self.right[node])
                s += rs
                h = max(h, rh)
            assert self.size[node] == s
            return s, h + 1

        _, h = dfs(self.root)
        return h

    def __contains__(self, key: T) -> bool:
        keys, left, right = self.key, self.left, self.right
        node = self.root
        while node:
            if key == keys[node]:
                return True
            node = left[node] if key < keys[node] else right[node]
        return False

    def __getitem__(self, k: int) -> T:
        left, right, size, key = self.left, self.right, self.size, self.key
        if k < 0:
            k += size[self.root]
        assert (
            0 <= k and k < size[self.root]
        ), f"IndexError: WBTSet[{k}], len={len(self)}"
        node = self.root
        while True:
            t = size[left[node]]
            if t == k:
                return key[node]
            if t < k:
                k -= t + 1
                node = right[node]
            else:
                node = left[node]

    def __iter__(self):
        self.__iter = 0
        return self

    def __next__(self):
        if self.__iter == self.__len__():
            raise StopIteration
        res = self[self.__iter]
        self.__iter += 1
        return res

    def __reversed__(self):
        for i in range(self.__len__()):
            yield self[-i - 1]

    def __len__(self):
        return self.size[self.root]

    def __bool__(self):
        return self.root != 0

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __repr__(self):
        return f"WBTSet({self})"
