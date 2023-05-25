____

# [CumulativeSum.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/CumulativeSum/CumulativeSum.py)


1次元累積和です。  

_____

## 仕様

### `acc = CumulativeSum(a: Iterable[int], e: int=0)`
`Iterable a` から `CumulativeSum` を構築します。ここで、 `a` の任意の2要素に対して `+`, `-` 演算子が定義されている必要があります。また、単位元を `e=0` としています。
( `int` 型 `list` などを想定しています。)  
`O(N)` です。

### `acc.pref(r: int) -> int`
`sum(a[:r])` を返します。

### `acc.sum(l: int, r: int) / .prod(l, r) -> int`
`sum(a[l:r])` を返します。

### `acc.all_sum() / .all_prod() -> int`
`sum(a)` を返します。

### `acc[k] -> int`
`a[k]` を返します。

### `str(acc)`
累積和の `list` を表示します。
