_____

# `HashSet`

_____

## コード

[`HashSet`](https://github.com/titan-23/Library_py/blob/main/DataStructures/Set/HashSet.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\Set\HashSet.py -->

_____

- ハッシュテーブルです。
- 組み込み辞書の `set` よりやや遅いです。とにかくハッシュ関数の質が悪いです。
- 削除クエリがくると、その遅さには特に目を見張るものがあります。視力を落としたくなければ使わないのが吉です。

_____

## 仕様

#### `s = HashSet(a: Iterable[int]=[], not_seen: int=-1, deleted: int=-2)`
- `a` から `HashSet` を作ります。
- `not_seen`, `deleted` はキーとして使用しない値を入れてください。デフォルト値はそれぞれ `-1`, `-2` であり、キーが非負整数と仮定しています。

#### `s.reserve(n: int) -> None`
- 空間 `O(n)` のメモリを確保します。

#### `s.add(key: int) -> bool`
- `key` が既に存在すれば何もせずに `False` を返します。そうでなければ `key` を追加して `True` を返します。期待 `O(1)` 時間です。

#### `s.discard(key: int) -> bool`
- `key` が存在してなければ何もせずに `False` を返します。そうでなければ `key` を削除して `True` を返します。期待 `O(1)` 時間です。

#### `key in s`
- `key` が存在すれば `True` を、そうでなければ `False` を返します。

#### `iter(s) / str(s) / len(s)`
- 毎度のよしなです。

_____

## 使用例

```python
from Library_py.DataStructures.Set.HashSet import HashSet

```
