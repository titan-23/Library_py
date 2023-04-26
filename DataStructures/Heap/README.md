最終更新: 2022/12/15  
・いろいろ更新しました。  

_____
# [IntervalHeap](https://github.com/titanium-22/Library/blob/main/Heap/IntervalHeap.py)

$\mathsf{IntervalHeap}$ です。  
値の追加/最小値取得( $\mathsf{pop}$ )/最大値取得( $\mathsf{pop}$ ) などができます。

### ```hq = IntervalHeap(a: Iterable[T]=[])```
$\mathsf{Iterable}$ $\mathsf{a}$ から $\mathsf{IntervalHeap}$ を構築します。 $\mathcal{O}(N)$ です。

### ```hq.add(key: T) -> None```
$\mathsf{key}$ を1つ追加します。 $\mathcal{O}(logN)$ です。

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
# [MinMaxSet](https://github.com/titanium-22/Library/blob/main/Heap/MinMaxSet.py)

内部で $\mathsf{set}$ を持ち、データを管理します。  
値の追加/削除/存在判定/最小値取得( $\mathsf{pop}$ )/最大値取得( $\mathsf{pop}$ ) などができます。  
計算量は償却だったりします。

### ```st = MinMaxSet(a: Iterable[T]=[])```
$\mathsf{Iterable}$ $\mathsf{a}$ から $\mathsf{MinMaxSet}$ を構築します。 $\mathcal{O}(N)$ です。

### ```st.data: Set[T]```
内部データを管理している $\mathsf{set}$ です。

### ```st.add(key: T) -> None```
$\mathsf{key}$ が既に存在していれば、何もしません。そうでなければ $\mathsf{key}$ を1つ追加します。 $\mathcal{O}(logN)$ です。

### ```st.discard(key: T) -> bool```
$\mathsf{key}$ が存在すれば、削除して $\mathsf{True}$ を返します。そうでなければ、何も削除せずに $\mathsf{False}$ を返します。 $\mathcal{O}(logN)$ です。

### ```st.popleft() -> T```
最小の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```st.pop() -> T```
最大の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```st.get_min() -> T```
最小の値を返します。 $\mathcal{O}(1)$ です。

### ```st.get_max() -> T```
最大の値を返します。 $\mathcal{O}(1)$ です。

### ```st.to_l() -> List[T]```
$\mathsf{key}$ からなる $\mathsf{List}$ を返します。 $\mathcal{O}(NlogN)$ です。

### ```key in st / len(st) / bool(st) / str(st)```
よしなに動きます。


_____
# [MinMaxMultiSet](https://github.com/titanium-22/Library/blob/main/Heap/MinMaxMultiSet.py)

内部で $\mathsf{dict}$ を持ち、データを管理します。  
値の追加/削除/存在判定/最小値取得( $\mathsf{pop}$ )/最大値取得( $\mathsf{pop}$ ) などができます。  
計算量は償却だったりします。

### ```mst = MinMaxMultiSet(a: Iterable[T]=[])```
$\mathsf{Iterable}$ $\mathsf{a}$ から $\mathsf{MinMaxMultiSet}$ を構築します。 $\mathcal{O}(N)$ です。

### ```st.data: dict```
内部データを管理している $\mathsf{dict}$ です。

### ```mst.add(key: T, val: int=1) -> None```
$\mathsf{key}$ を $\mathsf{val}$ 個追加します。 $\mathcal{O}(logN)$ です。

### ```mst.discard(key: T, val: int=1) -> bool```
$\mathsf{key}$ が存在しなければ何も削除せずに $\mathsf{False}$ を返します。
そうでなければ、$\mathsf{key}$ を $\mathsf{min(mst.count(key), val)}$ 個削除し、 $\mathsf{True}$ を返します。 $\mathcal{O}(logN)$ です。

### ```mst.popleft() -> T```
最小の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```mst.pop() -> T```
最大の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```mst.get_min() -> T```
最小の値を返します。 $\mathcal{O}(1)$ です。

### ```mst.get_max() -> T```
最大の値を返します。 $\mathcal{O}(1)$ です。

### ```mst.count(key: T) -> int```
$\mathsf{key}$ の個数を返します。 $\mathcal{O}(1)$ です。

### ```mst.to_l() -> List[T]```
$\mathsf{key}$ からなる $\mathsf{List}$ を返します。 $\mathcal{O}(NlogN)$ です。

### ```key in mst / len(mst) / bool(mst) / str(mst)```
よしなに動きます。
