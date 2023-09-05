_____

# `RedBlackTreeMultiset`

_____

## コード

[`RedBlackTreeMultiset`](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BBST/RedBlackTree/RedBlackTreeMultiset.py)

_____

赤黒木です。多重集合です。 `std::set` も怖くない。

アルゴリズムイントロダクションを参考に書きました。

_____

## [`RedBlackTreeMultiset.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/RedBlackTree/RedBlackTreeMultiset.py)

多重集合としての赤黒木です。 主に [`RedBlackTreeSet`](RedBlackTreeSet.md) と同等の操作ができます。差分は以下です。

#### `rbtree = RedBlackTreeMultiset(a: Iterable[T]=[])`
- `a` から `RedBlackTreeMultiset` を構築します。
- ソート済みなら `O(N)` 、そうでないなら `O(NlogN)` です。

#### `rbtree.add(key: T, cnt: int=1) -> None`
- `key` を `cnt` 個追加ます。
- `cnt` の値に依らず `O(logN)` です。

#### `rbtree.discard(key: T, cnt: int=1) -> bool`
- `key` を `min(cnt, rbtree.count(key))` 個削除します。
- `cnt` の値に依らず `O(logN)` です。

#### `rbtree.discard_all(key: T) -> bool`
- `key` が存在すればすべて削除し `True` を返します。そうでなければ何もせず `False` を返します。
- `O(logN)` です。

### 使用例

```python
s = RedBlackTreeMultiset([3, 1, 4, 1, 5, 9])
it = s.ge_iter(3)
while it:
  print(it.key, it.count, end=' ')
  it += 1

# 4 1
# 3 1
# 1 2
```
