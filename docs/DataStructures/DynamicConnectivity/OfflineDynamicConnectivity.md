_____

# [OfflineDynamicConnectivity.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/DynamicConnectivity/OfflineDynamicConnectivity.py)

最終更新: 2023/6/5
- 書きました

参考: [ちょっと変わったセグメント木の使い方(ei1333の日記)](https://ei1333.hateblo.jp/entry/2017/12/14/000000)

_____

## 仕様

### `dc = OfflineDynamicConnectivity(n: int, q: int)`
頂点数 `n` 、クエリ数 `q` で初期化します。

### `dc.uf: UndoableUnionFind`
`dc` 内部で管理される `UndoableUnionFind` です。後述です。

### `dc.add_edge(u: int, v: int) -> None`
辺 `{u, v}` を追加します。

### `dc.delete_edge(u: int, v: int) -> None`
辺 `{u, v}` を削除します。

### `dc.add_relax() -> None`
何もしません。

### `dc.run(out: Callable[[int], None]) -> None`
実行します。 `out` 関数はクエリ番号 `k` を引数にとります。時間計算量 `O(q(logq)^2)` です。

### `dc.uf.size(x: int) -> int`
頂点 `x` を含む連結成分の頂点の総数を返します。

### `dc.uf.same(x: int, y: int) -> bool`
頂点 `x` と `y` の連結性判定です。

### `dc.uf.add(x: int, v: int) -> None`
頂点 `x` に値 `v` を加えます。

### `dc.uf.group_sum(x: int) -> int`
頂点 `x` を含む連結成分の頂点の総和を返します。

## 使用例


