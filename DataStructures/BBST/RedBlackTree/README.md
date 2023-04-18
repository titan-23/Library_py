最終更新：2023/04/18  
- いろいろ更新しました。  

_____
# Node
Nodeです。双方向にられ進められます。計算量は平均O(1)、最悪O(logN)です。

### node += 1 / node -= 1
nodeを次/前のnodeにします。存在しないときはNoneになります。

### node + 1 / node - 1
次/前のnodeを返します。存在しないときはNoneを返します。

_____
# [RedBlackTreeSet](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/RedBlackTree/RedBlackTreeSet.py)
集合としての赤黒木です。以下の操作ができます:  
Add / Delete / Find / Predecessor / Successor /  
詳しくは下記です。

### ```rbtree = RedBlackTreeSet(a: Iterable[T]=[])```
aからRedBlackTreeSetを構築します。重複無くソート済みならO(N)、そうでないならO(NlogN)です。

### ```rbtree.add(key: T) -> bool```
keyが存在しないならkeyを追加し、Trueを返します。keyが存在するなら何も追加せず、Falseを返します。

### ```rbtree.discard_iter(node: Node) -> None```
nodeを削除します。償却O(1)らしいです。

### ```rbtree.discard(key: T) -> bool```
keyが存在するならkeyを削除し、Trueを返します。keyが存在しないなら何もせず、Falseを返します。O(logN)です。

### ```rbtree.couont(key: T) -> int```
keyが存在するなら1を、存在しないなら0を返します。O(logN)です。

### ```key in rbtree / key not in rbtree```
存在判定です。keyが存在すればTrueを、そうでなければFalseを返します。O(logN)です。

### ```rbtree.get_max() -> Optional[T]```
最大値を返します。空であればNoneを返します。O(1)です。

### ```rbtree.get_min() -> Optional[T]```
最小値を返します。空であればNoneを返します。O(1)です。

### ```rbtree.get_max_iter() -> Optional[Node]```
最大値を指すNodeを返します。空であればNoneを返します。O(1)です。

### ```rbtree.get_min_iter() -> Optional[Node]```
最小値を指すNodeを返します。空であればNoneを返します。O(1)です。

### ```rbtree.le(key) / .lt(key) / .ge(key) / gt(key)```
key(以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)の値を返します。存在しなければNoneを返します。O(logN)です。

### ```rbtree.le_iter(key) / .lt_iter(key) / .ge_iter(key) / gt_iter(key)```
key(以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)のNodeを返します。存在しなければNoneを返します。O(logN)です。

### ```rbtree.find(key) -> Optional[Node]```
keyが存在すれば、keyを指すNodeを返します。存在しなければNoneを返します。O(logN)です。

### ```rbtree.tolist() -> List[T]```
keyを昇順に並べたリストを返します。O(N)です。

### ```rbtree.pop_max() -> T```
最大値のノードを削除し、その値を返します。O(logN)です。空のrbtreeに使ってはいけません。

### ```rbtree.pop_min() -> T```
最小値のノードを削除し、その値を返します。O(logN)です。空のrbtreeに使ってはいけません。

### ```rbtree.clear() -> None```
clearします。O(1)です。

### ```str(rbtree) / repr(rbtree)```

### ```len(rbtree) / bool(rbtree)```

### ```iter(rbtree) / next(rbtree)```

_____
# [RedBlackTreeMultiset](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/RedBlackTree/RedBlackTreeMultiset.py)
多重集合としての赤黒木です。

### ```rbtree.add(key: T, cnt: int=1) -> None```
keyをcnt個追加ます。

### ```rbtree.discard(key: T, cnt: int=1) -> bool```
keyをmin(cnt, rbtree.count(key))個削除します。

