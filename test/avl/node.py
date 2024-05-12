from typing import Generic, Iterable, TypeVar, Optional, Sequence

T = TypeVar("T")


class AVLTreeNode:

    def __init__(self) -> None:
        self.size: int = 1
        self.par: Optional[AVLTreeNode] = None
        self.left: Optional[AVLTreeNode] = None
        self.right: Optional[AVLTreeNode] = None
        self.height: int = 1

    def _balance(self) -> int:
        hl = self.left.height if self.left else 0
        hr = self.right.height if self.right else 0
        return hl - hr

    def _update(self) -> None:
        self.size = (
            1
            + (self.left.size if self.left else 0)
            + (self.right.size if self.right else 0)
        )
        self.height = 1 + max(
            (self.left.height if self.left else 0),
            (self.right.height if self.right else 0),
        )

    def _rotate_right(self) -> "AVLTreeNode":
        u = self.left
        u.par = self.par
        self.left = u.right
        if u.right:
            u.right.par = self
        u.right = self
        self.par = u
        self._update()
        u._update()
        return u

    def _rotate_left(self) -> "AVLTreeNode":
        u = self.right
        u.par = self.par
        self.right = u.left
        if u.left:
            u.left.par = self
        u.left = self
        self.par = u
        self._update()
        u._update()
        return u

    def _rotate_LR(self) -> "AVLTreeNode":
        self.left = self.left._rotate_left()
        return self._rotate_right()

    def _rotate_RL(self) -> "AVLTreeNode":
        self.right = self.right._rotate_right()
        return self._rotate_left()

    def _min(self) -> "AVLTreeNode":
        node = self
        while node.left:
            node = node.left
        return node

    def _max(self) -> "AVLTreeNode":
        node = self
        while node.right:
            node = node.right
        return node

    def _next(self) -> Optional["AVLTreeNode"]:
        now = self
        pre = None
        flag = now.right is pre
        while now.right is pre:
            pre, now = now, now.par
        if not now:
            return None
        return now if flag and pre is now.left else now.right._min()

    def _prev(self) -> Optional["AVLTreeNode"]:
        now, pre = self, None
        flag = now.left is pre
        while now.left is pre:
            pre, now = now, now.par
        if not now:
            return None
        return now if flag and pre is now.right else now.left._max()

    def __iadd__(self, other: int) -> Optional["AVLTreeNode"]:
        node = self
        for _ in range(other):
            assert node
            node = node._next()
        return node

    def __isub__(self, other: int) -> Optional["AVLTreeNode"]:
        node = self
        for _ in range(other):
            assert node
            node = node._prev()
        return node

    def __add__(self, other: int) -> Optional["AVLTreeNode"]:
        node = self
        for _ in range(other):
            assert node
            node = node._next()
        return node

    def __sub__(self, other: int) -> Optional["AVLTreeNode"]:
        node = self
        for _ in range(other):
            assert node
            node = node._prev()
        return node

    def __str__(self) -> str:
        # if self.left is None and self.right is None:
        #   return f'key:{self.key, self.size}\n'
        # return f'key:{self.key, self.size},\n left:{self.left},\n right:{self.right}\n'
        return f"{self.__class__.__name__}({self.key})"


