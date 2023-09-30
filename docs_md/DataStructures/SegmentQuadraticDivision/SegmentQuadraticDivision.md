_____

# `SegmentQuadraticDivision`

_____

## コード

[`SegmentQuadraticDivision`](https://github.com/titan-23/Library/blob/main/QuadraticDivision/SegmentQuadraticDivision.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\SegmentQuadraticDivision\SegmentQuadraticDivision.py -->

_____

- 区間の総積取得クエリを時間計算量 `O(N√N)` で処理できるデータ構造です。計算量が `O(N√N)` になったセグ木ともみなせます。

_____

## 仕様

#### `qd = SegmentQuadraticDivision(n_or_a: Iterable[T], op: Callable[[T, T], T], e: T)`
- 列 `a` から `SegmentQuadraticDivision` を構築します。その他引数はセグ木のアレです。
`n` の型を `int` にすると `n` 個の `e` からなる配列で構築します。
- 計算量 `O(N)` です。

_____

## 使用例

```python
```

