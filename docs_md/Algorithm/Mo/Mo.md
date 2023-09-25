_____

# `Mo`

_____

## コード

[`Mo`](https://github.com/titanium-22/Library_py/blob/main/Algorithm/Mo/Mo.py)
<!-- code=https://github.com/titanium-22/Library_py/blob/main/Algorithm/Mo/Mo.py -->

_____


- 列に対する `Mo's algorithm` です。

_____

## 仕様

#### `mo = Mo(n: int, q: int)`
- 長さ `n` の列、クエリ数 `q` に対する `Mo's algorithm` です。

#### `mo.add_query(l: int, r: int) -> None`
- 区間 `[l, r)` に対するクエリを追加します。
- `O(1)` です。

#### `mo.run(add: Callable[[int], None], delete: Callable[[int], None], out: Callable[[int], None]) -> None`
- 実行します。

#### `mo.runrun(add_left: Callable[[int], None], add_right: Callable[[int], None], delete_left: Callable[[int], None], delete_right: Callable[[int], None], out: Callable[[int], None]) -> None`
- 実行します。

