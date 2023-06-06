___

# [warshall_floyd.py](https://github.com/titanium-22/Library_py/blob/main/Graph/warshall_floyd.py)

## 仕様
- `warshall_floyd(G: List[List[Tuple[int, int]]]) -> List[List[Union[int, float]]]`
引数は重み付き隣接リスト `G` です。戻り値は `G` の全点対最短経路です。計算量は `O(N^3)` です。

## 使用例
```
n, m = int(input())
G = [[] for _ in range(n)]
for _ in range(m):
  # u -> v の無向辺, 距離c
  u, v, c = map(int, input().split())
  G[u].append((u, v, c))
dist = warshall_floyd(G)
# dist[i][j]:= i -> jの最短距離
```
