_____

# [OfflineDynamicConnectivity.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/DynamicConnectivity/OfflineDynamicConnectivity.py)

最終更新: 2023/06/17
- `q` を消しました
- `build()` メソッドを追加しました
- 連結成分加算に対応しました。


- 参考:
  - [ちょっと変わったセグメント木の使い方(ei1333の日記)](https://ei1333.hateblo.jp/entry/2017/12/14/000000)

- 実はlogを1つにできるらしいです。あとで理解を試みます。
  - [noshiさんのツイート](https://twitter.com/noshi91/status/1420179696965197824)

- その他
  - 内部では辺を `dict` で管理しています。メモリに注意です。
  - 長さ `q` のセグ木に辺を乗せます。メモリに注意です。

_____

## 仕様

#### `dc = OfflineDynamicConnectivity(n: int)`
- 頂点数 `n` で初期化します。
- `O(n)` です。

#### `dc.add_edge(u: int, v: int) -> None`
- 辺 `{u, v}` を追加します。
- `O(1)` です。

#### `dc.delete_edge(u: int, v: int) -> None`
- 辺 `{u, v}` を削除します。呼び出し前で存在していなければなりません。
- `O(1)` です。

#### `dc.add_relax() -> None`
- 何もしません。内部のクエリカウントを1増加させます。
- `O(1)` です。

#### `dc.build(E: List[Tuple[int, int]]) -> None`
- 辺のリスト `E` を初期メンバーとします。内部のクエリカウントを1増加させます。
- `O(|E|)` です。

#### `dc.run(out: Callable[[int], None]) -> None`
- 実行します。 `out` 関数はクエリ番号 `k` を引数にとります。
- `O(q(logq)(logn))` です。

#### `dc.uf: UndoableUnionFind`
- `dc` 内部で管理される `UndoableUnionFind` です。戦略は (undo操作のため) Union by size のみです。

#### `dc.uf.size(x: int) -> int`
- 頂点 `x` を含む連結成分の頂点の総数を返します。
- `O(logn)` です。

#### `dc.uf.same(x: int, y: int) -> bool`
- 頂点 `x` と `y` の連結性判定です。
- `O(logn)` です。

#### `dc.uf.add_point(x: int, v: int) -> None`
- 頂点 `x` に値 `v` を加算します。
- `O(logn)` です。

#### `dc.uf.add_group(x int, v: int) -> None`
- 頂点 `x` を含む連結成分の要素それぞれに `v` を加算します。
- `O(logn)` です。

#### `dc.uf.grouop_count(x: int) -> int`
- 連結成分の個数を返します。
- `O(1)` です。

#### `dc.uf.group_sum(x: int) -> int`
- 頂点 `x` を含む連結成分の頂点の総和を返します。
- `O(logn)` です。

## 使用例

```python
n, m = map(int, input().split())
dc = OfflineDynamicConnectivity(n)
E = []
for _ in range(m):
  u, v = map(int, input().split())
  E.append((u, v))
q = int(input())
dc.build(E)  # 初期辺を追加
Query = [list(map(int, input().split())) for _ in range(q)]
for t, u, v in Query:
  if t == 0:
    dc.add_edge(u, v)  # 辺 {u, v} の追加
  elif t == 1:
    dc.delete_edge(u, v)  # 辺 {u, v} の削除
  else:
    dc.add_relax()  # クエリ用

def out(k: int):
  t, x, _ = Query[k]
  if t == 2:
    # クエリ2で、頂点 x の連結成分の大きさを答える
    print(dc.uf.size(x))

dc.run(out)
```
