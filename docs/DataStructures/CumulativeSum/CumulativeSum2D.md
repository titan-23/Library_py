____

- [CumulativeSum2D.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/CumulativeSum/CumulativeSum2D.py)

2次元累積和です。 `int` 型を想定しています。

_____

## 仕様

#### `acc = CumulativeSum2D(h: int, w: int, a: List[List[int]])`
- `h × w` のリスト `a` から2次元累積和の前計算をします。
- `O(hw)` です。

#### `acc.sum(h1: int, w1: int, h2: int, w2: int) -> int`
- 長方形領域 `[h1, h2) x [w1, w2)` の総和を返します。
- `O(1)` です。
