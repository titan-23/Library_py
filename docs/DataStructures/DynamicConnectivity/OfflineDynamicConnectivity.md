_____

# [OfflineDynamicConnectivity.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/DynamicConnectivity/OfflineDynamicConnectivity.py)

最終更新: 2023/06/07
- 書きました

参考: [ちょっと変わったセグメント木の使い方(ei1333の日記)](https://ei1333.hateblo.jp/entry/2017/12/14/000000)

_____

## 仕様

#### `dc = OfflineDynamicConnectivity(n: int, q: int)`
- 頂点数 `n` 、クエリ数 `q` で初期化します。
- `O(1)` です。

#### `dc.uf: UndoableUnionFind`
- `dc` 内部で管理される `UndoableUnionFind` です。後述です。

#### `dc.add_edge(u: int, v: int) -> None`
- 辺 `{u, v}` を追加します。
- `O(1)` です。

#### `dc.delete_edge(u: int, v: int) -> None`
- 辺 `{u, v}` を削除します。呼び出し前で存在していなければなりません。
- `O(1)` です。

#### `dc.add_relax() -> None`
- 何もしません。内部のクエリカウントを1増加させます。
- `O(1)` です。

#### `dc.run(out: Callable[[int], None]) -> None`
- 実行します。 `out` 関数はクエリ番号 `k` を引数にとります。
- `O(q(logq)(logn))` です。

#### `dc.uf.size(x: int) -> int`
- 頂点 `x` を含む連結成分の頂点の総数を返します。
- 戦略は (undo操作のため) Union by size のみであり `O(logn)` です。

#### `dc.uf.same(x: int, y: int) -> bool`
- 頂点 `x` と `y` の連結性判定です。
- `O(logn)` です。

#### `dc.uf.add(x: int, v: int) -> None`
- 頂点 `x` に値 `v` を加算します。
- `O(logn)` です。

#### `dc.uf.grouop_count(x: int) -> int`
- 連結成分の個数を返します。
- `O(1)` です。

#### `dc.uf.group_sum(x: int) -> int`
- 頂点 `x` を含む連結成分の頂点の総和を返します。
- `O(logn)` です。

## 使用例
```
n, q = map(int, input().split())
dc = OfflineDynamicConnectivity(n, q)
for _ in range(q):
  t, u, v = map(int, input().split())
  if t == 0:
    # 辺 {u, v} の追加
    dc.add_edge(u, v)
  else:
    # 辺 {u, v} の削除
    dc.delete_edge(u, v)
def out(k: int):
  # 各クエリ後、頂点0の連結成分の大きさを答える
  print(dc.uf.size(0))
dc.run(out)
```
