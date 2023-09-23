
#### `x in bst / x not in bst`
- 存在判定です。
- `O(logN)` です。

#### `bst[k: int] -> T`
- 昇順 `k` 番目の値を返します
- `O(logN)` です。

#### `bst.add(key: T) -> bool`
- `key` が存在しないなら `key` を追加し `True` を返します。そうでないなら何も追加せず `False` を返します。
- `O(logN)` です。

#### `bst.discard(key: T) -> bool`
- `key` が存在するなら `key` を削除し `True` を返します。そうでないなら何もせず `False` を返します。
- `O(logN)` です。

#### `bst.le(key) / .lt(key) / .ge(key) / gt(key) -> Optional[T]`
- `key` (以下の / より小さい / 以上の / より大きい) 値で (最大 / 最大 / 最小 / 最小) の値を返します。存在しなければ `None` を返します。
- `O(logN)` です。

#### `bst.index(key: T) / .index_right(key: T) -> int`
- `key` (より小さい / 以下の) 要素の数を返します。
- `O(logN)` です。

#### `bst.pop(k: int=-1) / .pop_min() -> T`
- (最大(昇順k番目) / 最小) の値を削除し、その値を返します。
- `O(logN)` です。

#### `bst.clear() -> None`
- clearします。
- `O(1)` です。

#### `bst.tolist() -> List[T]`
- `key` を昇順に並べたリストを返します。
- `O(N)` です。
