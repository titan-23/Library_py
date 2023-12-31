_____

# `LazySplayTree`

_____

## コード

[`LazySplayTree`](https://github.com/titan-23/Library_py/blob/main/DataStructures/SplayTree/LazySplayTree.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\SplayTree\LazySplayTree.py -->

_____

_____

## 仕様

### `LazySplayTree`

#### `splay = LazySplayTree(n_or_a: Union[int, Iterable[T]], op, mapping, composition, e, id)`

- `n_or_a` から `LazySplayTree` を構築します。
  - `n_or_a` が `int` のとき、`data.e` から長さ `n` の `splay` が作られます。
  - `n_or_a` が `Iterable` のとき、`a` から `splay` が作られます。
- `O(N)` です。

#### `splay.merge(other: LazySplayTree) -> None`

- `splay` の後ろに `other` を連結します。
- 償却 `O(logN)` です。

#### `splay.split(k: int) -> Tuple[LazySplayTree, LazySplayTree]`

- 2つの `LazySplayTree` を要素に持つタプルを返します。
  - 1要素目は `splay` の `0` 番目から `k-1` 番目までを、2要素目は `k` 番目以降を要素に持ちます。
- 償却 `O(logN)` です。

#### `splay.insert(k: int, key: T) -> None`

- 位置 `k` に `key` を挿入します。
- 償却 `O(logN)` です。

#### `splay.append(key: T) / .appendleft(key: T) -> None`

- 末尾 / 先頭 に `key` を追加します。
- 償却 `O(logN)` です。

#### `splay.pop(k: int=-1) / .popleft() -> T`

- `k` 番目 / 末尾 / 先頭 を削除しその値を返します。
- 償却 `O(logN)` です。

#### `splay[k] -> T`

- `k` 番目を返します。
- 償却 `O(logN)` です。

#### `splay[k] = key: T`

- `k` 番目を `key` に更新します。
- 償却 `O(logN)` です。

#### `splay.copy() -> LazySplayTree`

- コピーします。
- `O(N)` です。

#### `splay.reverse(l: int, r: int) -> None`

- 区間 `[l, r)` を反転します。
- 償却 `O(logN)` です。

#### `splay.all_reverse() -> None`

- 区間 `[0, N)` を反転します。
- `O(1)` です。

#### `splay.apply(l: int, r: int, f: F) -> None`

- 区間 `[l, r)` に作用 `f` を適用します。
- 償却 `O(logN)` です。

#### `splay.all_apply(f: F) -> None`

- 区間 `[0, N)` に作用 `f` を適用します。
- `O(1)` です。

#### `splay.prod(l: int, r: int) -> T`

- 区間 `[l, r)` に `op` を適用した結果を返します。
- 償却 `O(logN)` です。

#### `splay.all_prod() -> T`

- 区間 `[0, N)` の総積を返します。
- `O(1)` です。

#### `splay.tolisplay() -> List[T]`

- `List` に変換します。非再帰です。
- `O(N)` です。

#### `iter(splay) / next(splay) / len(splay) / str(splay) / repr(splay)`

_____

## 使用例

```python
op = lambda s, t: s + t
mapping = lambda f, s: f
composition = lambda f, g: f
e = 0
id = 0

n, q = map(int, input().split())
A = list(map(int, input().split()))
splay = LazySplayTree(A, op, mapping, composition, e, id))
for _ in range(q):
  qu = map(int, input().split())
```
