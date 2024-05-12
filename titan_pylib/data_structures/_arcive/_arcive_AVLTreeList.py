from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class Node:

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1

    def __str__(self):
        if self.left is None and self.right is None:
            return f"key:{self.key, self.height, self.size}\n"
        return f"key:{self.key, self.height, self.size},\n left:{self.left},\n right:{self.right}\n"


class AVLTreeList(Generic[T]):

    def __init__(self, a: Iterable[T] = [], node: Node = None) -> None:
        self.node = node
        if a:
            self._build(list(a))

    def _build(self, a: list[T]) -> None:
        def sort(l: int, r: int) -> Node:
            mid = (l + r) >> 1
            node = Node(a[mid])
            if l != mid:
                node.left = sort(l, mid)
            if mid + 1 != r:
                node.right = sort(mid + 1, r)
            self._update(node)
            return node

        self.node = sort(0, len(a))

    def _update(self, node: Node) -> None:
        if node.left is None:
            if node.right is None:
                node.size = 1
                node.data = node.key
                node.height = 1
            else:
                node.size = 1 + node.right.size
                node.height = node.right.height + 1
        else:
            if node.right is None:
                node.size = 1 + node.left.size
                node.height = node.left.height + 1
            else:
                node.size = 1 + node.left.size + node.right.size
                node.height = (
                    node.left.height + 1
                    if node.left.height > node.right.height
                    else node.right.height + 1
                )

    def _get_balance(self, node: Node) -> int:
        return (
            (0 if node.right is None else -node.right.height)
            if node.left is None
            else (
                node.left.height
                if node.right is None
                else node.left.height - node.right.height
            )
        )

    def _balance_left(self, node: Node) -> Node:
        if node.left.left is None or node.left.left.height + 2 == node.left.height:
            u = node.left.right
            node.left.right = u.left
            u.left = node.left
            node.left = u.right
            u.right = node
            self._update(u.left)
        else:
            u = node.left
            node.left = u.right
            u.right = node
        self._update(u.right)
        self._update(u)
        return u

    def _balance_right(self, node: Node) -> Node:
        if node.right.right is None or node.right.right.height + 2 == node.right.height:
            u = node.right.left
            node.right.left = u.right
            u.right = node.right
            node.right = u.left
            u.left = node
            self._update(u.right)
        else:
            u = node.right
            node.right = u.left
            u.left = node
        self._update(u.left)
        self._update(u)
        return u

    def _kth_elm(self, k: int) -> T:
        if k < 0:
            k += self.__len__()
        node = self.node
        while True:
            t = 0 if node.left is None else node.left.size
            if t == k:
                return node.key
            elif t < k:
                k -= t + 1
                node = node.right
            else:
                node = node.left

    def _merge_with_root(self, l: Node, root: Node, r: Node) -> Node:
        diff = (
            (0 if r is None else -r.height)
            if l is None
            else (l.height if r is None else l.height - r.height)
        )
        if diff > 1:
            l.right = self._merge_with_root(l.right, root, r)
            self._update(l)
            if (
                -l.right.height
                if l.left is None
                else l.left.height - l.right.height == -2
            ):
                return self._balance_right(l)
            return l
        elif diff < -1:
            r.left = self._merge_with_root(l, root, r.left)
            self._update(r)
            if (
                r.left.height
                if r.right is None
                else r.left.height - r.right.height == 2
            ):
                return self._balance_left(r)
            return r
        else:
            root.left = l
            root.right = r
            self._update(root)
            return root

    def _merge_node(self, l: Node, r: Node) -> Node:
        if l is None:
            return r
        if r is None:
            return l
        l, tmp = self._pop_max(l)
        return self._merge_with_root(l, tmp, r)

    def merge(self, other: "AVLTreeList") -> None:
        self.node = self._merge_node(self.node, other.node)

    def _pop_max(self, node: Node) -> tuple[Node, Node]:
        path = []
        mx = node
        while node.right is not None:
            path.append(node)
            mx = node.right
            node = node.right
        path.append(node.left)
        for _ in range(len(path) - 1):
            node = path.pop()
            if node is None:
                path[-1].right = None
                self._update(path[-1])
                continue
            b = self._get_balance(node)
            path[-1].right = (
                self._balance_left(node)
                if b == 2
                else self._balance_right(node) if b == -2 else node
            )
            self._update(path[-1])
        if path[0] is not None:
            b = self._get_balance(path[0])
            path[0] = (
                self._balance_left(path[0])
                if b == 2
                else self._balance_right(path[0]) if b == -2 else path[0]
            )
        mx.left = None
        self._update(mx)
        return path[0], mx

    def _split_node(self, node: Node, k: int) -> tuple[Node, Node]:
        if node is None:
            return None, None
        tmp = k if node.left is None else k - node.left.size
        if tmp == 0:
            return node.left, self._merge_with_root(None, node, node.right)
        elif tmp < 0:
            s, t = self._split_node(node.left, k)
            return s, self._merge_with_root(t, node, node.right)
        else:
            s, t = self._split_node(node.right, tmp - 1)
            return self._merge_with_root(node.left, node, s), t

    def split(self, k: int) -> tuple["AVLTreeList", "AVLTreeList"]:
        l, r = self._split_node(self.node, k)
        return AVLTreeList(node=l), AVLTreeList(node=r)

    def insert(self, k: int, key: T) -> None:
        s, t = self._split_node(self.node, k)
        self.node = self._merge_with_root(s, Node(key), t)

    def pop(self, k: int) -> T:
        s, t = self._split_node(self.node, k + 1)
        s, tmp = self._pop_max(s)
        self.node = self._merge_node(s, t)
        return tmp.key

    def clear(self) -> None:
        self.node = None

    def tolist(self) -> list[T]:
        a = []
        if self.node is None:
            return a

        def rec(node):
            if node.left is not None:
                rec(node.left)
            a.append(node.key)
            if node.right is not None:
                rec(node.right)

        rec(self.node)
        return a

    def __len__(self):
        return 0 if self.node is None else self.node.size

    def __iter__(self):
        self.__iter = 0
        return self

    def __next__(self):
        if self.__iter == len(self):
            raise StopIteration
        res = self.__getitem__(self.__iter)
        self.__iter += 1
        return res

    def __reversed__(self):
        for i in range(len(self)):
            yield self.__getitem__(-i - 1)

    def __bool__(self):
        return self.node is not None

    def __getitem__(self, k: int) -> T:
        return self._kth_elm(k)

    def __setitem__(self, k, key: T):
        if k < 0:
            k += self.__len__()
        node = self.node
        while True:
            t = 0 if node.left is None else node.left.size
            if t == k:
                node.key = key
                break
            elif t < k:
                k -= t + 1
                node = node.right
            else:
                node = node.left

    def __str__(self):
        return "[" + ", ".join(map(str, self.tolist())) + "]"

    def __repr__(self):
        return "AVLTreeList(" + str(self) + ")"
