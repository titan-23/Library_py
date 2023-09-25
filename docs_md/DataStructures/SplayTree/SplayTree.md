_____

# [`SplayTree`](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BBST/SplayTree)

最終更新：2023/06/07
- READMEを修正しました。

splay操作をする木です。

_____

# [`LazySplayTree.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/SplayTree/LazySplayTree.py)
<!-- code=https://github.com/titanium-22/Library_py/blob/main/DataStructures\SplayTree\SplayTree.py -->

遅延伝播反転可能平衡二分木です。アホの定数倍をしています(定数倍が大きい方向にアホです)。

## `LazySplayTreeData`
モノイドのデータや作用、左右の子などを保持するクラスです。 `LazySplayTree` をインスタンス化する際に渡してください。  
`merge / split` する場合はそれらが同一の `LazySplayTreeData` を持つ必要があります。

## `LazySplayTree`

親へのポインタ持たせて～～

#### `st = LazySplayTree(data: LazySplayTreeData, n_or_a: Union[int, Iterable[T]]=0)`
- `data` から `LazySplayTree` を構築します。
- `n_or_a` が `int` のとき、`data.e` から長さ `n` の `st` が作られます。
`n_or_a` が `Iterable` のとき、`a` から `st` が作られます。
-  `O(N)` です。

#### `st.merge(other: LazySplayTree) -> None`
- `st` の後ろに `other` を連結します。
- 償却 `O(logN)` です。

#### `st.split(k: int) -> Tuple[LazySplayTree, LazySplayTree]`
- 2つの `LazySplayTree` を要素に持つタプルを返します。
  - 1要素目は `st` の `0` 番目から `k-1` 番目までを、2要素目は `k` 番目以降を要素に持ちます。
- 償却 `O(logN)` です。

#### `st.insert(k: int, key: T) -> None`
- 位置 `k` に `key` を挿入します。
- 償却 `O(logN)` です。

#### `st.append(key: T) / .appendleft(key: T) -> None`
- 末尾 / 先頭 に `key` を追加します。
- 償却 `O(logN)` です。

#### `st.pop(k: int=-1) / .popleft() -> T`
- `k` 番目 / 末尾 / 先頭 を削除しその値を返します。
- 償却 `O(logN)` です。

#### `st[k] -> T`
- `k` 番目を返します。
- 償却 `O(logN)` です。

#### `st[k] = key: T`
- `k` 番目を `key` に更新します。
- 償却 `O(logN)` です。

#### `st.copy() -> LazySplayTree`
- コピーします。
- `O(N)` です。

#### `st.reverse(l: int, r: int) -> None`
- 区間 `[l, r)` を反転します。 `reverse()` メソッドを一度でも使用するなら `op` には可換性が求められます(可換性がない場合、嘘の動作をします)。
- 償却 `O(logN)` です。

#### `st.all_reverse() -> None`
- 区間 `[0, N)` を反転します。
- `O(1)` です。

#### `st.apply(l: int, r: int, f: F) -> None`
- 区間 `[l, r)` に作用 `f` を適用します。
- 償却 `O(logN)` です。

#### `st.all_apply(f: F) -> None`
- 区間 `[0, N)` に作用 `f` を適用します。
- `O(1)` です。

#### `st.prod(l: int, r: int) -> T`
- 区間 `[l, r)` に `op` を適用した結果を返します。
- 償却 `O(logN)` です。

#### `st.all_prod() -> T`
- 区間 `[0, N)` の総積を返します。
- `O(1)` です。

#### `st.tolist() -> List[T]`
- `List` に変換します。非再帰です。
- `O(N)` です。

#### `iter(st) / next(st) / len(st) / str(st) / repr(st)`


## 使用例

```python
op = lambda s, t: s + t
mapping = lambda f, s: f
composition = lambda f, g: f
e = 0
id = 0
data = LazySplayTreeData(op, mapping, composition, e, id)

n, q = map(int, input().split())
A = list(map(int, input().split()))
splay = LazySplayTree(data, A)
for _ in range(q):
  qu = map(int, input().split())
  if

```
