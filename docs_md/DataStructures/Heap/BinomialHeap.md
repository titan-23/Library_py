_____

# `BinomialHeap`

_____

## コード

[`BinomialHeap`](https://github.com/titan-23/Library_py/blob/main/DataStructures/Heap/BinomialHeap.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures\Heap\BinomialHeap.py -->

_____

- 2項ヒープです。
- 計算量はメチャクチャさぼってます。
  - あらゆる操作が `θ(logn)` です。
- `List` の代わりに `LinkedList` を使用し、`push,meld` では `O(1)` で連結させ、 `delete_min` にすべてを押し付けると `push,meld` が `O(1)` 、`delete_min` が償却 `O(logn)` になるはずです。 

_____

## 仕様


_____

## 使用例

```python
from Library_py.DataStructures.Heap.BinomialHeap import BinomialHeap
```
