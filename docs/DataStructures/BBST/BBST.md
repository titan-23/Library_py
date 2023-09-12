____

# BBST

最終更新: 2023/09/12
- なんかいろいろ更新
- 統一させるの難しいね


計算量は償却だったり最悪だったりします。詳しくは各READMEを読んでください。  

以下の木があります。  

- [`AVLTree`](../AVLTree/AVLTree.md)
- [`RedBlackTree`](../RedBlackTree/RedBlackTree.md)
  - [`RedBlackTreeSet`](../RedBlackTree/RedBlackTreeSet.md)
  - [`RedBlackTreeMultiset`](../RedBlackTree/RedBlackTreeMultiset.md)
- [`ScapegoatTree`](../ScapegoatTree/ScapegoatTree.md)
- [`SplayTree`](../SplayTree/SplayTree.md)
- [`Treap`](../Treap/Treap.md)

_____

## 集合としてのBBST

集合です。

[`OrderedSetInterface`](../../MyClass/OrderedSetInterface.md) を継承しています。

## 多重集合

多重集合です。

[`OrderedMultisetInterface`](../../MyClass/OrderedMultisetInterface.md) を継承しています。

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

