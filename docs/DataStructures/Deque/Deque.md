____

# [Deque.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/Deque/Deque.py)

`Deque` です。

先頭末尾の追加削除に加えて、`getitem / setitem` が `O(1)` で可能です。空間計算量は `O(N)` です。

内部ではデータを2つのスタックで管理しています。

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

- https://atcoder.jp/contests/typical90/tasks/typical90_bi

```python
q = int(input())
dq = Deque()
for _ in range(q):
  t, x = map(int, input().split())
  if t == 1:
    dq.appendleft(x)
  elif t == 2:
    dq.append(x)
  else:
    print(dq[x-1])
```
