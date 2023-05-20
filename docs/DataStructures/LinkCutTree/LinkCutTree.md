_____

# [LinkCutTree](https://github.com/titanium-22/Library_py/blob/main/DataStructures/LinkCutTree)

最終更新: 2023/4/26
- いろいろ更新しました。  

_____

# [LinkCutTree.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/LinkCutTree/LinkCutTree.py)

`LinkCutTree` です。森を管理します。パスクエリの強さに定評があります。

### `lct = LinkCutTree(n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T]=lambda x, y: None, mapping: Callable[[F, T], T]=lambda x, y: None, composition: Callable[[F, F], F]=lambda x, y: None, e: T=None, id: F=None)`
`n_or_a`が `int` のとき、頂点数 `n` の `LinkCutTree` を構築します。`Iterable` のとき、頂点数はその長さとなります。  
`op, mapping, composition, e, id` は遅延セグ木のアレです。よしなに。

### `lct.expose(v: int) -> int`
`v` が属する木において、その木を管理しているsplay木の根からvまでのパスを作ります。

### `lct.evert(v: int)`
`v` を根にします。

### `lct.link(c: int, p: int)`
辺 `{c, p}` を追加します。

### `lct.cut(c: int)`

### `lct.group_count()`

### `lct.root(v: int)`

### `lct.lca(u: int, v: int)`

### `lct.same(u: int, v: int)`

### `lct.prod(u: int, v: int)`

### `lct.apply(u: int, v: int)`

### `lct.merge(u: int, v: int)`

### `lct.split(u: int, v: int)`

### `lct.path_kth_elm(s: int, t: int, k: int)`

### `lct[k] / lct[k] = v`

### `str(lct) / repr(lct)`
