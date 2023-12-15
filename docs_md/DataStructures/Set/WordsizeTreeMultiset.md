_____

# `WordsizeTreeMultiset`

_____

## コード

[`WordsizeTreeMultiset`](https://github.com/titan-23/Library_py/blob/main/DataStructures/Set/WordsizeTreeMultiset.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\Set\WordsizeTreeMultiset.py -->

_____

- 32分木です。
- 空間 `O(u)` であることに注意してください。

_____

## 仕様

あとで書く

_____

## 使用例

```python
from Library_py.DataStructures.Set.WordsizeTreeMultiset import WordsizeTreeMultiset

u = 10**6
wst = WordsizeTreeMultiset(u)
for i in range(4):
  wst.add(i)
  wst.add(i)
print(wst)  # {0, 0, 1, 1, 2, 2, 3, 3}
```
