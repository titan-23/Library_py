from typing import TypeVar, Generic, Optional

T = TypeVar("T")
BST = TypeVar("BST")
# protcolで、key,val,left,right を規定


class BSTMultisetArrayBase(Generic[BST, T]):

    @staticmethod
    def _rle(a: list[T]) -> tuple[list[T], list[int]]:
        keys, vals = [a[0]], [1]
        for i, elm in enumerate(a):
            if i == 0:
                continue
            if elm == keys[-1]:
                vals[-1] += 1
                continue
            keys.append(elm)
            vals.append(1)
        return keys, vals

    @staticmethod
    def count(bst: BST, key: T) -> int:
        keys, left, right = bst.key, bst.left, bst.right
        node = bst.root
        while node:
            if keys[node] == key:
                return bst.val[node]
            node = left[node] if key < keys[node] else right[node]
        return 0

    @staticmethod
    def le(bst: BST, key: T) -> Optional[T]:
        keys, left, right = bst.key, bst.left, bst.right
        res = None
        node = bst.root
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

    @staticmethod
    def lt(bst: BST, key: T) -> Optional[T]:
        keys, left, right = bst.key, bst.left, bst.right
        res = None
        node = bst.root
        while node:
            if key <= keys[node]:
                node = left[node]
            else:
                res = keys[node]
                node = right[node]
        return res

    @staticmethod
    def ge(bst: BST, key: T) -> Optional[T]:
        keys, left, right = bst.key, bst.left, bst.right
        res = None
        node = bst.root
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

    @staticmethod
    def gt(bst: BST, key: T) -> Optional[T]:
        keys, left, right = bst.key, bst.left, bst.right
        res = None
        node = bst.root
        while node:
            if key < keys[node]:
                res = keys[node]
                node = left[node]
            else:
                node = right[node]
        return res

    @staticmethod
    def index(bst: BST, key: T) -> int:
        keys, left, right, vals, valsize = (
            bst.key,
            bst.left,
            bst.right,
            bst.val,
            bst.valsize,
        )
        k = 0
        node = bst.root
        while node:
            if key == keys[node]:
                if left[node]:
                    k += valsize[left[node]]
                break
            if key < keys[node]:
                node = left[node]
            else:
                k += valsize[left[node]] + vals[node]
                node = right[node]
        return k

    @staticmethod
    def index_right(bst: BST, key: T) -> int:
        keys, left, right, vals, valsize = (
            bst.key,
            bst.left,
            bst.right,
            bst.val,
            bst.valsize,
        )
        k = 0
        node = bst.root
        while node:
            if key == keys[node]:
                k += valsize[left[node]] + vals[node]
                break
            if key < keys[node]:
                node = left[node]
            else:
                k += valsize[left[node]] + vals[node]
                node = right[node]
        return k

    @staticmethod
    def _kth_elm(bst: BST, k: int) -> tuple[T, int]:
        left, right, vals, valsize = bst.left, bst.right, bst.val, bst.valsize
        if k < 0:
            k += len(bst)
        node = bst.root
        while True:
            t = vals[node] + valsize[left[node]]
            if t - vals[node] <= k < t:
                return bst.key[node], vals[node]
            if t > k:
                node = left[node]
            else:
                node = right[node]
                k -= t

    @staticmethod
    def contains(bst: BST, key: T) -> bool:
        left, right, keys = bst.left, bst.right, bst.key
        node = bst.root
        while node:
            if keys[node] == key:
                return True
            node = left[node] if key < keys[node] else right[node]
        return False

    @staticmethod
    def tolist(bst: BST) -> list[T]:
        left, right, keys, vals = bst.left, bst.right, bst.key, bst.val
        node = bst.root
        stack, a = [], []
        while stack or node:
            if node:
                stack.append(node)
                node = left[node]
            else:
                node = stack.pop()
                key = keys[node]
                for _ in range(vals[node]):
                    a.append(key)
                node = right[node]
        return a
