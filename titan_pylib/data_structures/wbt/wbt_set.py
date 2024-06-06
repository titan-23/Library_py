from titan_pylib.data_structures.wbt._wbt_set_node import _WBTSetNode
from typing import Generic, TypeVar, Optional, Iterable, Iterator

T = TypeVar("T")


class WBTSet(Generic[T]):
    """重み平衡木で実装された順序付き集合"""

    __slots__ = "_root", "_min", "_max"

    def __init__(self, a: Iterable[T] = []) -> None:
        """イテラブル ``a`` から ``WBTSet`` を構築します。

        Args:
            a (Iterable[T], optional): 構築元のイテラブルです。

        計算量:

            ソート済みなら :math:`O(n)` 、そうでないなら :math:`O(n \\log{n})`
        """
        self._root: Optional[_WBTSetNode[T]] = None
        self._min: Optional[_WBTSetNode[T]] = None
        self._max: Optional[_WBTSetNode[T]] = None
        self.__build(a)

    def __build(self, a: Iterable[T]) -> None:
        """再帰的に構築する関数"""

        def build(
            l: int, r: int, pnode: Optional[_WBTSetNode[T]] = None
        ) -> _WBTSetNode[T]:
            if l == r:
                return None
            mid = (l + r) // 2
            node = _WBTSetNode(a[mid])
            node._left = build(l, mid, node)
            node._right = build(mid + 1, r, node)
            node._par = pnode
            node._update()
            return node

        a = list(a)
        if not a:
            return
        if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
            a.sort()
            new_a = [a[0]]
            for elm in a:
                if new_a[-1] == elm:
                    continue
                new_a.append(elm)
            a = new_a
        self._root = build(0, len(a))
        self._max = self._root._max()
        self._min = self._root._min()

    def add(self, key: T) -> bool:
        """既に ``key`` が存在していれば何もせず ``False`` を返し、
        存在していれば ``key`` を 1 つ追加して ``True`` を返します。

        Args:
            key (T): 追加するキーです。

        Returns:
            bool: ``key`` を追加したら ``True`` 、そうでなければ ``False`` を返します。

        計算量:
            :math:`O(\\log{n})`
        """
        if not self._root:
            self._root = _WBTSetNode(key)
            self._max = self._root
            self._min = self._root
            return True
        pnode = None
        node = self._root
        while node:
            if key == node._key:
                return False
            pnode = node
            node = node._left if key < node._key else node._right
        if key < pnode._key:
            pnode._left = _WBTSetNode(key)
            if key < self._min._key:
                self._min = pnode._left
            pnode._left._par = pnode
        else:
            pnode._right = _WBTSetNode(key)
            if key > self._max._key:
                self._max = pnode._right
            pnode._right._par = pnode
        self._root = pnode._rebalance()
        return True

    def find_key(self, key: T) -> Optional[_WBTSetNode[T]]:
        """``key`` が存在すれば ``key`` を指すノードを返します。
        そうでなければ ``None`` を返します。

        Args:
            key (T):

        Returns:
            Optional[_WBTSetNode[T]]:

        計算量:
            :math:`O(\\log{n})`
        """
        node = self._root
        while node:
            if key == node._key:
                return node
            node = node._left if key < node._key else node._right
        return None

    def find_order(self, k: int) -> _WBTSetNode[T]:
        """昇順 ``k`` 番目のノードを返します。

        Args:
            k (int):

        Returns:
            _WBTSetNode[T]:

        計算量:
            :math:`O(\\log{n})`

        制約:
            :math:`-n \\leq k \\le n`
        """
        if k < 0:
            k += len(self)
        node = self._root
        while True:
            t = node._left._size if node._left else 0
            if t == k:
                return node
            if t < k:
                k -= t + 1
                node = node._right
            else:
                node = node._left

    def remove_iter(self, node: _WBTSetNode[T]) -> None:
        """``node`` を削除します。

        Args:
            node (_WBTSetNode[T]):

        計算量:
            :math:`O(\\log{n})`
        """
        if node is self._min:
            self._min = self._min._next()
        if node is self._max:
            self._max = self._max._prev()
        delnode = node
        pnode, mnode = node._par, None
        if node._left and node._right:
            pnode, mnode = node, node._left
            while mnode._right:
                pnode, mnode = mnode, mnode._right
            node = mnode
        cnode = node._right if not node._left else node._left
        if cnode:
            cnode._par = pnode
        if pnode:
            if pnode._left is node:
                pnode._left = cnode
            else:
                pnode._right = cnode
            self._root = pnode._rebalance()
        else:
            self._root = cnode
        if mnode:
            if self._root is delnode:
                self._root = mnode
            mnode._copy_from(delnode)
        del delnode

    def remove(self, key: T) -> None:
        """``key`` を削除します。

        Args:
            key (T): 削除する ``key`` です。

        計算量:
            :math:`O(\\log{n})`

        Note:
            ``key`` が存在しない場合、 ``AssertionError`` を出します。
        """
        node = self.find_key(key)
        assert node, f"KeyError: {key} is not exist."
        self.remove_iter(node)

    def discard(self, key: T) -> bool:
        """``key`` が存在すれば削除して ``True`` を返します。
        存在しなければなにもせず ``False`` を返します。

        Args:
            key (T): 削除する ``key`` です。

        Returns:
            bool: ``key`` が存在したかどうか

        計算量:
            :math:`O(\\log{n})`
        """
        node = self.find_key(key)
        if node is None:
            return False
        self.remove_iter(node)
        return True

    def pop(self, k: int = -1) -> T:
        """``k`` 番目の値を削除して返します。
        引数指定がない場合は最大の値を削除して返します。

        Args:
            k (int, optional): 削除するインデックスです。

        Returns:
            T: ``k`` 番目の値です。

        計算量:
            :math:`O(\\log{n})`
        """
        node = self.find_order(k)
        key = node._key
        self.remove_iter(node)
        return key

    def le_iter(self, key: T) -> Optional[_WBTSetNode[T]]:
        """``key`` 以下で最大のノードを返します。存在しないときは ``None`` を返します。

        計算量:
            :math:`O(\\log{n})`
        """
        res = None
        node = self._root
        while node:
            if key == node._key:
                res = node
                break
            if key < node._key:
                node = node._left
            else:
                res = node
                node = node._right
        return res

    def lt_iter(self, key: T) -> Optional[_WBTSetNode[T]]:
        """``key`` より小さい値で最大のノードを返します。存在しないときは ``None`` を返します。

        計算量:
            :math:`O(\\log{n})`
        """
        res = None
        node = self._root
        while node:
            if key <= node._key:
                node = node._left
            else:
                res = node
                node = node._right
        return res

    def ge_iter(self, key: T) -> Optional[_WBTSetNode[T]]:
        """``key`` 以上で最小のノードを返します。存在しないときは ``None`` を返します。

        計算量:
            :math:`O(\\log{n})`
        """
        res = None
        node = self._root
        while node:
            if key == node._key:
                res = node
                break
            if key < node._key:
                res = node
                node = node._left
            else:
                node = node._right
        return res

    def gt_iter(self, key: T) -> Optional[_WBTSetNode[T]]:
        """``key`` より大きい値で最小のノードを返します。存在しないときは ``None`` を返します。

        計算量:
            :math:`O(\\log{n})`
        """
        res = None
        node = self._root
        while node:
            if key < node._key:
                res = node
                node = node._left
            else:
                node = node._right
        return res

    def le(self, key: T) -> Optional[T]:
        """``key`` 以下で最大の要素を返します。存在しないときは ``None`` を返します。

        計算量:
            :math:`O(\\log{n})`
        """
        res = None
        node = self._root
        while node:
            if key == node._key:
                res = key
                break
            if key < node._key:
                node = node._left
            else:
                res = node._key
                node = node._right
        return res

    def lt(self, key: T) -> Optional[T]:
        """``key`` より小さい値で最大の要素を返します。存在しないときは ``None`` を返します。

        計算量:
            :math:`O(\\log{n})`
        """
        res = None
        node = self._root
        while node:
            if key <= node._key:
                node = node._left
            else:
                res = node._key
                node = node._right
        return res

    def ge(self, key: T) -> Optional[T]:
        """``key`` 以上で最小の要素を返します。存在しないときは ``None`` を返します。

        計算量:
            :math:`O(\\log{n})`
        """
        res = None
        node = self._root
        while node:
            if key == node._key:
                res = key
                break
            if key < node._key:
                res = node._key
                node = node._left
            else:
                node = node._right
        return res

    def gt(self, key: T) -> Optional[T]:
        """``key`` より大きい値で最小の要素を返します。存在しないときは ``None`` を返します。

        計算量:
            :math:`O(\\log{n})`
        """
        res = None
        node = self._root
        while node:
            if key < node._key:
                res = node._key
                node = node._left
            else:
                node = node._right
        return res

    def index(self, key: T) -> int:
        """``key`` より小さい値を個数を返します。

        Args:
            key (T):

        Returns:
            int:

        計算量:
            :math:`O(\\log{n})`
        """
        k = 0
        node = self._root
        while node:
            if key == node._key:
                k += node._left._size if node._left else 0
                break
            if key < node._key:
                node = node._left
            else:
                k += node._left._size + 1 if node._left else 1
                node = node._right
        return k

    def index_right(self, key: T) -> int:
        """``key`` 以下の値を個数を返します。

        Args:
            key (T):

        Returns:
            int:

        計算量:
            :math:`O(\\log{n})`
        """
        k = 0
        node = self._root
        while node:
            if key == node._key:
                k += node._left._size + 1 if node._left else 1
                break
            if key < node._key:
                node = node._left
            else:
                k += node._left._size + 1 if node._left else 1
                node = node._right
        return k

    def get_min(self) -> T:
        """最小の要素を返します。

        Returns:
            T:

        計算量:
            :math:`O(1)`

        制約:
            :math:`0 < n`
        """
        assert self._min
        return self._min._key

    def get_max(self) -> T:
        """最大の要素を返します。

        Returns:
            T:

        計算量:
            :math:`O(1)`

        制約:
            :math:`0 < n`
        """
        assert self._max
        return self._max._key

    def pop_min(self) -> T:
        """最小の要素を削除して返します。

        Returns:
            T:

        計算量:
            :math:`O(\\log{n})`

        制約:
            :math:`0 < n`
        """
        assert self._min
        key = self._min._key
        self.remove_iter(self._min)
        return key

    def pop_max(self) -> T:
        """最大の要素を削除して返します。

        Returns:
            T:

        計算量:
            :math:`O(\\log{n})`

        制約:
            :math:`0 < n`
        """
        assert self._max
        key = self._max._key
        self.remove_iter(self._max)
        return key

    def _check(self) -> None:
        """作業用デバック関数
        size,key,balanceをチェックして、正しければ高さを表示する
        """
        if self._root is None:
            # print("ok. 0 (empty)")
            return

        # _size, height
        def dfs(node: _WBTSetNode[T]) -> tuple[int, int]:
            h = 0
            s = 1
            if node._left:
                assert node._key > node._left._key
                ls, lh = dfs(node._left)
                s += ls
                h = max(h, lh)
            if node._right:
                assert node._key < node._right._key
                rs, rh = dfs(node._right)
                s += rs
                h = max(h, rh)
            assert node._size == s
            node._balance_check()
            return s, h + 1

        _, h = dfs(self._root)
        # print(f"ok. {h}")

    def __contains__(self, key: T) -> bool:
        """``key`` が存在すれば ``True`` 、そうでなければ ``False`` を返します。

        Args:
            key (T):

        Returns:
            bool:

        計算量:
            :math:`O(\\log{n})`
        """
        return self.find_key(key) is not None

    def __getitem__(self, k: int) -> T:
        """昇順 ``k`` 番目の値を返します。

        Args:
            k (int):

        Returns:
            T:

        計算量:
            k = 0 または k = n-1 の場合: :math:`O(1)`
            そうでない場合: :math:`O(\\log{n})`
        """
        assert (
            -len(self) <= k < len(self)
        ), f"IndexError: {self.__class__.__name__}[{k}], len={len(self)}"
        if k < 0:
            k += len(self)
        if k == 0:
            return self.get_min()
        if k == len(self) - 1:
            return self.get_max()
        return self.find_order(k)._key

    # def __delitem__(self, k: int) -> None:
    #     self.remove_iter(self.find_order(k))

    def __len__(self) -> int:
        """要素数を返します。

        Returns:
            int:

        計算量:
            :math:`O(1)`
        """
        return self._root._size if self._root else 0

    def __iter__(self) -> Iterator[T]:
        """昇順に値を返します。

        Yields:
            Iterator[T]:

        計算量:
            全体で :math:`O(n)`
        """
        stack: list[_WBTSetNode[T]] = []
        node = self._root
        while stack or node:
            if node:
                stack.append(node)
                node = node._left
            else:
                node = stack.pop()
                yield node._key
                node = node._right

    def __reversed__(self) -> Iterator[T]:
        """降順に値を返します。

        Yields:
            Iterator[T]:

        計算量:
            全体で :math:`O(n)`
        """
        stack: list[_WBTSetNode[T]] = []
        node = self._root
        while stack or node:
            if node:
                stack.append(node)
                node = node._right
            else:
                node = stack.pop()
                yield node._key
                node = node._left

    def __str__(self) -> str:
        return "{" + ", ".join(map(str, self)) + "}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" + "{" + ", ".join(map(str, self)) + "})"
