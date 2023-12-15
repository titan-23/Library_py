_____

# `WordsizeTreeSet`

_____

## コード

[`WordsizeTreeSet`](https://github.com/titan-23/Library_py/blob/main/DataStructures/Set/WordsizeTreeSet.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\Set\WordsizeTreeSet.py -->

_____

- 32分木です。
- 空間 `O(u)` であることに注意してください。

_____

## 仕様

#### `wst = WordsizeTreeSet(u: int, a: Iterable[int]=[])`
- `[0, u)` の範囲の整数を管理する `WordsizeTreeSet` を構築します。
- `a` から構築します。

#### `wst.add(x: int) -> bool`

#### `wst.discard(x: int) -> bool`

#### `wst.ge / gt / le / lt -> Optional[int]`

#### `wst.get_min / get_max / pop_min / pop_max`

#### `wst.clear() -> None`

#### `wst.tolist() -> List[int]`

#### `x in wst`

#### `len / bool / iter / next / str / repr`

_____

## 使用例

```python
from Library_py.DataStructures.Set.WordsizeTreeSet import WordsizeTreeSet

u = 10**6
wst = WordsizeTreeSet(u)
for i in range(10):
  wst.add(i)
print(wst)  # {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
```
