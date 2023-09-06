___

# `BitVector`

_____

## コード

[`BitVector.py`](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BitVector/BitVector.py)

_____

- `BitVector` です。
- コンパクトのつもりでいます。
- `select` は `Θ(logN)` です。

_____

## 仕様

#### `v = BitVector(n: int)`
- 長さ `n` の `BitVector` を用意します。
- bit を保持するのに `array[I]` を使用します。
  - `block_size= n / 32` として、使用bitは `32*block_size=2n bit` です。
- 累積和を保持するのに同様の `array[I]` を使用します。
  - 32bitごとの和を保存しています。同様に使用bitは `2n bit` です。
- コンパクトです。

#### `v.set(k: int) -> None`
- `k` 番目の bit を `1` にします。
- `O(1)` です。

#### `v.build() -> None`
- 構築します。**これ以降`set`メソッドを使用してはいけません。**
- `O(n)` です。

#### `v.access(k: int) / v[k: int] -> int`
- `k` 番目の bit の値を返します。
- `__getitem__` メソッドをサポートしています。
- `O(1)` です。

#### `v.rank0(r: int) / v.rank1(r: int) / v.rank(r: int, v: int) -> int`
- `a[0, r)` に含まれる `0 / 1 / v` の個数を返します。
- `O(1)` です。

#### `v.select0(r: int) / v.select1(r: int) / v.select(r: int, v: int) -> int`
- `k` 番目の `0 / 1 / v` のインデックスを返します。
- `Θ(logN)` です。
