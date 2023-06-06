____

# [`RedBlackTree`](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BBST/RedBlackTree)

最終更新：2023/06/06

- いろいろ更新しました。

赤黒木です。集合と多重集合です。 `std::set` も怖くない。

_____

# `Node`

`Node` です。双方向に進められます。 `1` だけ進める場合、計算量は平均 `O(1)` 、最悪 `O(logN)` です。 `k` だけ進める場合、だいたい `k` 倍になります(ホント?)。

### `node += 1 / node -= 1`
- `node` を次 / 前の `node` にします。存在しないときは `None` になります。

### `node + 1 / node - 1`
- 次 / 前の `node` を返します。存在しないときは `None` を返します。

### `node.key`
- `node` が保持している `key` です。変更はしないでください。できない仕様にしろ、それはそう

### `node.count`
- `node` が保持している `key` の個数です。

_____

# [`RedBlackTreeSet.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/RedBlackTree/RedBlackTreeSet.py)

集合としての赤黒木です。以下の操作ができます:  
`Add` / `Delete` / `Member` / `Predecessor` / `Successor` / など  

詳しくは以下です。

### `rbtree = RedBlackTreeSet(a: Iterable[T]=[])`
- `a` から `RedBlackTreeSet` を再帰的に構築します。
- 重複無くソート済みなら `O(N)` 、そうでないなら `O(NlogN)` です。

### `rbtree.add(key: T) -> bool`
- `key` が存在しないなら `key` を追加し、 `True` を返します。そうでないなら何も追加せずに `False` を返します。
- `O(logN)` です。

### `rbtree.discard_iter(node: Node) -> None`
- `node` を削除します。
- 償却 `O(1)` らしいです。ホントですか?

### `rbtree.discard(key: T) -> bool`
- `key` が存在するなら `key` を削除し `True` を返します。そうでないなら何もせずに `False` を返します。
- `O(logN)` です。

### `rbtree.count(key: T) -> int`
- `key` の個数を返します。 `key` が存在するなら `1` を、存在しないなら `0` を返します。
- `O(logN)` です。

### `key: T in rbtree`
- 存在判定です。 `key` が存在すれば `True` を、そうでなければ `False` を返します。
- `O(logN)` です。

### `rbtree.get_max() / .get_min() -> Optional[T]`
- 最大値 / 最小値を返します。存在しなければ `None` を返します。
- `O(1)` です。

### `rbtree.get_max_iter() / .get_min_iter() -> Optional[Node]`
- 最大値 / 最小値を指す `Node` を返します。空であれば `None` を返します。
- `O(1)` です。

### `rbtree.le(key: T) / .lt(key) / .ge(key) / gt(key) -> Optional[T]`
- `key` (以下の / より小さい / 以上の / より大きい) 値で (最大 / 最大 / 最小 / 最小) の値を返します。存在しなければ `None` を返します。
- `O(logN)` です。

### `rbtree.le_iter(key: T) / .lt_iter(key) / .ge_iter(key) / gt_iter(key) -> Optional[e]`
- `key` (以下の / より小さい / 以上の / より大きい) 値で (最大 / 最大 / 最小 / 最小) の `Node` を返します。存在しなければ `None` を返します。
- `O(logN)` です。

### `rbtree.find(key) -> Optional[Node]`
- `key` が存在すれば、 `key` を指す `Node` を返します。存在しなければ `None` を返します。
- `O(logN)` です。

### `rbtree.tolist() -> List[T]`
- `key` を昇順に並べたリストを返します。
- `O(N)` です。

### `rbtree.pop_max() / .pop_min() -> T`
- 最大値 / 最小値を削除し、その値を返します。空の `rbtree` に使ってはいけません。
- `O(logN)` です。

### `rbtree.clear() -> None`
- 要素をすべて削除します。
- `O(1)` です。

### `str(rbtree) / repr(rbtree)`
- 表示します。

### `len(rbtree) / bool(rbtree) / iter(rbtree) / next(rbtree)`
- よしなよしなです。

_____

# [`RedBlackTreeMultiset.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/RedBlackTree/RedBlackTreeMultiset.py)

多重集合としての赤黒木です。 主に `RedBlackTreeSet` と同等の操作ができます。差分は以下です。

### `rbtree = RedBlackTreeMultiset(a: Iterable[T]=[])`
- `a` から `RedBlackTreeMultiset` を構築します。
- ソート済みなら `O(N)` 、そうでないなら `O(NlogN)` です。

### `rbtree.add(key: T, cnt: int=1) -> None`
- `key` を `cnt` 個追加ます。
- `cnt` の値に依らず `O(logN)` です。

### `rbtree.discard(key: T, cnt: int=1) -> bool`
- `key` を `min(cnt, rbtree.count(key))` 個削除します。
- `cnt` の値に依らず `O(logN)` です。

### `rbtree.discard_all(key: T) -> bool`
- `key` が存在すればすべて削除し `True` を返します。そうでなければ何もせず `False` を返します。
- `O(logN)` です。

