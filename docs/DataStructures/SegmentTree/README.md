_____

# `SegmentTree`

_____

## コード

# [`SegmentTree`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/SegmentTree/SegmentTree.py)

_____

- `SegmentTree` です。非再帰です。

_____

## 仕様

#### `seg = SegmentTree(n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], e: T)`  
- 第1引数 `n_or_a` が `n: int` のとき、 `e` を初期値として長さ `n` の `SegmentTree` を構築します。  
- 第1引数 `n_or_a` が `a: Iterable[T]` のとき、 `a` から `SegmentTree` を構築します。  
- いずれも `O(N)` です。

#### `seg.set(k: int, v: T) / seg[k] = v -> None`
- `k` 番目の値を `v` に更新します。
- `O(logN)` です。

#### `seg.get(k: int) / seg[k] -> T`  
- `k` 番目の値を返します。 
- `O(1)` です。

#### `seg.prod(l: int, r: int) -> T`  
- 区間 `[l, r)` の総積を返します。
- `O(logN)` です。

#### `seg.all_prod() -> T`  
- 区間 `[l, N)` の総積を返します。
- `O(1)` です。

#### `seg.max_right(l: int, f: Callable[[T], bool]) -> int`  
- Find the largest index R s.t. f([l, R)) == True.
- `O(logN)`

#### `seg.min_left(r: int, f: Callable[[T], bool]) -> int`  
- Find the smallest index L s.t. f([L, r)) == True.
- `O(logN)`

#### `seg.tolist() -> List[T]`
- 各要素からなる `List` を返します。
- `O(N)` です。

#### `seg.show() -> None`
- デバッグ用のメソッドです。

#### `str(seg) / repr(seg)`

