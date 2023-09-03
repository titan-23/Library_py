___

# `AVLTreeBitVector`

___

## コード
[`AVLTreeBitVector`](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BitVector/AVLTreeBitVector.py)

___

- `AVLTreeBitVector` です。ただの AVL 木です。

___

## 仕様

#### `avl = AVLTreeBitVector(a: Iterable[int])`
- 引数 `a` をもとに、`AVLTreeBitVector` を構築します。

#### `avl.reserve(n: int) -> None`
- メモリを確保します。
- `Θ(n)` です。

#### `avl.insert(k: int, v: int) -> None`
- `k` 番目に `v` を挿入します。
- `Θ(logn)` です。

#### `avl.pop(k: int) -> int`
- `k` 番目の要素を削除し、その値を返します。
- `Θ(logn)` です。

#### `avl.set(k: int, v: int=1) -> None / avl[k] = v`
- `k` 番目の bit を `v` にします。
- `__setitem__` メソッドをサポートしています。
- `Θ(logn)` です。

#### `avl.access(k: int) / a[k: int] -> int`
- `k` 番目の bit の値を返します。
- `__getitem__` メソッドをサポートしています。
- `Θ(logn)` です。

#### `avl.rank0(r: int) -> int, avl.rank1(r: int) -> int, avl.rank(r: int, v: int) -> int`
- `a[0, r)` に含まれる `0 / 1 / v` の個数を返します。
- `Θ(logn)` です。

#### `avl.select0(r: int) -> int, avl.select1(r: int) -> int, avl.select(r: int, v: int) -> int`
- `k` 番目の `0 / 1 / v` のインデックスを返します。
- `Θ(log^2 N)` です。logは1つにできるはずですが、めんどくて妥協してます。おそくてごめん

#### `len(avl) / str(avl) / repr(avl)`
- よしなに。