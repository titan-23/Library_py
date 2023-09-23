_____

# `SparseTable`

_____

## コード

[`SparseTable`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/SparseTable/SparseTable.py)

_____

- `SparseTable` です。
- 静的であることに注意してください。
- 構築 `O(NlogN)` 、クエリ `O(1)` です。
  - メモリに注意です。
  - 競プロ範囲ではセグ木の方が速かったりします。

_____

## 仕様

#### `st = SparseTable(a: Iterable[T], op: Callable[[T, T], T], e: T=None)`
- `a / op / e` からスパテを構築します。
- 時間、空間ともに `O(NlogN)` の計算量です。

#### `st.prod(l: int, r: int) -> T`
- `a[l,r)` の総積を返します。
- `O(1)` です。

#### `st[k: int] -> T`
- `a[k]` を返します。
- `O(1)` です。

#### `len(st) / str(st) / repr(st)`
- よしなです。

