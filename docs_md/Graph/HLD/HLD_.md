___

# `HLD`

_____

## コード

[`HLD.py`](https://github.com/titanium-22/Library_py/tree/main/Graph/HLD/HLD.py)

_____

- `HLD` です。

_____

## 仕様

#### `hld = HLD(G: List[List[int]], root: int)`
- `root` を根とする木 `G` から `HLD` を構築します。
- 時間・空間ともに `O(n)` です。
- 非再帰です（！）。

#### `hld.build_list(a: List[Any]) -> List[Any]`
- `hld配列` を基にインデックスを振りなおします。

#### `hld.for_each_vertex(u: int, v: int) -> Iterator[Tuple[int, int]]`
- `u-v` パスに対応する区間のインデックスを返します。
- `O(logn)` です。

#### `hld.for_each_vertex_subtree(v: int) -> Iterator[Tuple[int, int]]`
- 頂点 `v` の部分木に対応する区間のインデックスを返します。
- `O(1)` です。

#### `hld.path_kth_elm(s: int, t: int, k: int) -> int`
- `s` から `t` に向かって `k` 個進んだ頂点のインデックスを返します。
- 存在しないときは `-1` を返します。
- `O(logn)` です。

#### `hld.lca(u: int, v: int) -> int`
- `u`, `v` の `lca` を返します。
- `O(logn)` です。

_____

## 使用例

```python
n = int(input())
A = list(map(int, input().split()))
G = [[] for _ in range(n)]
for _ in range(n-1):
  u, v = map(int, input().split())
  G[u].append(v)
  G[v].append(u)

root = 0
hld = HLD(G, root)
hld_a = hld.build_list(a)
seg = SegmentTree(hld_a, op, e)

q = int(input())
for _ in range(q):
  u, v = map(int, input().split())
  res = e
  for s, t in hld.for_each_vertex(u, v):
    res = op(res, seg.prod(s, t))
  print(res)

```
