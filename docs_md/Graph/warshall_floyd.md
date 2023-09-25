_____

# `warshall_floyd`

_____

## コード

[`warshall_floyd`](https://github.com/titanium-22/Library_py/blob/main/Graph/warshall_floyd.py)
<!-- code=https://github.com/titanium-22/Library_py/blob/main/Graph\warshall_floyd.py -->

_____

## 仕様

####  `warshall_floyd(G: List[List[Tuple[int, int]]]) -> List[List[Union[int, float]]]`
- 重み付き隣接リスト `G` に対し、全点対最短経路を返します。
- `O(N^3)` です。

_____

## 使用例

```python
n, m = int(input())
G = [[] for _ in range(n)]
for _ in range(m):
  # u -> v の無向辺, 距離c
  u, v, c = map(int, input().split())
  G[u].append((u, v, c))
dist = warshall_floyd(G)  # dist[i][j]:= (i -> j)の最短距離
```
