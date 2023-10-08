____

# `Deque`

____

## コード

[`Deque`](https://github.com/titan-23/Library_py/blob/main/DataStructures/Deque/Deque.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\Deque\Deque_.py -->

____

- `Deque` です。
- 先頭末尾の追加削除に加えて、`getitem / setitem` が `Θ(1)` で可能です。空間計算量は `Θ(N)` です。
- 内部ではデータを2つのスタックで管理しています。

____

## 仕様

#### `dq = Deque(a: Iterable[Any]=[])`

- `a` から `Deque` を構築します。
- `O(N)` です。

#### `dq.pop() / dq.popleft()`

- 末尾 / 先頭の要素を削除し、その値を返します。
- 償却 `O(1)` です。

#### `dq.append(v) / appendleft(v)`

- 要素 `v` を末尾 / 先頭に追加します。
- 償却 `O(1)` です。

#### `dq.tolist() -> List[Any]`

- `list` に変換します。 
- `O(N)` です。

#### `dq[k] / dq[k] = v`

- `getitem / setitem` です。
- `O(1)` です。うれしい。

#### `v in dq`

- `O(N)` です。

#### `bool(dq) / len(dq) / str(dq) / repr(dq)`

- よしなです。


## 使用例

- [https://atcoder.jp/contests/typical90/tasks/typical90_bi](https://atcoder.jp/contests/typical90/tasks/typical90_bi)

```python
from Library_py.DataStructures.Deque.Deque import Deque

q = int(input())
dq: Deque[int] = Deque()
for _ in range(q):
  t, x = map(int, input().split())
  if t == 1:
    dq.appendleft(x)  # O(1)
  elif t == 2:
    dq.append(x)  # O(1)
  else:
    print(dq[x-1])  # O(1)
```
