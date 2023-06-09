___

# [SegmentQuadraticDivision](https://github.com/titanium-22/Library/blob/main/QuadraticDivision/SegmentQuadraticDivision.py)

区間の総積取得クエリを時間計算量 `O(N√N)` で処理できるデータ構造です。計算量が `O(N√N)` になったセグ木ともみなせます。遅延評価の処理を必要としないため、[SegmentLazyQuadraticDivision](SegmentLazyQuadraticDivision.md)より定数倍が軽いです。  

## 仕様

計算量を明示していないものは計算量 `O(N√N)` です。

#### `qd = SegmentQuadraticDivision(n_or_a: Iterable[T], op: Callable[[T, T], T], e: T)`
- 列 `a` から `SegmentQuadraticDivision` を構築します。その他引数はセグ木のアレです。
`n` の型を `int` にすると `n` 個の `e` からなる配列で構築します。  
- 計算量 `O(N)` です。

