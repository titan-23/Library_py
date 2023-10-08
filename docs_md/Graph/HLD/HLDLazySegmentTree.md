_____

# `HLDLazySegmentTree`

_____

## コード

[`HLDLazySegmentTree`](https://github.com/titan-23/Library_py/blob/main/Graph/HLD/HLDLazySegmentTree.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/Graph\HLD\HLDLazySegmentTree.py -->

_____


_____

## 仕様

あとで書く

_____

## 使用例

```python
from Library_py.Graph.HLD.HLD import HLD
from Library_py.Graph.HLD.HLDLazySegmentTree import HLDLazySegmentTree

n = int(input())
G = [[] for _ in range(n)]
for _ in range(n-1):
  u, v = map(int, input().split())
  u -= 1
  v -= 1
  G[u].append(v)
  G[v].append(u)

root = 0
hld = HLD(G, root)

op = lambda s, t: min(s, t)
mapping = lambda f, s: f
composition = lambda f, g: f
e = 1<<31
id = 0

seg = HLDLazySegmentTree(hld, n, op, mapping, composition, e, id)
```
