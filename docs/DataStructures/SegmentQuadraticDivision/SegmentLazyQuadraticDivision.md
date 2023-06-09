___

# [SegmentLazyQuadraticDivision](https://github.com/titanium-22/Library_py/blob/main/DataStructures/SegmentQuadraticDivision/SegmentLazyQuadraticDivision.py)

最終更新：2023/06/09
- readmeを整備しました

区間の総積取得・区間への作用適用クエリをそれぞれ時間計算量 `O(N√N)` で処理できるデータ構造です。計算量が `O(N√N)` になった遅延セグ木ともみなせます。定数倍が軽いのでそこまで遅くはないはずです。  

## 仕様

計算量を明示していないものは計算量 `(O√N)` とします。  

#### `qd = SegmentLazyQuadraticDivision(n_or_a: Iterable[T], op: Callable[[T, T], T], mapping: Callable[[F, T], T], composition: Callable[F, F], F], e: T)`
- 列 `a` から `SegmentLazyQuadraticDivision` を構築します。その他引数は遅延セグ木のアレです。
- `n` の型を `int` にすると、 `n` 個の `e` からなる配列から構築します。
- 計算量 `O(N)` です。

#### `qd.apply(l: int, r: int, f: F) -> None`
- 区間 `[l, r)` に `f` を適用します。

#### `qd.all_apply(f: F) -> None`
- 区間 `[0, N)` に `f` を適用します。

#### `qd[k] -> T`
- `k` 番目の値を返します。

#### `qd[k] = key`
- `k` 番目の値を `key` に変更します。

#### `qd.prod(l: int, r: int) -> T`
- 区間 `[l, r)` に `op` を適用した総積を返します。

#### `qd.all_prod() -> T`
- 区間 `[0, N)` に `op` を適用した総積を返します。

