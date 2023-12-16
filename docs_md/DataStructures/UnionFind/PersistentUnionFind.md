_____

# `PersistentUnionFind`

_____

## コード

[`PersistentUnionFind`](https://github.com/titan-23/Library_py/blob/main/DataStructures/UnionFind/PersistentUnionFind.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\UnionFind\PersistentUnionFind.py -->

_____

- `PersistentUnionFind` です。

_____

## 仕様

#### `puf = PersistentUnionFind(n: int)`
- `n` 個の要素からなる `PersistentUnionFind` を構築します。
- 計算量 `O(N)` です。

#### `puf.copy() -> 'PersistentUnionFind'`
- copyして返します。
- `O(1)` です。

#### `puf.root(x: int) -> int`
- 要素 `x` を含む集合の代表元を返します。
- `O((logn)^2)` です。

#### `puf.unite(x: int, y: int) -> bool`
- `O((logn)^2)` です。

#### `puf.size(x: int) -> int`
- `O((logn)^2)` です。

#### `puf.same(x: int, y: int) -> bool`
- `O((logn)^2)` です。

_____

## 使用例

```python
from Library_py.DataStructures.UnionFind.PersistentUnionFind import PersistentUnionFind

n = int(input())
puf = PersistentUnionFind(n)
```
