____

[CumulativeOp.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/CumulativeSum/CumulativeOp.py)

抽象化?累積和です。  

_____

## 仕様

#### `acc = CumulativeOp(a: Iterable[T], op: Callable[[T, T], T], inv: Callable[[T], T], e: T)`
- `a` から `CumulativeOp` を構築します。
- `op` は2項演算をする関数です。
- `inv` は逆元を返す関数です。 `prod` メソッドを使用する場合必要です。
- `e` は単位元です。
- `Θ(N)` です。

#### `acc.pref(r: int) -> T`
- 区間 `[0, r)` の演算結果を返します。
- `Θ(1)` です。

#### `acc.prod(l: int, r: int) -> T`
- 区間 `[l, r)` の演算結果を返します。
- `Θ(1)` です。

#### `acc.all_prod() -> T`
- 区間 `[0, N)` の演算結果を返します。
- `Θ(1)` です。

#### `acc[k] -> T`
- `k` 番目の値を返します。 `inv` は使用しません。
- `Θ(1)` です。

#### `len(acc)`
- 元の `a` の長さを返します。

#### `str(acc)`
- 累積和の `list` を表示します。
