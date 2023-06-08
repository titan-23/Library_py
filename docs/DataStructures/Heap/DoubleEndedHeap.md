___

# [DoubleEndedHeap.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/Heap/DoubleEndedHeap.py)

`DoubleEndedHeap` です。  
値の追加/最小値取得/最大値取得 などができます。  
値の削除に対応した `MinMaxSet/Multiset` もどこかのデイレクトリにあります。  

参考です。  

- [両端優先度付きキューのInterval-Heap実装](https://natsugiri.hatenablog.com/entry/2016/10/10/035445)
- [Double-ended priority queue(wikipedia)](https://en.wikipedia.org/wiki/Double-ended_priority_queue)

___

#### `hq = DoubleEndedHeap(a: Iterable[T]=[])`
- `a` から `DoubleEndedHeap` を構築します。
- `O(N)` です。

#### `hq.add(key: T) -> None`
- `key` を1つ追加します。
- `O(logN)` です。

#### `hq.pop_min() -> T`
- 最小の値を削除し返します。
- `O(logN)` です。

#### `hq.pop_max() -> T`
- 最大の値を削除し返します。
- `O(logN)` です。

#### `hq.get_min() -> T`
- 最小の値を返します。
- `O(1)` です。

#### `hq.get_max() -> T`
- 最大の値を返します。
- `O(1)` です。

#### `len(hq) / bool(hq) / str(hq)`
- よしなに動きます。

