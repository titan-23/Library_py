_____

# `HashString`

_____

## コード

[`HashString`](https://github.com/titan-23/Library_py/blob/main/String/HashString.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/String\HashString.py -->

_____

- ロリハです。
- `mod=(1<<61)-1`(固定)、`base=random.randint(37, 10**9)`です。
- 参考
  - [https://qiita.com/keymoon/items/11fac5627672a6d6a9f6](https://qiita.com/keymoon/items/11fac5627672a6d6a9f6)

_____

## 仕様

#### `hsb = HashStringBase(n: int)`
- Baseクラスです。
- `n` は文字列の長さの上限です。
- `O(n)` です。

#### `hs = HashString(hsb: HashStringBase, s: str, update: bool=False)`
- 文字列 `s` からロリハを構築します。
- `update=True` のとき、1点更新が可能になります。
  - 内部でセグ木を構築してます。
- `O(n)` です。

#### `hs.get(l: int, r: int) -> int`
- `s[l, r)` のハッシュ値を返します。
- 1点更新処理後は `O(logn)` 、そうでなければ `O(1)` です。

#### `hs[k: int] -> int`
- `s[k]` のハッシュ値を返します。
- 1点更新処理後は `O(logn)` 、そうでなければ `O(1)` です。

#### `hs.set(k: int, c: str) -> None / hs[k: int] = c: str`
- `k` 番目の文字を `c` に更新します。
- `O(logn)` です。また、今後の `get()` が `O(logn)` になります。

#### `hs.get_lcp() -> List[int]`
- lcp配列を返します。
- `O(nlogn)` です。

_____

## 使用例

[ABC331F Palindrome Query]()

```python
from Library_py.String.HashString import HashStringBase, HashString

import sys
from Library_py.IO.FastO import FastO
write, flush = FastO.write, FastO.flush
input = lambda: sys.stdin.readline().rstrip()

#  -----------------------  #

n, q = map(int, input().split())
s = input()
hsb = HashStringBase(n, 2)
hs  = HashString(hsb, s, update=True)
rhs = HashString(hsb, s[::-1], update=True)
for _ in range(q):
  com, a, b = input().split()
  if com == '1':
    x, c = int(a)-1, b
    hs[x] = c
    rhs[n-x-1] = c
  else:
    l, r = int(a)-1, int(b)
    u = hs.get(l, r)
    v = rhs.get(n-r, n-l)
    write('Yes' if u == v else 'No')
flush()
```
