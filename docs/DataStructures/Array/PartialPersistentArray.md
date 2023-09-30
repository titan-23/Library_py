_____

# `PartialPersistentArray`

_____

## コード

[`PartialPersistentArray`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/Array/PartialPersistentArray.py)
<!-- code=https://github.com/titanium-22/Library_py/blob/main/DataStructures/Array/PartialPersistentArray.py -->

_____

- 部分永続配列です。
  - 最新版の更新と、過去へのアクセスが可能です。

_____

## 仕様

#### `pa = PartialPersistentArray(a: Iterable[T])`
- `a` から部分永続配列を作ります。
- 初期配列のバージョンは `0` です。
- `O(N)` です。

#### `pa.set(k: int, v: T, t: int) -> None`
- `pa` を更新します。
  - 位置 `k` を `v` に更新します。
  - 新たな永続配列のバージョンを `t` とします。
- `O(1)` です。

#### `pa.get(k: int, t: int=-1) -> T`
- 位置 `k` 、バージョン `t` の要素を返します。
  - `t=-1` のとき、バージョンを最新版とします。
- `O(logN)` です。

#### `pa.tolist(t: int) -> List[T]`
- バージョン `t` の配列を返します。
- `O(NlogN)` です。

#### `pa.show(t: int) -> None`
- バージョン `t` の配列を表示します。
- `O(NlogN)` です。

#### `pa.show_all() -> None`
- すべてのバージョンの配列を表示します。
- `O(NlogN)` です。

#### `len(pa)`
- よしなです。

_____

