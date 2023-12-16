_____

# `UndoableUnionFind`

_____

## コード

[`UndoableUnionFind`](https://github.com/titan-23/Library_py/blob/main/DataStructures/UnionFind/UndoableUnionFind.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\UnionFind\UndoableUnionFind.py -->

_____

- `UndoableUnionFind` です。

_____

## 仕様

#### `uf = UndoableUnionFind(n: int)`
- `n` 個の要素からなる `UndoableUnionFind` を構築します。
- `O(n)` です。

#### `uf.root(x: int) -> int`
- 要素 `x` を含む集合の代表元を返します。
- `O(logn)` です。

#### `uf.unite(x: int, y: int) -> bool`
- 要素 `x` を含む集合と要素 `y` を含む集合を併合します。
- もともと同じ集合であれば `False`、そうでなければ `True` を返します。
- `O(logn)` です。

#### `uf.undo() -> None`
- 直前の `unite` クエリを戻します。
- `O(1)` です。

#### `size / same / all_roots / all_group_members / clear`

#### `str`

_____

## 使用例

```python
from Library_py.DataStructures.UnionFind.UndoableUnionFind import UndoableUnionFind
```
