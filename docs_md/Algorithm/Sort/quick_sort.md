_____

# `quick_sort`

_____

## コード

[`quick_sort`](https://github.com/titan-23/Library_py/blob/main/Algorithm/Sort/quick_sort.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/Algorithm\Sort\quick_sort.py -->

_____

- くいっくそーと

_____

## 仕様

#### `quick_sort(a: Iterable[T], key: Callable[[T, T], bool]=lambda s, t: s < t) -> List[T]:`

- 列 `a` をクイックソートします。
- 非破壊的です。
- 比較関数 `key` にしたがって比較演算をします。
  - `key: Callable[[T, T], bool]` です。
  - `(第1引数)<(第2引数)` のとき、 `True` を返すようにしてください。
- 時間計算量は期待 `O(nlogn)` です。
- 空間計算量は `O(n)` です。

_____

## 使用例

```python
from Library_py.Algorithm.Sort.quick_sort import quick_sort

a = [5, 3, 3, 1, 8, 2, 5]
a = quick_sort(a)
print(a)  # [1, 2, 3, 3, 5, 5, 8]
```
