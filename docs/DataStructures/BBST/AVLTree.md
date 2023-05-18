_____

# [AVLTree](https://github.com/titanium-22/Library/blob/main/BST/AVLTree)

最終更新：2022/12/03

- いろいろ更新しました。

_____

# [AVLTreeSet.py](https://github.com/titanium-22/Library/blob/main/BST/AVLTree/AVLTreeSet.py)
集合としてのAVL木です。

### `avl = AVLTreeSet(a: Iterable[T]=[])`
`a` から `AVLTreeSet` を構築します。ソートがボトルネックとなり、計算量 `O(NlogN)` です。ソート済みを仮定して内部をいじると `O(N)` です。

### `avl.add(key: T)`
`key` が存在しないなら `key` を追加し、 `True` を返します。 `key` が存在するなら何も追加せず、 `False` を返します。

### `avl.discard(key)`
`key` が存在するなら `key` を削除し、 `True` を返します。 `key` が存在しないなら何もせず、 `False` を返します。

### `key in avl / key not in avl`
存在判定です。 `key` が存在すれば `True` を、そうでなければ `False` を返します。

### `avl[k]`
昇順k番目の値を返します。

### `avl.le(key) / .lt(key) / .ge(key) / gt(key)`
`key` (以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)の値を返します。存在しなければ `None` を返します。

### `avl.index(key) / .index_right(key)`
`key` (より小さい/以下の)要素の数を返します。

### `avl.pop(k=-1) / .popleft()`
(最大(昇順 `k` 番目)/最小)の値を削除し、その値を返します。

### `avl.clear()`
`clear` します。 `O(1)` です。

### `avl.tolist()`
`key` を昇順に並べたリストを返します。 `O(N)` です。

# [AVLTreeSet2.py](https://github.com/titanium-22/Library/blob/main/BST/AVLTree/AVLTreeSet2.py)
集合としてのAVL木です。  
各 `Node` は `key/左の子/右の子` のみをもち、 `Node` を頂点とする部分木の大きさは持ちません。[AVLTreeSet](https://github.com/titanium-22/Library/blob/main/BST/AVLTree/AVLTreeSet.py)の機能を落として高速化を図った形です。違いは以下の通りです。

### `avl = AVLTreeSet2(a: Iterable[T]=[])`
`a` から `AVLTreeSet` を構築します。ソートがボトルネックとなり、計算量 `O(NlogN)` です。ソート済みを仮定して内部をいじると `O(N)` です。

### `avl[k]`
`k` に指定できるものは、 `0/-1/len(avl)-1` のいずれかです。

### `avl.get_min() / .get_max()`
(最小/最大)の値を返します。

### `avl.pop() / .popleft()`
(最大/最小)の値を削除し、その値を返します。  
`pop` で引数が指定できなくなりました。

_____

# [AVLTreeMultiSet.py](https://github.com/titanium-22/Library/blob/main/BST/AVLTree/AVLTreeMultiSet.py)
多重集合としての `AVL` 木です。

_____

# [LazyAVLTree.py](https://github.com/titanium-22/Library/blob/main/BST/AVLTree/LazyAVLTree.py)

遅延伝播反転可能平衡二分木です。アホの定数倍をしています(定数倍が大きい方向にアホです)。  

### `avl = LazyAVLTree(a, op, mapping, composition, e)`
列 `a` から `LazyAVLTree` を構築します。その他引数は遅延セグ木のアレです。時間計算量 `O(N)` です。  
`op, mapping, composition, e` は省略可能です。特に `e` は `prod(l, r)` で `l=r` のとき使用されます。

### `avl.merge(other)`
stにotherをmergeできます。

### `avl.split(k)`
`x, y = avl.split(k)` で、`k` 番目で左右に分けた `AVLTree` をつくり `x, y` に代入できます。 `avl` は破壊されます。( `x` の長さが `k` 。)

### `avl.insert(k, key)`
`k` に `key` を `insesrt` できます。

### `avl.pop(k)`
`k` 番目を削除しその値を返します。

### `avl[k]`
`k` 番目を取得できます。

### `avl.prod(l, r)`
区間 `[l, r)` に `op` を適用した結果を返します。

### `avl.reverse(l, r)`
区間 `[l, r)` を反転します。 `reverse()` メソッドを一度でも使用するなら `op` には可換性が求められます(可換性がない場合、嘘の動作をします)。

### `avl.apply(l, r, f)`
区間 `[l, r)` に `f` を適用します。

### `avl.tolist()`
`Node` の `key` からなるリストを返します。計算量 `O(N)` です。

