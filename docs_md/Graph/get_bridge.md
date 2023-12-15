_____

# `get_bridge`

_____

## コード

[`get_bridge`](https://github.com/titan-23/Library_py/blob/main/Graph/get_bridge.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/Graph\get_bridge.py -->

_____

_____

## 仕様

あとで書く

_____

## 使用例

- https://onlinejudge.u-aizu.ac.jp/courses/library/5/GRL/3/GRL_3_B

```python
from Library_py.Graph.get_bridge import get_bridge

#  -----------------------  #

import sys
sys.setrecursionlimit(7*10**5)
input = lambda: sys.stdin.buffer.readline().rstrip()

n, m = map(int, input().split())
G = [[] for _ in range(n)]
for _ in range(m):
  s, t = map(int, input().split())
  G[s].append(t)
  G[t].append(s)

bridge = get_bridge(G)
bridge = sorted((min(u, v), max(u, v)) for u, v in bridge)
for u, v in bridge:
  print(u, v)
```
