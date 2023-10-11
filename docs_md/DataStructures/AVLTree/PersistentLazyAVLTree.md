_____

# `PersistentLazyAVLTree`

_____

## コード

[`PersistentLazyAVLTree`](https://github.com/titan-23/Library_py/blob/main/DataStructures/AVLTree/PersistentLazyAVLTree.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\AVLTree\PersistentLazyAVLTree.py -->

_____

- ♰完全永続遅延伝播反転可能抽象化平衡二分探索木♰です。

_____

## 仕様

#### `avl = PersistentLazyAVLTree(a: Iterable[T],  op, mapping, composition, e, id)`

- `PersistentLazyAVLTree` を構築します。
- 時間・空間共に `O(N)` です。

#### `avl.merge(other: PersistentLazyAVLTree) -> PersistentLazyAVLTree`

- `avl` の後ろに `other` を連結？させた `PersistentLazyAVLTree` を返します。
- 時間・空間共に `O(logN)` です。

#### `avl.split(k: int) -> Tuple[PersistentLazyAVLTree, PersistentLazyAVLTree]`

- 時間・空間共に `O(logN)` です。

#### `avl.apply(l: int, r: int, f: F) -> PersistentLazyAVLTree`

- 時間・空間共に `O(logN)` です。

#### `avl.prod(l: int, r) -> T`

- 時間・空間共に `O(logN)` です。

#### `avl.insert(k: int, key: T) -> PersistentLazyAVLTree`

- 時間・空間共に `O(logN)` です。

#### `avl.pop(k: int) -> Tuple[PersistentLazyAVLTree, T]`

- 時間・空間共に `O(logN)` です。

#### `avl.reverse(l: int, r: int) -> PersistentLazyAVLTree`

- 時間・空間共に `O(logN)` です。

#### `avl.tolist() -> List[T]`

- 時間・空間共に `O(N)` です。

#### `avl[k: int] -> T`

- 時間 `O(logN)` 、空間 `O(1)` です。

#### `len(avl) / str(avl) / repr(avl)`


_____

## 使用例

[グラフではない](https://atcoder.jp/contests/arc030/submissions/45758203)

```python
op = lambda s, t: (s[0]+t[0], s[1]+t[1])
mapping = lambda f, s: (s[0] + f * s[1], s[1])
composition = lambda f, g: f + g
e = (0, 0)
id = 0

n, q = map(int, input().split())
X = list(map(int, input().split()))
X = [(x, 1) for x in X]
avl = PersistentLazyAVLTree(X, op, mapping, composition, e, id)
for _ in range(q):
  com, *qu = list(map(int, input().split()))
  if com == 1:
    a, b, v = qu
    a -= 1; b -= 1
    avl = avl.apply(a, b+1, v)
  if com == 2:
    a, b, c, d = qu
    a -= 1; b -= 1; c -= 1; d -= 1
    t, _ = avl.split(d+1)
    _, t = t.split(c)
    y, z = avl.split(b+1)
    x, _ = y.split(a)
    avl = x.merge(t)
    avl = avl.merge(z)
  if com == 3:
    a, b = qu
    a -= 1; b -= 1
    ans = avl.prod(a, b+1)[0]
    print(ans)
```
