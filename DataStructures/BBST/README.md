最終更新: 2023/04/19  
- なんかいろいろ更新

計算量は償却だったり最悪だったりします。詳しくは各READMEを読んでください。  
以下の木があります。  
- [AVLTree](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BBST/AVLTree)
- [ScapegoatTree](https://github.kcom/titanium-22/Library_py/tree/main/DataStructures/BBST/ScapegoatTree)
- [SplayTree](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BBST/SplayTree)
- [Treap](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BBST/Treap)
- [RedBlackTree](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BBST/RedBlackTree)

_____
# 列を扱うBinaryTree #

列を扱えます。

### ```bt.merge(other)```
`bt` に `other` をマージします。 `merge` した後に `other` を使うとマズイです。 `O(logN)` です。

### ```bt.split(k)```
`bt` を `k` で `split` します。`O(logN)`です。

### ```bt.prod(l, r)```
区間 `[l, r)`の総積を取得します。 `l >= r` のとき `e` を返します。 `O(logN)` です。

### ```bt.all_prod()```
区間 `[0, n)` の総積を取得します。 `O(1)` です。

### ```bt.insert(k, key)```
`k` 番目に `key` を挿入します。 `O(logN)` です。

### ```bt.append(key) / appendleft(key)```
先頭/末尾に `key` を追加します。 `O(logN)` です。

### ```bt.pop(k=-1) / .popleft()```
末尾( `k` 番目)/先頭の値を削除し、その値を返します。 `O(logN)` です。

### ```bt[k]```
`k` 番目の値を返します。 `O(logN)` です。

### ```bt[k] = key```
`k` 番目の値を `key` に更新します。 `O(logN)` です。

### ```bt.copy() -> None```
copyします。 `O(N)` です。

### ```bt.clear() -> None```
clearします。 `O(1)` です。

### ```bt.tolist() -> List[T]```
`key` からなるリストを返します。 `O(N)` です。

# 遅延評価できる木
列を扱う `BinaryTree` に加えて以下の操作ができます。

### ```bt.reverse(l, r)```
区間 `[l, r)` を反転します。 `reverse` メソッドを使うなら、`op` には可換性が求められます。 `O(logN)` です。

### ```bt.apply(l, r, f)```
区間 `[l, r)` に `f` を適用します。 `O(logN)`です。

### ```bt.all_apply(f)```
区間 `[0, n)` に `f` を適用します。 `O(1)`です。

_____
# 集合としてのBinarySearchTree

### ```x in bst / x not in bst```
存在判定です。` O(logN)` です。

### ```bst[k]```
昇順k番目の値を返します。` O(logN)` です。

### ```bst.add(key)```
`key` が存在しないなら `key` を追加し、 `True` を返します。 `key` が存在するなら何も追加せず、 `False` を返します。` O(logN)` です。

### ```bst.discard(key)```
`key` が存在するなら `key` を削除し、 `True` を返します。 `key` が存在しないなら何もせず、 `False` を返します。` O(logN)` です。

### ```bst.le(key) / .lt(key) / .ge(key) / gt(key)```
`key` (以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)の値を返します。存在しなければNoneを返します。` O(logN)` です。

### ```bst.index(key) / .index_right(key)```
key(より小さい/以下の)要素の数を返します。` O(logN)` です。

### ```bst.pop(k=-1) / .popleft()```
(最大(昇順k番目)/最小)の値を削除し、その値を返します。` O(logN)` です。

### ```bst.clear()```
clearします。O(1)です。` O(logN)` です。

### ```bst.tolist()```
keyを昇順に並べたリストを返します。O(N)です。

# 多重集合

Setに加えて、以下の操作ができます。  
valの値に関わらず、` O(logN)` で動作します。

### ```bst.add(key, val=1)```
val個のkeyを追加します。` O(logN)` です。

### ```bst.discard(key, val=1)```
`key` を `val` 個削除します。 `val` が `key` の数より大きいときは、 `key` を全て削除します。  
`key` が無いとき `False` を、そうでないときTrueを返します。` O(logN)` です。

### ```bst.dicard_all(key)```
`key` を全て削除します。` O(logN)` です。

### ```bst.count(key)```
含まれる `key` の数を返します。` O(logN)` です。

### ```bst.index_keys(key) / index_right_keys(key)```
`key` (より小さい/以下の)要素の種類数を返します。` O(logN)` です。

### ```bst.tolist_items()```
`key` で昇順に並べたリストを返します。各要素は `(key, st.count(key))` です。 `O(N)` です。

### ```bst.keys() / values() / items()```
よしなに動きます。

### ```bst.get_elm(k)```
要素の重複を除いたときの、昇順 `k` 番目の `key` を返します。` O(logN)` です。

### ```bst.len_elm()```
stの要素の種類数を返します。 `O(1)` です。

### ```bst.show()```
よしなにprintします。 `O(N)` です。
