____

# `CumulativeSum`

_____

## コード

[`CumulativeSum`](https://github.com/titan-23/Library_py/blob/main/DataStructures/CumulativeSum/CumulativeSum.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\CumulativeSum\CumulativeSum_.py -->

_____

- 1次元累積和です。 `int` 型を想定しています。

_____

## 仕様

#### `acc = CumulativeSum(a: Iterable[int], e: int=0)`

- `a` から `CumulativeSum` を構築します。 `int` 型を想定しており、単位元は `e=0` としています。
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

#### `str(acc) / repr(acc)`

- 累積和の `list` を表示します。

_____

## 使用例

```python
```
