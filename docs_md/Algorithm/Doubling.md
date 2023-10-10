_____

# `Doubling`

_____

## コード

[`Doubling`](https://github.com/titan-23/Library_py/blob/main/Algorithm/Doubling.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/Algorithm\Doubling.py -->

_____

- ダブリングのライブラリです。

_____

## 仕様

#### `db = Doubling(n: int, lim: int, move_to: Callable[[T], T])`

- ダブリングテーブルを構築します。
- `n` はテーブルサイズです。
- `lim` はクエリの最大数です。
- `move_to(u) -> v` は遷移関数です。 `u` から `v` へ遷移します。
- `Θ(nlog(lim))` です。

#### `ans = db.kth(start: T, k: int) -> T`

- `start` から `k` 個進んだ状態を返します。
- `Θ(logk)` です。

_____

## 使用例

```python
from Library_py.Algorithm.Doubling import Doubling
```
