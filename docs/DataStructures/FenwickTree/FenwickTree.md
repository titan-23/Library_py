_____

# `FenwickTree`

_____

## コード

[`FenwickTree`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/FenwickTree/FenwickTree.py)
<!-- code=https://github.com/titanium-22/Library_py/blob/main/DataStructures\FenwickTree\FenwickTree_.py -->

_____

- `FenwickTree` です。
- 1点更新と区間和取得ができます。

_____

## 仕様

#### `fw = FenwicTree(n_or_a: Union[Iterable[int], int])`
- `n_or_a` が `int` のとき、初期値 `0` 、長さ `n` で構築します。
- `n_or_a` が `Iterable` のとき、初期値 `a` で構築します。
- 時間計算量 `O(n)` です。

#### `fw.pref(r: int) -> int`
- 区間 `[0, r)` の総和を返します。
- 時間計算量 `O(logn)` です。

#### `fw.suff(l: int) -> int`
- 区間 `[l, n)` の総和を返します。
- 時間計算量 `O(logn)` です。

#### `fw.sum(l: int, r: int) / prod -> int`
- 区間 `[l, r)` の総和を返します。
- 時間計算量 `O(logn)` です。

#### `fw[k: int] -> int`
- 位置 `k` の要素を返します。
- 時間計算量 `O(logn)` です。

#### `fw.add(k: int, x: int) -> None`
- 位置 `k` に `x` を加算します。
- 時間計算量 `O(logn)` です。

#### `fw[k: int] = x: int`
- 位置 `k` を `x` に更新します。
- 時間計算量 `O(logn)` です。

#### `fw.bisect_left(w: int) -> Optional[int]`

#### `fw.bisect_right(w: int) -> int`

#### `fw.tolist() -> List[int]`
- List にして返します。
- 時間計算量 `O(nlogn)` です。

#### `get_inversion_num(a: List[int], compress: bool=False) -> int`
- `staticmethod` です。
- List `a` の転倒数を返します。
- 時間計算量 `O(nlogn)` です。

_____

## 使用例

[Point Add Range Sum](https://judge.yosupo.jp/submission/148336)

```python
n, q = map(int, input().split())
A = list(map(int, input().split()))
fw = FenwickTree(A)
for _ in range(q):
  t, p, x = map(int, input().split())
  if t == 0:
    fw.add(p, x)
  else:
    l, r = p, x
    print(fw.sum(l, r))
```

