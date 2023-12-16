_____

# `FullyRetroactiveUnionFind`

_____

## コード

[`FullyRetroactiveUnionFind`](https://github.com/titan-23/Library_py/blob/main/DataStructures/UnionFind/FullyRetroactiveUnionFind.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\UnionFind\FullyRetroactiveUnionFind.py -->

_____

- `FullyRetroactiveUnionFind` です。
  - 適当です。

_____

## 仕様

#### `ruf = FullyRetroactiveUnionFind(n: int, m: int)`
- 頂点数 `n` 、クエリ列の長さ `m` の `FullyRetroactiveUnionFind` を作ります。
- `O(n+m)` です。

#### `ruf.unite(u: int, v: int, t: int) -> None`
- 時刻 `t` のクエリを `unite(u, v)` にします。
- **`disconnect` を使用する場合、 `u`, `v` が連結されていてはいけません。**
- 償却 `O(log(n+m))` です。

#### `ruf.disconnect(t: int) -> None`
- 時刻 `t` の連結クエリをなくして、そのクエリの2頂点を非連結にします。
- 償却 `O(log(n+m))` です。

#### `ruf.same(u: int, v: int, t: int) -> bool`
- 時刻 `t` で `u`, `v` の連結判定をします。
- 償却 `O(log(n+m))` です。

_____

## 使用例

```python
from Library_py.DataStructures.UnionFind.FullyRetroactiveUnionFind import FullyRetroactiveUnionFind

n, m = map(int,input().split())
uf = FullyRetroactiveUnionFind(n, m+1)
for i in range(m):
  u, v = map(int, input().split())
  u -= 1; v -= 1
  uf.unite(u, v, i+1)
```
