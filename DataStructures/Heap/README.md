最終更新: 2023/4/26
- いろいろ更新しました。  

_____
# [IntervalHeap](https://github.com/titanium-22/Library_py/blob/main/DataStructures/Heap/IntervalHeap.py)

`IntervalHeap` です。  
値の追加/最小値取得/最大値取得 などができます。  
値の削除に対応した `MinMaxSet/Multiset` もどこかのフォルダにあります。

### ```hq = IntervalHeap(a: Iterable[T]=[])```
`Iterable a` から `IntervalHeap` を構築します。 $\mathcal{O}(N)$ です。

### ```hq.add(key: T) -> None```
`key` を1つ追加します。 $\mathcal{}(logN)$ です。

### ```hq.pop_min() -> T```
最小の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```hq.pop_max() -> T```
最大の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```hq.get_min() -> T```
最小の値を返します。 $\mathcal{O}(1)$ です。

### ```hq.get_max() -> T```
最大の値を返します。 $\mathcal{O}(1)$ です。

### ```len(hq) / bool(hq) / str(hq)```
よしなに動きます。

_____
# [RandomizedMeldableHeap](https://github.com/titanium-22/Library_py/blob/main/DataStructures/Heap/RandomizedMeldableHeap.py)

併合可能ヒープです。

