_____

# `RedBlackTreeMultiset`

_____

## コード

[`RedBlackTreeMultiset`](https://github.com/titanium-22/Library_py/tree/main/DataStructures/RedBlackTree/RedBlackTreeMultiset.py)

_____

赤黒木です。多重集合です。 `std::set` も怖くない。

アルゴリズムイントロダクションを参考に書きました。

_____

## 仕様

多重集合としての赤黒木です。 主に [`RedBlackTreeSet`](RedBlackTreeSet.md) と同等の操作ができます。差分は以下です。

#### `rbtree = RedBlackTreeMultiset(a: Iterable[T]=[])`
- `a` から `RedBlackTreeMultiset` を構築します。
- ソート済みなら `O(N)` 、そうでないなら `O(NlogN)` です。

_____

## 使用例

```python
s = RedBlackTreeMultiset([3, 1, 4, 1, 5, 9])
it = s.ge_iter(3)
while it:
  print(it.key, it.count)
  it += 1

# 4 1
# 3 1
# 1 2
```