class AVLTreeSet(Generic[T]):

    class AVLTreeSetNode(AVLTreeNode):

        def __init__(self, key: T) -> None:
            super().__init__()
            self.key = key

    def __init__(self, a: Iterable[T] = []) -> None:
        self.root: Optional[AVLTreeSet.AVLTreeSetNode] = None
        if not isinstance(a, Sequence):
            a = list(a)
        if a:
            self._build(a)

    def _build(self, a: Sequence[T]) -> None:
        AVLTreeSetNode = AVLTreeSet.AVLTreeSetNode

        def build(l: int, r: int) -> AVLTreeSet.AVLTreeSetNode:
            mid = (l + r) >> 1
            node = AVLTreeSetNode(a[mid])
            if l != mid:
                node.left = build(l, mid)
                node.left.par = node
            if mid + 1 != r:
                node.right = build(mid + 1, r)
                node.right.par = node
            node._update()
            return node

        if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
            a = sorted(a)
            new_a = [a[0]]
            for elm in a:
                if new_a[-1] == elm:
                    continue
                new_a.append(elm)
            a = new_a
        self.root = build(0, len(a))

    def _remove_balance(self, node: AVLTreeSetNode) -> None:
        while node:
            new_node = None
            node._update()
            if node._balance() == 2:
                new_node = (
                    node._rotate_LR()
                    if node.left._balance() == -1
                    else node._rotate_right()
                )
            elif node._balance() == -2:
                new_node = (
                    node._rotate_RL()
                    if node.right._balance() == 1
                    else node._rotate_left()
                )
            elif node._balance() != 0:
                node = node.par
                break
            if not new_node:
                node = node.par
                continue
            if not new_node.par:
                self.root = new_node
                return
            node = new_node.par
            if new_node.key < node.key:
                node.left = new_node
            else:
                node.right = new_node
            if new_node._balance() != 0:
                break
        while node:
            node._update()
            node = node.par

    def _add_balance(self, node: AVLTreeSetNode) -> None:
        new_node = None
        while node:
            node._update()
            if node._balance() == 0:
                node = node.par
                break
            if node._balance() == 2:
                new_node = (
                    node._rotate_LR()
                    if node.left._balance() == -1
                    else node._rotate_right()
                )
                break
            elif node._balance() == -2:
                new_node = (
                    node._rotate_RL()
                    if node.right._balance() == 1
                    else node._rotate_left()
                )
                break
            node = node.par
        if new_node:
            node = new_node.par
            if node:
                if new_node.key < node.key:
                    node.left = new_node
                else:
                    node.right = new_node
            else:
                self.root = new_node
        while node:
            node._update()
            node = node.par

    def add(self, key: T) -> bool:
        if not self.root:
            self.root = AVLTreeSet.AVLTreeSetNode(key)
            return True
        pnode = None
        node = self.root
        while node:
            if key == node.key:
                return False
            pnode = node
            node = node.left if key < node.key else node.right
        if key < pnode.key:
            pnode.left = AVLTreeSet.AVLTreeSetNode(key)
            pnode.left.par = pnode
        else:
            pnode.right = AVLTreeSet.AVLTreeSetNode(key)
            pnode.right.par = pnode
        self._add_balance(pnode)
        return True

    def remove_iter(self, node: AVLTreeNode) -> None:
        pnode = node.par
        if node.left and node.right:
            pnode = node
            mnode = node.left
            while mnode.right:
                pnode = mnode
                mnode = mnode.right
            node.key = mnode.key
            node = mnode
        cnode = node.right if not node.left else node.left
        if cnode:
            cnode.par = pnode
        if pnode:
            if node.key <= pnode.key:
                pnode.left = cnode
            else:
                pnode.right = cnode
            self._remove_balance(pnode)
        else:
            self.root = cnode

    def discard(self, key: T) -> bool:
        node = self.find_key(key)
        if node is None:
            return False
        self.remove_iter(node)
        return True

    def remove(self, key: T) -> None:
        node = self.find_key(key)
        assert node
        self.remove_iter(node)

    def le(self, key: T) -> Optional[T]:
        res = None
        node = self.root
        while node:
            if key == node.key:
                res = key
                break
            if key < node.key:
                node = node.left
            else:
                res = node.key
                node = node.right
        return res

    def lt(self, key: T) -> Optional[T]:
        res = None
        node = self.root
        while node:
            if key <= node.key:
                node = node.left
            else:
                res = node.key
                node = node.right
        return res

    def ge(self, key: T) -> Optional[T]:
        res = None
        node = self.root
        while node:
            if key == node.key:
                res = key
                break
            if key < node.key:
                res = node.key
                node = node.left
            else:
                node = node.right
        return res

    def gt(self, key: T) -> Optional[T]:
        res = None
        node = self.root
        while node:
            if key < node.key:
                res = node.key
                node = node.left
            else:
                node = node.right
        return res

    def index(self, key: T) -> int:
        k = 0
        node = self.root
        while node:
            if key == node.key:
                k += 0 if node.left is None else node.left.size
                break
            elif key < node.key:
                node = node.left
            else:
                k += 1 if node.left is None else node.left.size + 1
                node = node.right
        return k

    def index_right(self, key: T) -> int:
        k = 0
        node = self.root
        while node:
            if key == node.key:
                k += 1 if node.left is None else node.left.size + 1
                break
            elif key < node.key:
                node = node.left
            else:
                k += 1 if node.left is None else node.left.size + 1
                node = node.right
        return k

    def find_key(self, key: T) -> Optional[AVLTreeSetNode]:
        node = self.root
        while node:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    def find_kth(self, k: int) -> AVLTreeSetNode:
        node = self.root
        while True:
            t = 0 if node.left is None else node.left.size
            if t == k:
                return node
            if t < k:
                k -= t + 1
                node = node.right
            else:
                node = node.left

    def pop(self, k: int = -1) -> T:
        assert (
            self.root
        ), f"IndexError: {self.__class__.__name__}.pop({k}), pop({k}) from Empty {self.__class__.__name__}"
        node = self.find_kth(k)
        key = node.key
        self.remove_iter(node)
        return key

    def tolist(self) -> list[T]:
        a = []
        stack = []
        node = self.root
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                a.append(node.key)
                node = node.right
        return a

    def __contains__(self, key: T) -> bool:
        return self.find_key(key) is not None

    def __getitem__(self, k: int) -> T:
        assert (
            0 <= k < len(self)
        ), f"IndexError: {self.__class__.__name__}.__getitem__({k}), len={len(self)}"
        return self.find_kth(k).key

    def __iter__(self):
        self.__iter = 0
        return self

    def __next__(self):
        if self.__iter == self.__len__():
            raise StopIteration
        res = self[self.__iter]
        self.__iter += 1
        return res

    def __len__(self):
        return self.root.size if self.root else 0

    def __str__(self):
        return "{" + ", ".join(map(str, self.tolist())) + "}"

    def check(self) -> None:
        if not self.root:
            print("height=0")
            print("check ok empty.")
            return

        # print(f'height={self.root.height}')
        def dfs(node: AVLTreeSet.AVLTreeSetNode):
            h = 0
            b = 0
            s = 1
            if node.left:
                assert node.left.par is node
                assert node.key > node.left.key
                dfs(node.left)
                h = max(h, node.left.height)
                b += node.left.height
                s += node.left.size
            if node.right:
                assert node.right.par is node
                assert node.key < node.right.key
                dfs(node.right)
                h = max(h, node.right.height)
                b -= node.right.height
                s += node.right.size
            assert node.height == h + 1
            assert -1 <= b <= 1, f"{b=}"
            assert node.size == s

        dfs(self.root)
        # print('check ok.')


