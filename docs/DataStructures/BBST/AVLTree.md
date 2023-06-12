_____

# [AVLTree](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BBST/AVLTree)

最終更新：2022/5/26

- いろいろ更新しました。

AVL木です。

_____

## [`AVLTreeSet.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/AVLTree/AVLTreeSet.py)

集合としてのAVL木です。 

## [`AVLTreeSet2.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/AVLTree/AVLTreeSet2.py)
集合としてのAVL木です。  
各 `Node` は `key/左の子/右の子` のみをもち、 `Node` を頂点とする部分木の大きさは持ちません。[`AVLTreeSet`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/AVLTree/AVLTreeSet.py)の機能を落として高速化を図った形です。違いは以下の通りです。

#### `avl = AVLTreeSet2(a: Iterable[T]=[])`
- `a` から `AVLTreeSet` を構築します。ソートがボトルネックとなり、計算量 `O(NlogN)` です。ソート済みを仮定して内部をいじると `O(N)` です。

#### `avl[k] -> T`
- `k` に指定できるものは、 `0/-1/len(avl)-1` のいずれかです。

#### `avl.get_min() / .get_max() -> T`
- (最小 / 最大)の値を返します。

#### `avl.pop() / .popleft() -> T`
- (最大 / 最小)の値を削除し、その値を返します。 `pop` で引数が指定できなくなりました。

_____

## [`AVLTreeMultiSet.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/AVLTree/AVLTreeMultiset.py)
多重集合としての `AVL` 木です。

_____

## [`LazyAVLTree.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/AVLTree/LazyAVLTree.py)

遅延伝播反転可能平衡二分木です。

