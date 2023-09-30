`Set` に加えて、以下の操作ができます。  
valの値に関わらず `O(logN)` で動作します。

#### `bst.add(key: T, val: int=1) -> None`
- `key` を `val` 個追加します。
- `O(logN)` です。

#### `bst.discard(key: T, val: int=1) -> bool`
- `key` を `val` 個削除します。 `val` が `key` の数より大きいときは、 `key` を全て削除します。
- `key` が無いとき `False` を、そうでないときTrueを返します。
- `O(logN)` です。

#### `bst.dicard_all(key: T) -> None`
- `key` を全て削除します。
- `O(logN)` です。

#### `bst.count(key: T) -> int`
- 含まれる `key` の数を返します。
- `O(logN)` です。

#### `bst.index_keys(key: T) / index_right_keys(key: T) -> int`
- `key` (より小さい / 以下の) 要素の種類数を返します。
- `O(logN)` です。

#### `bst.tolist_items() -> Liset[Tuple[T, int]]`
- `key` で昇順に並べたリストを返します。各要素は `(key, st.count(key))` です。
- `O(N)` です。

#### `bst.keys() / values() / items()`
よしなに動きます。

#### `bst.get_elm(k: int) -> T`
- 要素の重複を除いたときの、昇順 `k` 番目の `key` を返します。
- `O(logN)` です。

#### `bst.len_elm() -> int`
- 要素の種類数を返します。
- `O(1)` です。

