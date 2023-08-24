___

# `DynamicBitVector`

___

## コード
[`DynamicBitVector`](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BitVector/DynamicBitVector.py)

### import
- [`DynamicBitVector_SplayTreeList`](../BitVector/DynamicBitVector_SplayTreeList.md)

___

- `DynamicBitVector` です。
- 簡潔でもコンパクトでも何でもありません。ただの平衡二分木です。
  - `splay木` を使用しているため、以下は償却計算量となります。

___

## 仕様

#### `dv = DynamicBitVector(n_or_a: Union[int, Iterable[int]], data: Optional[DynamicBitVector_SplayTreeList_Data]=None)`
- 引数をもとに、`DynamicBitVector` を構築します。
  - `n` のとき、要素 `0` 長さ `n` です。
  - `a` のとき、`a` です。
  - `data` はあまりいじらなくてよいでしょう。内部用です。

#### `dv.reserve(n: int) -> None`
- メモリを確保します。
- `O(n)` です。

#### `dv.insert(k: int, v: int) -> None`
- `k` 番目に `v` を挿入します。
- `O(logn)` です。

#### `dv.pop(k: int) -> int`
- `k` 番目の要素を削除し、その値を返します。
- `O(logn)` です。

#### `dv.set(k: int, v: int=1) -> None / dv[k] = v`
- `k` 番目の bit を `v` にします。
- `__setitem__` メソッドをサポートしています。
- `O(logn)` です。

#### `dv.access(k: int) / a[k: int] -> int`
- `k` 番目の bit の値を返します。
- `__getitem__` メソッドをサポートしています。
- `O(logn)` です。

#### `dv.rank0(r: int) -> int, dv.rank1(r: int) -> int, dv.rank(r: int, v: int) -> int`
- `a[0, r)` に含まれる `0 / 1 / v` の個数を返します。
- `O(logn)` です。

#### `dv.select0(r: int) -> int, dv.select1(r: int) -> int, dv.select(r: int, v: int) -> int`
- `k` 番目の `0 / 1 / v` のインデックスを返します。
- `Θ(log^2 N)` です。おそくてごめん

#### `len(dv) / str(dv) / repr(dv)`
- よしなに。
