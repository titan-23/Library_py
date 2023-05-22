____

`Deque` です。
`getitem / setitem` が `O(1)` で可能です。


## 仕様

### `dq = Deque(a: Iterable[Any]=[])`
`Iterable a` から `Deque` を構築します。 `O(N)` です。

### `dq.pop() / dq.popleft()`
末尾 / 先頭を削除し、その値を返します。償却 `O(1)` です。

### `dq.append(v) / appendleft(v)`
`v` を末尾 / 先頭に追加します。償却 `O(1)` です。

### `dq.tolist() -> List[Any]`
`list` に変換します。 `O(N)` です。

### `dq[k] / dq[k] = v`
`getitem / setitem` です。 `O(1)` です。

### `v in dq`
`O(N)` です。

### `bool(dq) / len(dq) / str(dq) / repr(dq)`
よしなです。

