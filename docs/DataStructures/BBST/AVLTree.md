_____

# [AVLTree](https://github.com/titanium-22/Library/blob/main/BST/AVLTree)

最終更新：2022/12/03  

- いろいろ更新しました。

※計算量を明示していないものはすべてO(logN)の計算量です。

_____

# [AVLTreeSet.py](https://github.com/titanium-22/Library/blob/main/BST/AVLTree/AVLTreeSet.py)
集合としてのAVL木です。

### ```avl = AVLTreeSet(a: Iterable[T]=[])```
aからAVLTreeSetを構築します。ソートがボトルネックとなり、計算量O(NlogN)です。ソート済みを仮定して内部をいじるとO(N)です。

### ```avl.add(key: T)```
keyが存在しないならkeyを追加し、Trueを返します。keyが存在するなら何も追加せず、Falseを返します。

### ```avl.discard(key)```
keyが存在するならkeyを削除し、Trueを返します。keyが存在しないなら何もせず、Falseを返します。

### ```key in avl / key not in avl```
存在判定です。keyが存在すればTrueを、そうでなければFalseを返します。

### ```avl[k]```
昇順k番目の値を返します。

### ```avl.le(key) / .lt(key) / .ge(key) / gt(key)```
key(以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)の値を返します。存在しなければNoneを返します。

### ```avl.index(key) / .index_right(key)```
key(より小さい/以下の)要素の数を返します。

### ```avl.pop(k=-1) / .popleft()```
(最大(昇順k番目)/最小)の値を削除し、その値を返します。

### ```avl.clear()```
clearします。O(1)です。

### ```avl.to_l()```
keyを昇順に並べたリストを返します。O(N)です。

# [AVLTreeSet2.py](https://github.com/titanium-22/Library/blob/main/BST/AVLTree/AVLTreeSet2.py)
集合としてのAVL木です。  
各Nodeはkey/左の子/右の子のみをもち、Nodeを頂点とする部分木の大きさは持ちません。[AVLTreeSet](https://github.com/titanium-22/Library/blob/main/BST/AVLTree/AVLTreeSet.py)の機能を落として高速化を図った形です。違いは以下の通りです。

### ```avl = AVLTreeSet2(a: Iterable[T]=[])```
aからAVLTreeSetを構築します。ソートがボトルネックとなり、計算量O(NlogN)です。ソート済みを仮定して内部をいじるとO(N)です。

### ```avl[k]```
kに指定できるものは、0/-1/len(avl)-1のいずれかです。

### ```avl.get_min() / .get_max()```
(最小/最大)の値を返します。

### ```avl.pop() / .popleft()```
(最大/最小)の値を削除し、その値を返します。  
popで引数が指定できなくなりました。



_____
# [AVLTreeMultiSet.py](https://github.com/titanium-22/Library/blob/main/BST/AVLTree/AVLTreeMultiSet.py)
多重集合としてのAVL木です。


_____
# [LazyAVLTree.py](https://github.com/titanium-22/Library/blob/main/BST/AVLTree/LazyAVLTree.py)
遅延伝播反転可能平衡二分木です。アホの定数倍をしています(定数倍が大きい方向にアホです)。  
※恒等写像はいりません(内部で恒等写像をNoneとして場合分けしています)。

### ```avl = LazyAVLTree(a, op, mapping, composition, e)```
列aからLazyAVLTreeを構築します。その他引数は遅延セグ木のアレです。時間計算量O(N)です。  
op, mapping, composition, eは省略可能です。特にeはprod(l, r)でl=rのとき使用されます。

### ```avl.merge(other)```
stにotherをmergeできます。

### ```avl.split(indx)```
x, y = avl.split(indx)で、indx番目で左右に分けたAVLTreeをつくりx, yに代入できます。avlは破壊されます。(xの長さがindx。)

### ```avl.insert(indx, key)```
indxにkeyをinsesrtできます。

### ```avl.pop(indx)```
indx番目を削除しその値を返します。

### ```avl[indx]```
indx番目を取得できます。

### ```avl.prod(l, r)```
区間[l, r)にopを適用した結果を返します。

### ```avl.reverse(l, r)```
区間[l, r)を反転します。reverse()メソッドを一度でも使用するならopには可換性が求められます(可換性がない場合、嘘の動作をします)。

### ```avl.apply(l, r, f)```
区間[l, r)にfを適用します。

### ```avl.to_l()```
Nodeのkeyからなるリストを返します。計算量はO(N)です。

