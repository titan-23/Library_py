___

# `WaveletMatrix`

_____

## コード

[`WaveletMatrix`](https://github.com/titanium-22/Library_py/tree/main/DataStructures/WaveletMatrix/WaveletMatrix.py)

_____

- `WaveletMatrix` です。
- 静的であることに注意してください。
- 以下の仕様の計算量には嘘があるかもしれません。import 元の [`BitVector`](../BitVector/BitVector_.md) の計算量も参考にしてください。
- 未 verify が多いです。使わないのが吉でしょう。
- 参考:
  - [https://miti-7.hatenablog.com/entry/2018/04/28/152259](https://miti-7.hatenablog.com/entry/2018/04/28/152259){:target="_blank"}
  - [https://www.slideshare.net/pfi/ss-15916040](https://www.slideshare.net/pfi/ss-15916040){:target="_blank"}
  - [デwiki](https://scrapbox.io/data-structures/Wavelet_Matrix){:target="_blank"}

_____

## 仕様

#### `wm = WaveletMatrix(sigma: int, a: Sequence[int]=[])`
- `[0, sigma)` の整数列を管理する `WaveletMatrix` です。
- 列 `a` から `WaveletMatrix` を構築します。
- 時間計算量 `Θ(Nlog(σ))` です。
- 空間計算量 `Θ(Nlog(σ))` のはずです。

#### `wm.access(k: int) / wm[k: int] -> int`
- `a[k]` を返します。
- `__getitem__` をサポートしてます。
- 時間計算量 `Θ(log(σ))` です。

#### `wm.rank(r: int, x: int) -> int`
- `a[0, r)` に含まれる `x` の個数を返します。
- 時間計算量 `Θ(log(σ))` です。

#### `wm.select(k: int, x: int) -> int`
- `k` 番目の `v` のインデックスを返します。
- 時間計算量 `Θ(log(σ))` です。

#### `wm.kth_smallest(l: int, r: int, k: int) -> int`
- `wm.quantile(l, r, k)` と等価です。
- `a[l, r)` で `k` 番目に小さい値を返します。
- 時間計算量 `Θ(log(σ))` です。

#### `wm.kth_largest(l: int, r: int, k: int) -> int`
- `a[l, r)` で `k` 番目に**大きい値**を返します。
- 時間計算量 `Θ(log(σ))` です。

#### `wm.topk(l: int, r: int, k: int) -> List[Tuple[int, int]]`
- `a[l, r)` の中で、要素を出現回数が多い順にその頻度とともに `k` 個返します。
  - 返り値は `(要素, 頻度)` です。
- 時間計算量 `Θ(min(r-l, σ) log(σ))` です。
  - あやしいです。
  - `σ` が大きい場合、計算量に注意です。

#### `wm.sum(l: int, r: int) -> int`
- `a[l, r)` の総和を返します。
- 時間計算量 `Θ(min(r-l, σ) log(σ))` です。
  - `σ` が大きい場合、計算量に注意です。

#### `wm.range_freq(l: int, r: int, x: int, y: int) -> int`
- `a[l, r)` に含まれる、 `x` 以上 `y` 未満である要素の個数を返します。
- 時間計算量 `Θ(log(σ))` です。

#### `wm.prev_value(l: int, r: int, x: int) -> int`
- `a[l, r)` で、`x` 以上 `y` 未満であるような要素のうち最大の要素を返します。
- 時間計算量 `Θ(log(σ))` です。

#### `wm.next_value(l: int, r: int, x: int) -> int`
- `a[l, r)` で、`x` 以上 `y` 未満であるような要素のうち最小の要素を返します。
- 時間計算量 `Θ(log(σ))` です。

#### `wm.range_conut(l: int, r: int, x: int) -> int`
- `a[l, r)` に含まれる `x` の個数を返します。
- `wm.rank(r, x) - wm.rank(l, x)` と等価です。必要性
  - `range_freq` だと遅くなることに気を付けるためのメソッドです。
- 時間計算量 `Θ(log(σ))` です。

#### `len(wm) / str(wm)`
- よしなです。
- `len(wm)` の計算量は `Θ(1)` です。
