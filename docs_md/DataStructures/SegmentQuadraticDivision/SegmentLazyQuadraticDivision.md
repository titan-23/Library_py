_____

# `SegmentLazyQuadraticDivision`

_____

## コード

[`SegmentLazyQuadraticDivision`](https://github.com/titan-23/Library_py/blob/main/DataStructures/SegmentQuadraticDivision/SegmentLazyQuadraticDivision.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\SegmentQuadraticDivision\SegmentLazyQuadraticDivision.py -->

_____

- 区間の総積取得・区間への作用適用クエリをそれぞれ時間計算量 `O(N√N)` で処理できるデータ構造です。計算量が `O(N√N)` になった遅延セグ木ともみなせます。
- 定数倍が軽いのでそこまで遅くはないはずです。  

_____

## 仕様

#### `qd = SegmentLazyQuadraticDivision(n_or_a: Iterable[T], op: Callable[[T, T], T], mapping: Callable[[F, T], T], composition: Callable[F, F], F], e: T, id: F)`
- 列 `a` から `SegmentLazyQuadraticDivision` を構築します。その他引数は遅延セグ木のアレです。
- `n` の型を `int` にすると、 `n` 個の `e` からなる配列から構築します。
- 計算量 `O(N)` です。

#### `qd.apply(l: int, r: int, f: F) -> None`
- 区間 `[l, r)` に `f` を適用します。
- 計算量 `(O√N)` です。

#### `qd.all_apply(f: F) -> None`
- 区間 `[0, N)` に `f` を適用します。
- 計算量 `(O√N)` です。

#### `qd[k] -> T`
- `k` 番目の値を返します。
- 計算量 `(O√N)` です。

#### `qd[k] = key`
- `k` 番目の値を `key` に変更します。
- 計算量 `(O√N)` です。

#### `qd.prod(l: int, r: int) -> T`
- 区間 `[l, r)` に `op` を適用した総積を返します。
- 計算量 `(O√N)` です。

#### `qd.all_prod() -> T`
- 区間 `[0, N)` に `op` を適用した総積を返します。
- 計算量 `(O√N)` です。

_____

## 使用例

```python
```

