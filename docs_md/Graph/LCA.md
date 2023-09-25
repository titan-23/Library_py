_____

# `LCA`

_____

## コード

[`LCA.py`](https://github.com/titanium-22/Library_py/blob/main/Graph/LCA.py)
<!-- code=https://github.com/titanium-22/Library_py/blob/main/Graph\LCA.py -->

_____

- オイラーツアーとスパーステーブルを用いて、構築 `O(NlogN)` クエリ `O(1)` を実現しています。
- セグ木の方が速いと話題

_____

## 仕様

#### `tree = LCA(G: List[List[int]], root: int)`
- 根が `root` の重み無し隣接リスト `G` で表されるグラフに対して `lca` を求めます。
- 初期化時に前計算を行っています。
- 計算量は時間・空間共に `O(NlogN)` です。

#### `tree.lca(x: int, y: int) -> int`
- 頂点 `x` と頂点 `y` の `lca` を返します。
- `O(1)` 時間です。

#### `tree.lca_mul(a: List[int]) -> int`
- 頂点集合 `a` の `lca` を求めます。
- `O(|A|)` 時間です。

#### `tree.dist(x: int, y: int) -> int`
- 頂点 `x` と頂点 `y` の距離を返します。**全ての辺のコストが1のときのみ使用できます。**
- `O(1)` 時間です。


## 使用例
```python
n = int(input())
G = [[] for _ in range(n)]
for _ in range(n-1):
  u, v = map(int, input().split())
  u -= 1; v -= 1
  G[u].append(v)
  G[v].append(u)
tree = LCA(G, 0)  # O(nlogn)
q = int(input())
for _ in range(q):
  x, y = map(int, input().split())
  x -= 1; y -= 1
  print(tree.lca(x, y))  # O(1)
```
