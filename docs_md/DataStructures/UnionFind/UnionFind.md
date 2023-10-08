_____

# `UnionFind`

_____

## コード

[`UnionFind.py`](https://github.com/titan-23/Library_py/blob/main/DataStructures/UnionFind/UnionFind.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\UnionFind\UnionFind_.py -->

_____

- `UnionFind` です。素集合データ構造です。 

_____

## 仕様

以下、α(N)をアッカーマン関数の逆関数とします。

#### `uf = UnionFind(n: int)`
- `n` 個の要素からなる `UnionFind` を構築します。
- 時間計算量 `Θ(N)` です。

#### `uf.root(x: int) -> int`
- 要素 `x` を含む集合の代表元を返します。

#### `uf.unite(x: int, y: int) -> int`
- 要素 `x` を含む集合と要素 `y` を含む集合を併合し、併合後の集合の代表元を返します。
- `Θ(α(N))` です。

#### `uf.same(x: int, y: int) -> bool`
- 要素 `x` と `y` が同じ集合に属するなら `True` を、そうでないなら `False` を返します。
- `Θ(α(N))` です。

#### `uf.size(x: int) -> int`
- 要素` x` を含む集合の要素数を返します。
- `Θ(α(N))` です。

#### `uf.members(x: int) -> Set[int]`
- 要素` x` を含む集合を返します。
- `Θ(n)`

#### `uf.all_roots() -> List[int]`
- 全ての集合の代表元からなるリストを返します。
- `Θ(N)` です。

#### `uf.group_count() -> int`
- `uf` の集合の総数を返します。
- `Θ(1)` です。

#### `uf.all_group_members() -> defaultdict[int, List[int]]`
- `key` に代表元、 `value` に `key` を代表元とする集合のリストをもつ `defaultdict` を返します。
- `Θ(Nα(N))` です。

#### `uf.claer() -> None`
- 集合を工場出荷状態に戻します。
- `Θ(N)` です。

#### `str(uf)`
- よしなにします。
- `ΘNα(N))` です。

_____

## 使用例

```python
from Library_py.DataStructures.UnionFind.UnionFind import UnionFind

```
