_____

# `get_biconnected_components`

_____

## コード

[`get_biconnected_components`](https://github.com/titan-23/Library_py/blob/main/Graph/get_biconnected_components.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/Graph\get_biconnected_components.py -->

_____

- 二重頂点連結分解します。

_____

## 仕様

#### `vertex_ans, edge_ans = get_biconnected_components(G: List[List[int]])`
- `G` を二重頂点連結分解します。
- `vertex_ans: List[List[int]]`
  - 頂点集合です。
- `edge_ans: List[List[Tuple[int, int]]]`
  - 辺集合です。
- `O(n+m)` です。

_____

## 使用例

- [https://judge.yosupo.jp/problem/biconnected_components](https://judge.yosupo.jp/problem/biconnected_components)

```python
from Library_py.Graph.get_biconnected_components import get_biconnected_components

#  -----------------------  #

import sys
input = lambda: sys.stdin.buffer.readline().rstrip()
from Library_py.IO.FastO import FastO
write, flush = FastO.write, FastO.flush

n, m = map(int, input().split())
G = [[] for _ in range(n)]
for _ in range(m):
  a, b = map(int, input().split())
  G[a].append(b)
  G[b].append(a)
ans, _ = get_biconnected_components(G)
write(len(ans))
for v in ans:
  write(len(v), end=' ')
  write(' '.join(map(str, v)))
flush()
```
