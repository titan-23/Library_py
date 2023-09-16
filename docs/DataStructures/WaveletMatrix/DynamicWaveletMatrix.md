_____

# `DynamicWaveletMatrix`

_____

## コード

[`DynamicWaveletMatrix`](https://github.com/titanium-22/Library_py/tree/main/DataStructures/WaveletMatrix/DynamicWaveletMatrix.py)

_____

- `DynamicWaveletMatrix` です。
- [`WaveletMatrix`](./WaveletMatrix_.md) と大体同じです。
  - `BitVector` を平衡二分木にしています(`AVLTreeBitVector`)。あらゆる操作に平衡二分木の log がつきます。これヤバくね
- 未 verify が多いです。使わないのが吉でしょう。
- とにかく重いです。
  - 10^5 回のクエリで 4 秒弱です。病弱です。
- 高速化のため、アホの設計のもとコーディングをしています。
  - `AVLTreeBitVector` の `_insert_and_rank1` / `_access_pop_and_rank1` なるメソッドです。
  - そもそも設計なんてしてませんが。

_____

## 仕様

[`WaveletMatrix`](./WaveletMatrix_.md) との差分は以下です。(以下に示していないメソッドの時間計算量も `O(logn)` 倍されます。)

#### `wm = DynamicWaveletMatrix(sigma: int, a: Sequence[int]=[])`
- `[0, sigma)` の整数列を管理する `DynamicWaveletMatrix` です。
- 列 `a` から `DynamicWaveletMatrix` を構築します。

#### `wm.reserve(n: int) -> None`
- `n` 要素分のメモリを確保します。
- 時間計算量 `Θ(n)` です。

#### `wm.insert(k: int, x: int) -> None`
- 位置 `k` に `x` を挿入します。
- 時間計算量 `Θ(log(n)log(σ))` です。

#### `wm.pop(k: int) -> int`
- 位置 `k` の要素を削除し、その値を返します。
- 時間計算量 `Θ(log(n)log(σ))` です。

#### `wm.update(k: int, x: int) -> None / wm[k: int] = x: int`
- 位置 `k` の要素を `x` に更新します。
- `__setitem__` をサポートしています。
- 時間計算量 `Θ(log(n)log(σ))` です。

_____

## 使用例

```python
n = int(input())
A = list(map(int, input().split()))
dwm = DynamicWaveletMatrix(1<<30, A)
q = int(input())
for _ in range(q):
  c, l, r, k = map(int, input().split())
  if c == 0:
    v = wm.pop(r)
    wm.insert(l, v)
  if c == 1:
    print(dwm.kth_smallest(l, r, k))
```
