____

# [CumulativeSum.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/CumulativeSum/CumulativeSum.py)

1次元累積和です。 `int` 型を想定しています。

_____

## 仕様

#### `acc = CumulativeSum(a: Iterable[int], e: int=0)`
- `a` から `CumulativeSum` を構築します。ここで、 `a` の任意の2要素に対して `+`, `-` 演算子が定義されている必要があります。単位元は `e=0` としています。
- `Θ(N)` です。

#### `acc.pref(r: int) -> int`
- `sum(a[:r])` を返します。
- `Θ(1)` です。

#### `acc.sum(l: int, r: int) / .prod(l: int, r: int) -> int`
- `sum(a[l:r])` を返します。
- `Θ(1)` です。

#### `acc.all_sum() / .all_prod() -> int`
- `sum(a)` を返します。
- `Θ(1)` です。

#### `acc[k] -> int`
- `a[k]` を返します。
- `Θ(1)` です。

#### `len(acc)`
- 元の `a` の長さを返します。

#### `str(acc)`
累積和の `list` を表示します。

## コード

<!-- <details><summary> CumulativeSum.py </summary> -->

```python
from typing import Iterable

class CumulativeSum():

  def __init__(self, a: Iterable[int], e: int=0):
    if not isinstance(a, list):
      a = list(a)
    n = len(a)
    acc = [e] * (n+1)
    for i in range(n):
      acc[i+1] = acc[i] + a[i]
    self.n = n
    self.acc = acc
    self.a = a

  def pref(self, r: int) -> int:
    assert 0 <= r <= self.n, \
        f'IndexError: CumulativeSum.pref({r}), n={self.n}'
    return self.acc[r]

  def all_sum(self) -> int:
    return self.acc[-1]

  def sum(self, l: int, r: int) -> int:
    assert 0 <= l <= r <= self.n, \
        f'IndexError: CumulativeSum.sum({l}, {r}), n={self.n}'
    return self.acc[r] - self.acc[l]

  prod = sum
  all_prod = all_sum

  def __getitem__(self, k: int) -> int:
    assert -self.n <= k < self.n, \
        f'IndexError: CumulativeSum[{k}], n={self.n}'
    return self.a[k]

  def __str__(self):
    return str(self.acc)

```

<!-- </details> -->
