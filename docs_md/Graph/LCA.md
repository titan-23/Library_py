_____

# `LCA`

_____

## コード

[`LCA`](https://github.com/titan-23/Library_py/blob/main/Graph/LCA.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/Graph\LCA.py -->

_____

- `lca` を高速に求めます。
- オイラーツアーとスパーステーブルを用いて、構築 `Θ(NlogN)` クエリ `Θ(1)` で動作します。
- セグ木の方が速いと話題

_____

## 仕様

#### `tree = LCA(G: List[List[int]], root: int)`

- 根が `root` の重み無し隣接リスト `G` で表されるグラフに対して `lca` を求めます。
- 初期化時に前計算を行います。
- 計算量は時間・空間共に `Θ(NlogN)` です。

#### `tree.lca(u: int, v: int) -> int`

- 頂点 `u` と頂点 `v` の `lca` を返します。
- `Θ(1)` 時間です。

#### `tree.lca_mul(a: List[int]) -> int`

- 頂点集合 `a` の `lca` を返します。
- `Θ(|A|)` 時間です。

#### `tree.dist(u: int, v: int) -> int`

- 頂点 `u` と頂点 `v` の距離を返します。**全ての辺のコストが1のときのみ使用できます。**
- `Θ(1)` 時間です。

## 使用例

```python
n = int(input())
G = [[] for _ in range(n)]
for _ in range(n-1):
  u, v = map(int, input().split())
  u -= 1; v -= 1
  G[u].append(v)
  G[v].append(u)
tree = LCA(G, 0)  # Θ(nlogn)
q = int(input())
for _ in range(q):
  x, y = map(int, input().split())
  x -= 1; y -= 1
  print(tree.lca(x, y))  # Θ(1)
```
