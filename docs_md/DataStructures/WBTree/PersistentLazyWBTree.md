_____

# `PersistentLazyWBTree`

_____

## コード

[`PersistentLazyWBTree`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/WBTree/PersistentLazyWBTree.py)
<!-- code=https://github.com/titanium-22/Library_py/blob/main/DataStructures\WBTree\PersistentLazyWBTree.py -->

_____

- `PersistentLazyWBTree` です。
- 永続化可能な平衡二分木が欲しくて作りました。
- `AVL` 木と比べると同程度っぽいです。

_____

## 仕様

あとで書く

_____

## 使用例

```python
from Library_py.DataStructures.WBTree.PersistentLazyWBTree import PersistentLazyWBTree

#  -----------------------  #

def not_graph():
  op = lambda s, t: (s[0]+t[0], s[1]+t[1])
  mapping = lambda f, s: (s[0] + f * s[1], s[1])
  composition = lambda f, g: f + g
  copy_t = lambda s: s
  copy_f = lambda f: f
  e = (0, 0)
  id = 0

  n, q = map(int, input().split())
  X = list(map(int, input().split()))
  X = [(x, 1) for x in X]
  tree = PersistentLazyWBTree(X, op, mapping, composition, e, id, copy_t, copy_f)
  for _ in range(q):
    com, *qu = list(map(int, input().split()))
    if com == 1:
      a, b, v = qu
      a -= 1; b -= 1
      tree = tree.apply(a, b+1, v)
    if com == 2:
      a, b, c, d = qu
      a -= 1; b -= 1; c -= 1; d -= 1
      t, _ = tree.split(d+1)
      _, t = t.split(c)
      y, z = tree.split(b+1)
      x, _ = y.split(a)
      tree = x.merge(t)
      tree = tree.merge(z)
    if com == 3:
      a, b = qu
      a -= 1; b -= 1
      ans = tree.prod(a, b+1)[0]
      write(ans)
  flush()

if __name__ == '__main__':
  not_graph()
```

