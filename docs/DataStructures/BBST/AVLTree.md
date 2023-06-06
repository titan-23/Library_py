_____

# [AVLTree](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BBST/AVLTree)

最終更新：2022/5/26

- いろいろ更新しました。

AVL木です。

_____

## [`AVLTreeSet.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/AVLTree/AVLTreeSet.py)

集合としてのAVL木です。 `T` は全順序が定義されてると仮定します。

- `avl = AVLTreeSet(a: Iterable[T]=[])`
  - `a` から `AVLTreeSet` を構築します。ソートがボトルネックとなり、計算量 `O(NlogN)` です。ソート済みを仮定して内部をいじると `O(N)` です。

- `avl.add(key: T) -> bool`
  - `key` が存在しないなら `key` を追加し、 `True` を返します。 `key` が存在するなら何も追加せず、 `False` を返します。

- `avl.discard(key) -> bool`
  - `key` が存在するなら `key` を削除し、 `True` を返します。 `key` が存在しないなら何もせず、 `False` を返します。

- `key in avl`
存在判定です。 `key` が存在すれば `True` を、そうでなければ `False` を返します。

- `avl[k: int] -> T`
昇順 `k` 番目の値を返します。

- `avl.le(key) / .lt(key) / .ge(key) / gt(key) -> Optional[T]`
  - `key` (以下の / より小さい / 以上の / より大きい)値で(最大 / 最大 / 最小 / 最小)の値を返します。存在しなければ `None` を返します。

- `avl.index(key) / .index_right(key) -> int`
  - `key` (より小さい / 以下の)要素の数を返します。

- `avl.pop(k=-1) / .popleft() -> T`
  - (最大(昇順 `k` 番目) / 最小)の値を削除し、その値を返します。

- `avl.clear() -> None`
  - `clear` します。 `O(1)` です。

- `avl.tolist() -> List[T]`
  - `key` を昇順に並べたリストを返します。 `O(N)` です。

## [`AVLTreeSet2.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/AVLTree/AVLTreeSet2.py)
集合としてのAVL木です。  
各 `Node` は `key/左の子/右の子` のみをもち、 `Node` を頂点とする部分木の大きさは持ちません。[`AVLTreeSet`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/AVLTree/AVLTreeSet.py)の機能を落として高速化を図った形です。違いは以下の通りです。

- `avl = AVLTreeSet2(a: Iterable[T]=[])`
  - `a` から `AVLTreeSet` を構築します。ソートがボトルネックとなり、計算量 `O(NlogN)` です。ソート済みを仮定して内部をいじると `O(N)` です。

- `avl[k] -> T`
  - `k` に指定できるものは、 `0/-1/len(avl)-1` のいずれかです。

- `avl.get_min() / .get_max() -> T`
  - (最小 / 最大)の値を返します。

- `avl.pop() / .popleft() -> T`
  - (最大 / 最小)の値を削除し、その値を返します。 `pop` で引数が指定できなくなりました。

_____

## [`AVLTreeMultiSet.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/AVLTree/AVLTreeMultiset.py)
多重集合としての `AVL` 木です。

_____

## [`LazyAVLTree.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/AVLTree/LazyAVLTree.py)

遅延伝播反転可能平衡二分木です。アホの定数倍をしています(定数倍が大きい方向にアホです)。  

- `avl = LazyAVLTree(a, op, mapping, composition, e)` - 
列 `a` から `LazyAVLTree` を構築します。その他引数は遅延セグ木のアレです。時間計算量 `O(N)` です。

- `avl.merge(other: LazyAVLTree) -> None`
  - `avl` に `other` を `merge` できます。

- `avl.split(k) -> Tuple[LazyAVLTree, LazyAVLTree]`
  - `x, y = avl.split(k)` で、`k` 番目で左右に分けた `AVLTree` をつくり `x, y` に代入できます。 `avl` は破壊されます。( `x` の長さが `k` 。)

- `avl.insert(k, key)`
  - `k` に `key` を `insesrt` できます。

- `avl.pop(k)`
  - `k` 番目を削除しその値を返します。

- `avl[k]`
  - `k` 番目を取得できます。

- `avl.prod(l, r)`
  - 区間 `[l, r)` に `op` を適用した結果を返します。

- `avl.reverse(l, r)`
  - 区間 `[l, r)` を反転します。 `reverse()` メソッドを一度でも使用するなら `op` には可換性が求められます(可換性がない場合、嘘の動作をします)。

- `avl.apply(l, r, f)`
  - 区間 `[l, r)` に `f` を適用します。

- `avl.tolist() -> List[T]`
  - `Node` の `key` からなるリストを返します。計算量 `O(N)` です。

