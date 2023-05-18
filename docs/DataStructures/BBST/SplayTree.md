最終更新：2023/5/3
- READMEを修正しました。


# `SplayTree`
splay操作をする木です。強いです。  

_____

# [`LazySplayTree`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/SplayTree/LazySplayTree.py)
遅延伝播反転可能平衡二分木です。アホの定数倍をしています(定数倍が大きい方向にアホです)。

## `LazySplayTreeData`
モノイドのデータや作用、左右の子などを保持するクラスです。 `LazySplayTree` をインスタンス化する際に渡してください。  
`merge/split` する場合はそれらが同一の `LazySplayTreeData` を持つ必要があります。

## `LazySplayTree`
親へのポインタ持たせて～～

### `lazy_splay_tree = LazySplayTree(data: LazySplayTreeData, n_or_a: Union[int, Iterable[T]]=0)`
`data` から `LazySplayTree` を構築します。 `O(N)` です。
`n_or_a` が `int` のとき、`data` の `e` から長さ `n` の `lazy_splay_tree` が作られます。  
`n_or_a` が `Iterable` のとき、`a` から `lazy_splay_tree` が作られます。  
以降、 `st = lazy_splay_tree` と書きます。

### `st.merge(other: LazySplayTree) -> None`
`st` に `other` を `merge` します。 `list` における `.extend(other)` と似たような処理です。

### `st.split(k: int) -> Tuple[LazySplayTree, LazySplayTree]`
2つの `LazySplayTree` を要素に持つタプルを返します。  
1要素目は `st` の `0` 番目から `k-1` 番目までを、2要素目は `k` 番目以降を要素に持ちます。

### `st.insert(k: int, key: T) -> None`
位置 `k` に `key` を挿入します。償却 `O(logN)` です。

### `st.append(key: T) / .appendleft(key: T) -> None`
末尾/先頭 に `key` を追加します。償却 `O(logN)` です。

### `st.pop(k: int=-1) / .popleft() -> T`
`k` 番目/末尾/先頭 を削除しその値を返します。償却 `O(logN)` です。

### `st[k] -> T`
`k` 番目を返します。償却 `O(logN)` です。

### `st[k] = key: T`
`k` 番目を `key` に更新します。償却 `O(logN)` です。

### `st.copy() -> LazySplayTree`
`copy` できます。 `O(N)` です。

### `st.prod(l: int, r: int) -> T`
区間 `[l, r)` に `op` を適用した結果を返します。償却 `O(logN)` です。

### `st.reverse(l: int, r: int) -> None`
区間 `[l, r)` を反転します。償却 `O(logN)` です。 `reverse()` メソッドを一度でも使用するなら `op` には可換性が求められます(可換性がない場合、嘘の動作をします)。

### `st.apply(l: int, r: int, f: F) -> None`
区間 `[l, r)` に作用 `f` を適用します。償却 `O(logN)` です。

### `st.all_apply(f: F) -> None`
区間 `[0, N)` に作用 `f` を適用します。 `O(1)` です。

### `st.tolist() -> List[T]`
`List` に変換します。非再帰です。`O(N)` です。

### `iter(st) / next(st) / len(st) / str(st) / repr(st)`

<!--
_____

# [`SplayTreeSet`](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeSet.py)
集合としてのSplayTreeです。任意の他要素と比較可能な要素が載ります。  
全機能をverifyしたわけではないのでコンテスト中の利用は控えると吉です。

### `st = SplayTreeSet(a: Iterable[T]])`
`a` から `SplayTreeSet` を作ります。 `O(NlogN)` 時間です。ソート済みを仮定して内部をいじると `O(N)` 時間です。

### `len(st)`
要素の個数を返します。O(1)時間です。

### `x in st / x not in st`
存在判定です。

### `st[k] -> T`
k番目に小さい値(0-indexed)を返します。負の添え字に対応しています。

### `bool(st) / str(st) / reversed(st)`
よしなに動きます。

### `st.add(x) -> bool`
xがなければxを追加しTrueを返します。xがあれば追加せずにFalseを返します。

### `st.discard(x) -> bool`
xがあれば削除しTrueを返します。xがなければ何も削除せずにFalseを返します。

### `st.le(x) / .lt(x) / .ge(x) / gt(x) -> Union[T, None]`
x(以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)の値を返します。存在しなければNoneを返します。

### `st.index(x) / .index_right(x) -> int`
x(より小さい/以下の)要素の数を返します。

### `st.pop(k=-1) / .popleft() -> T`
k番目の要素を削除し、その値を返します。

### `st.clear() -> None`
stを工場出荷状態に戻します。O(1)です。

### `st.tolist() -> List[T]`
リストに変換します。内部でsys.setrecursionlimit(len(self))をしているので安心です。O(N)です。

_____
# [`SplayTreeMultiSet`](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeMultiSet.py)
多重集合としてのSplayTreeです。[SplayTreeSet](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeSet.py)でできる操作に加えて以下の操作がができます。  

### `st.add(key, val) -> None`
keyをval個追加します。

### `st.discard(key, val) -> bool`
keyをval個削除します。valがkeyの数より大きいときは、keyを全て削除します。  
keyが無いときFalseを、そうでないときTrueを返します。

### `st.discard_all(key) -> None`
keyを全て削除します。st.discard(key, st.count(key))と等価です。

### `st.count(key) -> int`
stに含まれるkeyの数を返します。

### `st.index_keys(x) / .index_right_keys(x) -> int`
x(より小さい/以下の)要素の種類数を返します。

### `st.tolist_items() -> List[Tulpe[T, int]]`
stをリストに変換します。各要素は(key, st.count(key))です。

### `st.get_elm(k) -> T`
stの重複を除いたときの、小さい方からk番目のkeyを返します。

### `st.len_elm() -> int`
stの要素の種類数を返します。

### `st.show() -> None`
よしなにprintします。

-->
