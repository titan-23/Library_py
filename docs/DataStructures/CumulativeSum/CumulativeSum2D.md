____

- [CumulativeSum2D.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/CumulativeSum/CumulativeSum2D.py)

- 2次元累積和です。 `int` 型を想定しています。
- 内部では、2次元ではなく1次元配列で累積和を管理しています。

_____

## 仕様

#### `acc = CumulativeSum2D(h: int, w: int, a: List[List[int]])`
- `h × w` のリスト `a` から2次元累積和の前計算をします。
- `O(hw)` です。

#### `acc.sum(h1: int, w1: int, h2: int, w2: int) -> int`
- 長方形領域 `[h1, h2) x [w1, w2)` の総和を返します。
- `O(1)` です。

## 使用例

```python
from typing import List

class CumulativeSum2D():

  def __init__(self, h: int, w: int, a: List[List[int]]):
    acc = [0] * ((h+1)*(w+1))
    for ij in range(h*w):
      i, j = divmod(ij, w)
      acc[(i+1)*(w+1)+j+1] = acc[i*(w+1)+j+1] + acc[(i+1)*(w+1)+j] - acc[i*(w+1)+j] + a[i][j]
    self.h = h
    self.w = w
    self.acc = acc

  def sum(self, h1: int, w1: int, h2: int, w2: int) -> int:
    assert h1 <= h2 and w1 <= w2, f'IndexError'
    return self.acc[h2*(self.w+1)+w2] - self.acc[h2*(self.w+1)+w1] - self.acc[h1*(self.w+1)+w2] + self.acc[h1*(self.w+1)+w1]
```
