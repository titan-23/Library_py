_____

# `get_suffix_array`

_____

## コード

[`get_suffix_array`](https://github.com/titan-23/Library_py/blob/main/String/get_suffix_array.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/String\get_suffix_array.py -->

_____

- ソートします。
- ロリハで大小比較をするため、比較関数に `O(logn)` 、ソートが `O(nlogn*(比較関数の計算慮))` で、全体 `O(nlog^2n)` です。

_____

## 仕様

#### `get_suffix_array(s: str, hs: HashString) -> List[int]:`
- 文字列 `s` , `HashString hs` から `suffix_array` を返します。
- 計算量 `O(nlog^2n)` です。

_____

## 使用例

```python
from Library_py.String.get_suffix_array import get_suffix_array
from Library_py.String.HashString import HashString

s = input()
n = len(s)
hsb = HashStringBase(n)
hs = HashString(hsb, s)
sa = get_suffix_array(s, hs)
print(' '.join(map(str, sa)))
```
