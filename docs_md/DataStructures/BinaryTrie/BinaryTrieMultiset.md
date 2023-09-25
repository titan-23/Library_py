_____

# `BinaryTrieMultiset`

____

## コード
[`BinaryTrieMultiset`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BinaryTrie/BinaryTrieMultiset.py)
<!-- code=https://github.com/titanium-22/Library_py/blob/main/DataStructures\BinaryTrie\BinaryTrieMultiset.py -->

____

- `BinaryTrieMultiset` です。0以上u未満の整数からなる**多重**集合を管理できます。
- 空間 `O((要素数)logu)` のはずです。

____

## 仕様

[`OrderedMultisetInterface`](../../MyClass/OrderedMultisetInterface.md) を継承しています。

#### `bt = BinaryTrieMultiset(u: int, a: Iterable[int]=[])`
- `a` から、**0 以上 u 未満**の整数を管理する `BinaryTrieMultiset` を構築します。
- `O(nlogu)` です。

#### `bt.reserve(n: int) -> None`
- 内部のメモリを `O(n)` だけ確保します。
- `O(n)` です。

#### `bt.all_xor(x: int) -> None`
- すべての要素に `x` で `xor` をかけます。
- `O(1)` です。

#### `bt.index(key: int) / .index_right(key: int) -> int`
- `key` (より小さい / 以下の) 要素の数を返します。
- `O(logu)` です。

#### `bt[k: int] -> int`
- 昇順 `k` 番目の値を返します
- `O(logu)` です。

## 使用例

```python
q = int(input())
bt = BinaryTrieMultiset(1<<30)  # 0 以上 1<<30 未満の整数を管理する多重集合 bt を定義
bt.reserve(q)
for _ in range(q):
  t, x = map(int, input().split())
  if t == 0:
    bt.add(x)  # x を追加する
  elif t == 1:
    bt.discard(x)  # x を削除する
  else:
    # 全体に x を xor した時の最小値を出力する 
    bt.all_xor(x)
    print(bt[0])
    bt.all_xor(x)
```
