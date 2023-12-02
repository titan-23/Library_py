_____

# `Mo`

_____

## コード

[`Mo`](https://github.com/titan-23/Library_py/blob/main/Algorithm/Mo/Mo.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/Algorithm\Mo\Mo.py -->

_____


- 列に対する `Mo's algorithm` です。

_____

## 仕様

#### `mo = Mo(n: int, q: int)`

- 長さ `n` の列、クエリ数 `q` に対する `Mo's algorithm` です。

#### `mo.add_query(l: int, r: int) -> None`

- 区間 `[l, r)` に対するクエリを追加します。
- `O(1)` です。

#### `mo.run(add: Callable[[int], None], delete: Callable[[int], None], out: Callable[[int], None]) -> None`

- 実行します。

#### `mo.runrun(add_left: Callable[[int], None], add_right: Callable[[int], None], delete_left: Callable[[int], None], delete_right: Callable[[int], None], out: Callable[[int], None]) -> None`

- 実行します。

_____

## 使用例

[Range Set Query](https://atcoder.jp/contests/abc174/submissions/48086746)

```python
from Library_py.Algorithm.Mo.Mo import Mo

from Library_py.IO.FastO import FastO
write = FastO.write
flush = FastO.flush

import sys
from array import array
input = lambda: sys.stdin.buffer.readline().rstrip()

#  -----------------------  #

n, q = map(int, input().split())
C = array('I', map(int, input().split()))
mo = Mo(n, q)
for i in range(q):
  l, r = map(int, input().split())
  mo.add_query(l-1, r)
res = 0
cnt = array('I', bytes(4*(n+1)))
ans = array('I', bytes(4*q))
def add(k):
  ck = C[k]
  if not cnt[ck]:
    global res
    res += 1
  cnt[ck] += 1
def delete(k):
  ck = C[k]
  cnt[ck] -= 1
  if not cnt[ck]:
    global res
    res -= 1
def out(k):
  ans[k] = res
mo.run(add, delete, out)
print('\n'.join(map(str, ans)))
```
