# from titan_pylib.data_structures.avl_tree.avl_tree_dict import AVLTreeDict
# from titan_pylib.my_class.supports_less_than import SupportsLessThan
from typing import Protocol


class SupportsLessThan(Protocol):

    def __lt__(self, other) -> bool: ...
from typing import Callable, Generic, Iterable, TypeVar, Union, Optional

K = TypeVar("K", bound=SupportsLessThan)
V = TypeVar("V")


class AVLTreeDict(Generic[K, V]):

    class Node:

        def __init__(self, key: K, val: V):
            self.key: K = key
            self.val: V = val
            self.left: Optional[AVLTreeDict.Node] = None
            self.right: Optional[AVLTreeDict.Node] = None
            self.balance = 0

        def __str__(self):
            if self.left is None and self.right is None:
                return f"key:{self.key, self.val}\n"
            return (
                f"key:{self.key, self.val},\n left:{self.left},\n right:{self.right}\n"
            )

    def __init__(
        self,
        a: Iterable[K] = [],
        counter: bool = False,
        default: Callable[[], K] = None,
    ) -> None:
        self._default = default
        self.node = None
        self._len = 0
        if counter:
            self._default = int
            self._build(a)

    def _build(self, a: Iterable[K]) -> None:
        for a_ in sorted(a):
            self.__setitem__(a_, self.__getitem__(a_) + 1)

    def _rotate_L(self, node: Node) -> Node:
        u = node.left
        node.left = u.right
        u.right = node
        if u.balance == 1:
            u.balance = 0
            node.balance = 0
        else:
            u.balance = -1
            node.balance = 1
        return u

    def _rotate_R(self, node: Node) -> Node:
        u = node.right
        node.right = u.left
        u.left = node
        if u.balance == -1:
            u.balance = 0
            node.balance = 0
        else:
            u.balance = 1
            node.balance = -1
        return u

    def _update_balance(self, node: Node) -> None:
        if node.balance == 1:
            node.right.balance = -1
            node.left.balance = 0
        elif node.balance == -1:
            node.right.balance = 0
            node.left.balance = 1
        else:
            node.right.balance = 0
            node.left.balance = 0
        node.balance = 0

    def _rotate_LR(self, node: Node) -> Node:
        B = node.left
        E = B.right
        B.right = E.left
        E.left = B
        node.left = E.right
        E.right = node
        self._update_balance(E)
        return E

    def _rotate_RL(self, node: Node) -> Node:
        C = node.right
        D = C.left
        C.left = D.right
        D.right = C
        node.right = D.left
        D.left = node
        self._update_balance(D)
        return D

    def items(self):
        a = self.tolist_items()
        for i in range(self.__len__()):
            yield a[i]

    def keys(self):
        a = self.tolist_items()
        for i in range(self.__len__()):
            yield a[i][0]

    def values(self):
        a = self.tolist_items()
        for i in range(self.__len__()):
            yield a[i][1]

    def _search_node(self, key: K) -> Union[Node, None]:
        node = self.node
        while node is not None:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def _discard(self, key: K) -> bool:
        di = 0
        path = []
        node = self.node
        while node is not None:
            if key == node.key:
                break
            elif key < node.key:
                path.append(node)
                di <<= 1
                di |= 1
                node = node.left
            else:
                path.append(node)
                di <<= 1
                node = node.right
        else:
            return False
        if node.left is not None and node.right is not None:
            path.append(node)
            di <<= 1
            di |= 1
            lmax = node.left
            while lmax.right is not None:
                path.append(lmax)
                di <<= 1
                lmax = lmax.right
            node.key = lmax.key
            node = lmax
        cnode = node.right if node.left is None else node.left
        if path:
            pnode = path[-1]
            if di & 1:
                pnode.left = cnode
            else:
                pnode.right = cnode
        else:
            self.node = cnode
            return True
        while path:
            new_node = None
            pnode = path.pop()
            pnode.balance -= 1 if di & 1 else -1
            di >>= 1
            if pnode.balance == 2:
                new_node = (
                    self._rotate_LR(pnode)
                    if pnode.left.balance == -1
                    else self._rotate_L(pnode)
                )
            elif pnode.balance == -2:
                new_node = (
                    self._rotate_RL(pnode)
                    if pnode.right.balance == 1
                    else self._rotate_R(pnode)
                )
            elif pnode.balance != 0:
                break
            if new_node is not None:
                if not path:
                    self.node = new_node
                    return True
                if di & 1:
                    path[-1].left = new_node
                else:
                    path[-1].right = new_node
                if new_node.balance != 0:
                    break
        return True

    def tolist_items(self) -> list[tuple[K, V]]:
        a = []
        if self.node is None:
            return a

        def rec(node):
            if node.left is not None:
                rec(node.left)
            a.append((node.key, node.val))
            if node.right is not None:
                rec(node.right)

        rec(self.node)
        return a

    def __setitem__(self, key: K, val: V):
        self._len += 1
        if self.node is None:
            self.node = AVLTreeDict.Node(key, val)
            return True
        pnode = self.node
        path = []
        di = 0
        while pnode is not None:
            if key == pnode.key:
                pnode.val = val
                return
            elif key < pnode.key:
                path.append(pnode)
                di <<= 1
                di |= 1
                pnode = pnode.left
            else:
                path.append(pnode)
                di <<= 1
                pnode = pnode.right
        if di & 1:
            path[-1].left = AVLTreeDict.Node(key, val)
        else:
            path[-1].right = AVLTreeDict.Node(key, val)
        new_node = None
        while path:
            pnode = path.pop()
            pnode.balance += 1 if di & 1 else -1
            di >>= 1
            if pnode.balance == 0:
                break
            if pnode.balance == 2:
                new_node = (
                    self._rotate_LR(pnode)
                    if pnode.left.balance == -1
                    else self._rotate_L(pnode)
                )
                break
            elif pnode.balance == -2:
                new_node = (
                    self._rotate_RL(pnode)
                    if pnode.right.balance == 1
                    else self._rotate_R(pnode)
                )
                break
        if new_node is not None:
            if path:
                gnode = path.pop()
                if di & 1:
                    gnode.left = new_node
                else:
                    gnode.right = new_node
            else:
                self.node = new_node
        return True

    def __delitem__(self, key: K):
        if self._discard(key):
            self._len -= 1
            return
        raise KeyError(key)

    def __getitem__(self, key: K):
        node = self._search_node(key)
        return self.__missing__() if node is None else node.val

    def __contains__(self, key: K):
        return self._search_node(key) is not None

    def __len__(self):
        return self._len

    def __bool__(self):
        return self.node is not None

    def __str__(self):
        return "{" + ", ".join(map(lambda x: f"{x[0]}: {x[1]}", self.items())) + "}"

    def __repr__(self):
        return "AVLTreeDict(" + str(self) + ")"

    def __missing__(self, e):
        return self._default()
