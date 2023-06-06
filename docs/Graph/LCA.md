___

# [LCA.py](https://github.com/titanium-22/Library_py/blob/main/Graph/LCA.py)

## 仕様

### tree = LCA(G: List[List[int]], root: int)
根が `root` の隣接リスト `G` で表されるグラフに対して `lca` を求めます。内部ではオイラーツアーとスパーステーブルを用いて、構築 `O(NlogN)` 、クエリ `O(1)` を実現しています。  
初期化時に前計算を行っています。これは `O(NlogN)` 時間です。

### tree.lca(x: int, y: int) -> int
頂点 `x` と頂点 `y` の `lca` を返します。 `O(1)` 時間です。

### tree.lca_mul(a: List[int]) -> int
頂点集合 `a` の `lca` を求めます。 `O(|A|)` 時間です。

### tree.dist(x: int, y: int) -> int
頂点 `x` と頂点 `y` の距離を返します。 `O(1)` 時間です。**全ての辺のコストが1のときのみ使用できます。**

