____

# BBST

最終更新: 2023/06/12
- なんかいろいろ更新
- 統一させるの難しいね


計算量は償却だったり最悪だったりします。詳しくは各READMEを読んでください。  

以下の木があります。  

- [`AVLTree`](AVLTree.md)
- [`RedBlackTree`](RedBlackTree.md)
- [`ScapegoatTree`](ScapegoatTree.md)
- [`SplayTree`](SplayTree.md)
- [`Treap`](Treap.md)

_____

## 列を扱うBBST

列を扱えます。

#### `bt.merge(other: BBST) -> None`
`bt` に `other` をマージします。 `merge` した後に `other` を使うとマズイです。 `O(logN)` です。

#### `bt.split(k: int) -> Tuple[BBST, BBST]`
- `bt` を `k` で `split` します。`O(logN)`です。

#### `bt.prod(l: int, r: int) -> T`
- 区間 `[l, r)`の総積を取得します。
- `O(logN)` です。

#### `bt.all_prod() -> T`
- 区間 `[0, n)` の総積を取得します。
- `O(1)` です。

#### `bt.insert(k: int, key: T) -> None`
- `k` 番目に `key` を挿入します。
- `O(logN)` です。

#### `bt.append(key: T) / .appendleft(key: T) -> None`
- 先頭 / 末尾に `key` を追加します。
- `O(logN)` です。

#### `bt.pop(k: int=-1) / .popleft() -> T`
- 末尾( `k` 番目) / 先頭の値を削除し、その値を返します。
- `O(logN)` です。

#### `bt[k: int] -> T`
- `k` 番目の値を返します。
- `O(logN)` です。

#### `bt[k: int] = key: T`
- `k` 番目の値を `key` に更新します。
- `O(logN)` です。

#### `bt.copy() -> None`
- コピーします。
- `O(N)` です。

#### `bt.clear() -> None`
- clearします。
- `O(1)` です。

#### `bt.tolist() -> List[T]`
- `key` からなるリストを返します。
- `O(N)` です。

## 遅延評価できる木

列を扱う `BinaryTree` に加えて以下の操作ができます。

#### `bt.reverse(l: int, r: int) -> None`
- 区間 `[l, r)` を反転します。 `reverse` メソッドを使うなら、`op` には可換性が求められます。
- `O(logN)` です。

#### `bt.apply(l: int, r: int, f: F) -> None`
- 区間 `[l, r)` に `f` を適用します。
- `O(logN)`です。

#### `bt.all_apply(f: F) -> None`
- 区間 `[0, n)` に `f` を適用します。
`O(1)`です。

_____

## 集合としてのBBST

集合です。

#### `x in bst / x not in bst`
- 存在判定です。
- `O(logN)` です。

#### `bst[k: int] -> T`
- 昇順 `k` 番目の値を返します
- `O(logN)` です。

#### `bst.add(key: T) -> bool`
- `key` が存在しないなら `key` を追加し `True` を返します。そうでないなら何も追加せず `False` を返します。
- `O(logN)` です。

#### `bst.discard(key: T) -> bool`
- `key` が存在するなら `key` を削除し `True` を返します。そうでないなら何もせず `False` を返します。
- `O(logN)` です。

#### `bst.le(key) / .lt(key) / .ge(key) / gt(key) -> Optional[T]`
- `key` (以下の / より小さい / 以上の / より大きい) 値で (最大 / 最大 / 最小 / 最小) の値を返します。存在しなければ `None` を返します。
- `O(logN)` です。

#### `bst.index(key: T) / .index_right(key: T) -> int`
- `key` (より小さい / 以下の) 要素の数を返します。
- `O(logN)` です。

#### `bst.pop(k: int=-1) / .popleft() -> T`
- (最大(昇順k番目) / 最小) の値を削除し、その値を返します。
- `O(logN)` です。

#### `bst.clear() -> None`
- clearします。
- `O(1)` です。

#### `bst.tolist() -> List[T]`
- `key` を昇順に並べたリストを返します。
- `O(N)` です。

## 多重集合

`Set` に加えて、以下の操作ができます。  
valの値に関わらず `O(logN)` で動作します。

#### `bst.add(key: T, val: int=1) -> None`
- `key` を `val` 個追加します。
- `O(logN)` です。

#### `bst.discard(key: T, val: int=1) -> bool`
- `key` を `val` 個削除します。 `val` が `key` の数より大きいときは、 `key` を全て削除します。
- `key` が無いとき `False` を、そうでないときTrueを返します。
- `O(logN)` です。

#### `bst.dicard_all(key: T) -> None`
- `key` を全て削除します。
- `O(logN)` です。

#### `bst.count(key: T) -> int`
- 含まれる `key` の数を返します。
- `O(logN)` です。

#### `bst.index_keys(key: T) / index_right_keys(key: T) -> int`
- `key` (より小さい / 以下の) 要素の種類数を返します。
- `O(logN)` です。

#### `bst.tolist_items() -> Liset[Tuple[T, int]]`
- `key` で昇順に並べたリストを返します。各要素は `(key, st.count(key))` です。
- `O(N)` です。

#### `bst.keys() / values() / items()`
よしなに動きます。

#### `bst.get_elm(k: int) -> T`
- 要素の重複を除いたときの、昇順 `k` 番目の `key` を返します。
- `O(logN)` です。

#### `bst.len_elm() -> int`
- 要素の種類数を返します。
- `O(1)` です。
