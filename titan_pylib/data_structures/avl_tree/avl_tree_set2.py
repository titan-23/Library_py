from titan_pylib.my_class.supports_less_than import SupportsLessThan
from titan_pylib.my_class.ordered_set_interface import OrderedSetInterface
from array import array
from typing import Generic, Iterable, TypeVar, Optional

T = TypeVar("T", bound=SupportsLessThan)


class AVLTreeSet2(OrderedSetInterface, Generic[T]):
    """AVLTreeSet2
    集合としての AVL 木です。
    配列を用いてノードを表現しています。
    size を持たないので軽めです。
    """

    def __init__(self, a: Iterable[T] = []) -> None:
        self.root = 0
        self._len = 0
        self.key = [0]
        self.left = array("I", bytes(4))
        self.right = array("I", bytes(4))
        self.balance = array("b", bytes(1))
        self.end = 1
        if not isinstance(a, list):
            a = list(a)
        if a:
            self._build(a)

    def reserve(self, n: int) -> None:
        self.key += [0] * n
        a = array("I", bytes(4 * n))
        self.left += a
        self.right += a
        self.balance += array("b", bytes(n))

    def _build(self, a: list[T]) -> None:
        left, right, balance = self.left, self.right, self.balance

        def sort(l: int, r: int) -> tuple[int, int]:
            mid = (l + r) >> 1
            node = mid
            hl, hr = 0, 0
            if l != mid:
                left[node], hl = sort(l, mid)
            if mid + 1 != r:
                right[node], hr = sort(mid + 1, r)
            balance[node] = hl - hr
            return node, max(hl, hr) + 1

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
        self._len = n
        end = self.end
        self.end += n
        self.reserve(n)
        self.key[end : end + n] = a
        self.root = sort(end, n + end)[0]

    def _rotate_L(self, node: int) -> int:
        left, right, balance = self.left, self.right, self.balance
        u = left[node]
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
        left, right, balance = self.left, self.right, self.balance
        u = right[node]
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
        left, right = self.left, self.right
        B = left[node]
        E = right[B]
        right[B] = left[E]
        left[E] = B
        left[node] = right[E]
        right[E] = node
        self._update_balance(E)
        return E

    def _rotate_RL(self, node: int) -> int:
        left, right = self.left, self.right
        C = right[node]
        D = left[C]
        left[C] = right[D]
        right[D] = C
        right[node] = left[D]
        left[D] = node
        self._update_balance(D)
        return D

    def _make_node(self, key: T) -> int:
        end = self.end
        if end >= len(self.key):
            self.key.append(key)
            self.left.append(0)
            self.right.append(0)
            self.balance.append(0)
        else:
            self.key[end] = key
        self.end += 1
        return end

    def add(self, key: T) -> bool:
        if self.root == 0:
            self.root = self._make_node(key)
            self._len = 1
            return True
        left, right, balance, keys = self.left, self.right, self.balance, self.key
        node = self.root
        path = []
        di = 0
        while node:
            if key == keys[node]:
                return False
            di <<= 1
            path.append(node)
            if key < keys[node]:
                di |= 1
                node = left[node]
            else:
                node = right[node]
        self._len += 1
        if di & 1:
            left[path[-1]] = self._make_node(key)
        else:
            right[path[-1]] = self._make_node(key)
        new_node = 0
        while path:
            pnode = path.pop()
            balance[pnode] += 1 if di & 1 else -1
            di >>= 1
            if balance[pnode] == 0:
                break
            if balance[pnode] == 2:
                new_node = (
                    self._rotate_LR(pnode)
                    if balance[left[pnode]] == -1
                    else self._rotate_L(pnode)
                )
                break
            elif balance[pnode] == -2:
                new_node = (
                    self._rotate_RL(pnode)
                    if balance[right[pnode]] == 1
                    else self._rotate_R(pnode)
                )
                break
        if new_node:
            if path:
                gnode = path.pop()
                if di & 1:
                    left[gnode] = new_node
                else:
                    right[gnode] = new_node
            else:
                self.root = new_node
        return True

    def remove(self, key: T) -> bool:
        if self.discard(key):
            return True
        raise KeyError(key)

    def discard(self, key: T) -> bool:
        left, right, balance, keys = self.left, self.right, self.balance, self.key
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
        self._len -= 1
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
            new_node = 0
            pnode = path.pop()
            balance[pnode] -= 1 if di & 1 else -1
            di >>= 1
            if balance[pnode] == 2:
                new_node = (
                    self._rotate_LR(pnode)
                    if balance[left[pnode]] == -1
                    else self._rotate_L(pnode)
                )
            elif balance[pnode] == -2:
                new_node = (
                    self._rotate_RL(pnode)
                    if balance[right[pnode]] == 1
                    else self._rotate_R(pnode)
                )
            elif balance[pnode]:
                break
            if new_node:
                if not path:
                    self.root = new_node
                    return True
                if di & 1:
                    left[path[-1]] = new_node
                else:
                    right[path[-1]] = new_node
                if balance[new_node]:
                    break
        return True

    def le(self, key: T) -> Optional[T]:
        keys, left, right = self.key, self.left, self.right
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
                res = key
                break
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

    def get_max(self) -> Optional[T]:
        if not self:
            return
        right = self.right
        node = self.root
        while right[node]:
            node = right[node]
        return self.key[node]

    def get_min(self) -> Optional[T]:
        if not self:
            return
        left = self.left
        node = self.root
        while left[node]:
            node = left[node]
        return self.key[node]

    def pop_min(self) -> T:
        self._len -= 1
        left, right, balance, keys = self.left, self.right, self.balance, self.key
        path = []
        node = self.root
        while left[node]:
            path.append(node)
            node = left[node]
        res = keys[node]
        cnode = right[node]
        if path:
            left[path[-1]] = cnode
        else:
            self.root = cnode
            return res
        while path:
            new_node = 0
            pnode = path.pop()
            balance[pnode] -= 1
            if balance[pnode] == 2:
                new_node = (
                    self._rotate_LR(pnode)
                    if balance[left[pnode]] == -1
                    else self._rotate_L(pnode)
                )
            elif balance[pnode] == -2:
                new_node = (
                    self._rotate_RL(pnode)
                    if balance[right[pnode]] == 1
                    else self._rotate_R(pnode)
                )
            elif balance[pnode]:
                break
            if new_node:
                if not path:
                    self.root = new_node
                    return res
                left[path[-1]] = new_node
                if balance[new_node]:
                    break
        return res

    def pop_max(self) -> T:
        self._len -= 1
        left, right, balance, keys = self.left, self.right, self.balance, self.key
        path = []
        node = self.root
        while right[node]:
            path.append(node)
            node = right[node]
        res = keys[node]
        cnode = right[node] if left[node] == 0 else left[node]
        if path:
            right[path[-1]] = cnode
        else:
            self.root = cnode
            return res
        while path:
            new_node = 0
            pnode = path.pop()
            balance[pnode] += 1
            if balance[pnode] == 2:
                new_node = (
                    self._rotate_LR(pnode)
                    if balance[left[pnode]] == -1
                    else self._rotate_L(pnode)
                )
            elif balance[pnode] == -2:
                new_node = (
                    self._rotate_RL(pnode)
                    if balance[right[pnode]] == 1
                    else self._rotate_R(pnode)
                )
            elif balance[pnode]:
                break
            if new_node:
                if not path:
                    self.root = new_node
                    return res
                right[path[-1]] = new_node
                if balance[new_node]:
                    break
        return res

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

    def __contains__(self, key: T) -> bool:
        keys, left, right = self.key, self.left, self.right
        node = self.root
        while node:
            if key == keys[node]:
                return True
            node = left[node] if key < keys[node] else right[node]
        return False

    def __iter__(self):
        self.it = self.get_min()
        return self

    def __next__(self):
        if self.it is None:
            raise StopIteration
        res = self.it
        self.it = self.gt(res)
        return res

    def __len__(self):
        return self._len

    def __bool__(self):
        return self.root != 0

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def __repr__(self):
        return f"AVLTreeSet2({self})"
