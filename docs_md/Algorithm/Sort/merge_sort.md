_____

# `merge_sort`

_____

## コード

[`merge_sort`](https://github.com/titan-23/Library_py/blob/main/Algorithm/Sort/merge_sort.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/Algorithm\Sort\merge_sort.py -->

_____

- まーじそーと

_____

## 仕様

#### `merge_sort(a: Iterable[T], key: Callable[[T, T], bool]=lambda s, t: s < t) -> List[T]:`

- 列 `a` をマージソートします。
- 非破壊的です。
- 比較関数 `key` にしたがって比較演算をします。
  - `key: Callable[[T, T], bool]` です。
  - `(第1引数)<(第2引数)` のとき、 `True` を返すようにしてください。
- 時間・空間ともに `Θ(nlogn)` です。

_____

## 使用例

```python
from Library_py.Algorithm.Sort.merge_sort import merge_sort

a = [5, 3, 3, 1, 8, 2, 5]
a = merge_sort(a)
print(a)  # [1, 2, 3, 3, 5, 5, 8]
```
