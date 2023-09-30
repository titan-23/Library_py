_____

# `CumulativeSum2D`

_____

## コード

[`CumulativeSum2D`](https://github.com/titan-23/Library_py/blob/main/DataStructures/CumulativeSum/CumulativeSum2D.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\CumulativeSum\CumulativeSum2D.py -->

_____

- 2次元累積和です。 `int` 型を想定しています。
- 内部では、(2次元ではなく)1次元配列で累積和を管理しています。

_____

## 仕様

#### `acc = CumulativeSum2D(h: int, w: int, a: List[List[int]])`
- `h × w` のリスト `a` から2次元累積和の前計算をします。
- `Θ(hw)` です。

#### `acc.sum(h1: int, w1: int, h2: int, w2: int) -> int`
- 長方形領域 `[h1, h2) x [w1, w2)` の総和を返します。
- `Θ(1)` です。

