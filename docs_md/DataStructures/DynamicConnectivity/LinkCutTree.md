_____

# `LinkCutTree`

_____

## コード
[`LinkCutTree`](https://github.com/titan-23/Library_py/blob/main/DataStructures/DynamicConnectivity/LinkCutTree.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\DynamicConnectivity\LinkCutTree.py -->

_____

- `LinkCutTree` です。
- 森を管理します。パスクエリの強さに定評があります。

_____

## 仕様

#### `lct = LinkCutTree(n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T]=lambda x, y: None, mapping: Callable[[F, T], T]=lambda x, y: None, composition: Callable[[F, F], F]=lambda x, y: None, e: T=None, id: F=None)`

- `n_or_a`が `int` のとき、頂点数 `n` の `LinkCutTree` を構築します。`Iterable` のとき、頂点数はその長さとなります。`op, mapping, composition, e, id` は遅延セグ木のアレです。よしなに。
  - `op` は非可換でもよいです。

#### `lct.expose(v: int) -> int`

- `v` が属する木において、その木を管理しているsplay木の根からvまでのパスを作ります。

#### `lct.evert(v: int) -> None`

- `v` を根にします。
- `O(logN)` です。

#### `lct.link(c: int, p: int) -> None`

- 辺 `{c -> p}` を追加します。
- `O(logN)` です。

#### `lct.cut(c: int) -> None`

- 辺 `{c -> cの親}` を削除します。
- `O(logN)` です。

#### `lct.group_count() -> int`

- 連結成分数を返します。
- `O(1)` です。

#### `lct.root(v: int) -> int`

- `v` が属する木の根を返します。
- `O(logN)` です。

#### `lct.lca(u: int, v: int, root: int=-1) -> int`

- `u`, `v` の LCA を返します。`root` で根を指定することもできます。
- `O(logN)` です。

#### `lct.same(u: int, v: int) -> bool`

- `u`, `v` が同じ連結成分であれば `True` を、そうでなければ `False` を返します。
- `O(logN)` です。

#### `lct.merge(u: int, v: int) -> bool`

- `u`, `v` が同じ連結成分なら `False` を返します。そうでなければ辺 `{u -> v}` を追加して `True` を返します。
- `O(logN)` です。

#### `lct.split(u: int, v: int) -> bool`

- 辺 `{u - v}` があれば削除し `True` を返します。そうでなければ何もせず `False` を返します。
- `O(logN)` です。

#### `lct.path_prod(u: int, v: int) -> T`

- `u` から `v` へのパスの総積を返します。
- `O(logN)` です。

#### `lct.path_apply(u: int, v: int, f: F) -> None`

- `u` から `v` へのパスに `f` を作用させます。
- `O(logN)` です。

#### `lct.path_length(u: int, v: int) -> int`

- `u-v` パスの辺の個数を返します。
- `O(logN)` です。

#### `lct.path_kth_elm(s: int, t: int, k: int) -> int`

- `u` から `v` へ `k` 個進んだ頂点を返します。存在しないときは `-1` を返します。
- `O(logN)` です。

#### `lct[k] / lct[k] = v`

- 頂点 `k` の値を返します。
- `O(logN)` です。

#### `str(lct) / repr(lct)`

_____

## 使用例

```python
from Library_py.DataStructures.DynamicConnectivity.LinkCutTree import LinkCutTree

lct = LinkCutTree(10)
```