def test():
    import random

    random.seed(0)
    s = AVLTreeSet(range(1000))
    ts = set(s)
    Q = 10**4
    for i in range(Q):
        if i % (Q // 10) == 0:
            print(f"query={i}")
        # print(len(s))
        com = random.randint(0, 50)
        x = random.randint(0, 100)
        if com <= 0:
            # insert
            # print(f'add({x})')
            s.add(x)
            ts.add(x)
        else:
            # delete
            # print(f'discard({x})')
            s.discard(x)
            ts.discard(x)
        # print(s, ts)
        assert s.tolist() == sorted(ts)
        s.check()
    s.check()
    exit()


def data():
    import sys

    input = lambda: sys.stdin.buffer.readline().rstrip()
    q = int(input())
    s = AVLTreeSet()
    ans = []
    for _ in range(q):
        t, x = map(int, input().split())
        if t == 1:
            s.add(x)
        else:
            ans.append(s.pop(x - 1))
    if ans:
        print("\n".join(map(str, ans)))
    exit()


data()
# test()

import os
import io


class FastO:
    """標準出力高速化ライブラリです。"""

    _output = io.StringIO()

    @classmethod
    def write(cls, *args, sep: str = " ", end: str = "\n", flush: bool = False) -> None:
        """標準出力します。次の ``FastO.flush()`` が起きると print します。"""
        wr = cls._output.write
        for i in range(len(args) - 1):
            wr(str(args[i]))
            wr(sep)
        if args:
            wr(str(args[-1]))
        wr(end)
        if flush:
            cls.flush()

    @classmethod
    def flush(cls) -> None:
        """``flush`` します。これを実行しないと ``write`` した内容が表示されないので忘れないでください。"""
        os.write(1, cls._output.getvalue().encode())
        cls._output.close()


write, flush = FastO.write, FastO.flush

import sys

input = lambda: sys.stdin.readline().rstrip()

#  -----------------------  #

n, q = map(int, input().split())
s = input()
s = AVLTreeSet(i for i, c in enumerate(s) if c == "1")
for _ in range(q):
    c, k = map(int, input().split())
    if c == 0:
        s.add(k)
    elif c == 1:
        s.discard(k)
    elif c == 2:
        write(1 if k in s else 0)
    elif c == 3:
        ans = s.ge(k)
        write(-1 if ans is None else ans)
    else:
        ans = s.le(k)
        write(-1 if ans is None else ans)
flush()
