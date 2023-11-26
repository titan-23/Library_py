_____

# `MexMultiset`

_____

## コード

[`MexMultiset`](https://github.com/titan-23/Library_py/blob/main/DataStructures/Set/MexMultiset.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\Set\MexMultiset.py -->

_____

- `MexMultiset` です。
- 各操作には `log` がつきますが、ANDセグ木の `log` で割と軽いです。

_____

## 仕様

#### `mx = MexMultiset(u: int, a: Iterable[int]=[])`
- `[0, u)`の範囲のmexを計算するMexMultisetを構築します。
- `a`の長さを`N`として、`Θ(N)` です。

#### `mx.add(key: int) -> None`
- `key` を追加します。
- `Θ(logN)` です。

#### `mx.remove(key: int) -> None`
- `key` を削除します。 `key` は `mx` 内にあるとします。
- `Θ(logN)` です。

#### `mx.mex() -> int`
- `mx` の `mex` を返します。
- `Θ(logN)` です。セグ木の`max_right()`関数を使用しています。

_____

## 使用例

- [ABC330E Mex and Update](https://atcoder.jp/contests/abc330/submissions/47972707)

```python
from Library_py.DataStructures.Set.MexMultiset import MexMultiset

import sys
from Library_py.IO.FastO import FastO
write, flush = FastO.write, FastO.flush
input = lambda: sys.stdin.buffer.readline().rstrip()

#  -----------------------  #

n, q = map(int, input().split())
A = list(map(int, input().split()))
mx = MexMultiset(n, A)
for _ in range(q):
  i, x = map(int, input().split())
  i -= 1
  mx.remove(A[i])
  A[i] = x
  mx.add(A[i])
  write(mx.mex())
flush()
```
