最終更新：2023/02/25  
・いろいろ更新しました。

※計算量を明示していないものはすべて最悪O(logN)の計算量です。

_____
# Node
Nodeです。

### node += 1 / node -= 1
nodeを次/前のnodeにします。存在しないときはNoneを返します。

### node + 1 / node - 1
次/前のnodeを返します。存在しないときはNoneを返します。


_____
# [RedBlackTreeSet](https://github.com/titanium-22/Library/blob/main/DataStructures/BST/RedBlackTree/RedBlackTreeSet.py)
集合としての赤黒木です。以下の操作ができます:  
Add/Delete/Predecessor/Successor/  
詳しくは下記です。

### ```rbtree = RedBlackTreeSet(a: Iterable[T]=[])```
aからRedBlackTreeSetを構築します。重複無くソート済みならO(N)、そうでないならO(NlogN)です。

### ```rbtree.add(key: T) -> bool```
keyが存在しないならkeyを追加し、Trueを返します。keyが存在するなら何も追加せず、Falseを返します。

### ```rbtree.discard_iter(node: Node) -> None```
nodeを削除します。

### ```rbtree.discard(key: T) -> bool```
keyが存在するならkeyを削除し、Trueを返します。keyが存在しないなら何もせず、Falseを返します。

### ```rbtree.couont(key: T) -> int```
keyが存在するなら1を、存在しないなら0を返します。

### ```key in rbtree / key not in rbtree```
存在判定です。keyが存在すればTrueを、そうでなければFalseを返します。

### ```rbtree.get_max() -> T```
最大値を返します。空のrbtreeに使ってはいけません。

### ```rbtree.get_min() -> T```
最小値を返します。空のrbtreeに使ってはいけません。

### ```rbtree.get_max_iter() -> Optional[Node]```
最大値を指すNodeを返します。

### ```rbtree.get_min_iter() -> Optional[Node]```
最小値を指すNodeを返します。

### ```rbtree.le(key) / .lt(key) / .ge(key) / gt(key)```
key(以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)の値を返します。存在しなければNoneを返します。

### ```rbtree.le_iter(key) / .lt_iter(key) / .ge_iter(key) / gt_iter(key)```
key(以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)のNodeを返します。存在しなければNoneを返します。

### ```rbtree.find(key) -> Optional[Node]```
keyが存在すれば、keyを指すNodeを返します。存在しなければNoneを返します。

### ```rbtree.tolist() -> List[T]```
keyを昇順に並べたリストを返します。O(N)です。

### ```rbtree.pop_max() -> T```
最大値のノードを削除し、その値を返します。空のrbtreeに使ってはいけません。

### ```rbtree.pop_min() -> T```
最小値のノードを削除し、その値を返します。空のrbtreeに使ってはいけません。

### ```rbtree.clear() -> None```
clearします。O(1)です。

### ```str(rbtree) / repr(rbtree)```

### ```len(rbtree) / bool(rbtree)```

### ```iter(rbtree) / next(rbtree)```

_____
# [AVLTreeMultiSet](https://github.com/titanium-22/Library/blob/main/DataStructures/BST/RedBlackTree/RedBlackTreeMultiset.py)
多重集合としての赤黒木です。

### ```rbtree.add(key: T, cnt: int=1) -> None```
keyが存在しないならkeyを追加し、Trueを返します。keyが存在するなら何も追加せず、Falseを返します。

### ```rbtree.discard(key: T, cnt=1) -> bool```
keyをmin(cnt, rbtree.count(key))個削除します。

