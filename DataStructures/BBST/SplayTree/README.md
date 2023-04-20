最終更新：2022/12/01

・色々修正しました。


# SplayTree
splay操作をする木です。強いです。  
計算量を明示していないものは、償却計算量O(logN)です。
_____
# [LazySplayTree](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/SplayTree/LazySplayTree.py)
遅延伝播反転可能平衡二分木です。アホの定数倍をしています(定数倍が大きい方向にアホです)。

## MonoidData
モノイドのデータや作用、左右の子などを保持するクラスです。 `LazySplayTree` をインスタンス化する際に渡してください。

## LazySplayTree

### ```splay = LazySplayTree(monoiddata: MonoidData, n_or_a: Union[int, Iterable[T]]=0)```
列 `a` 、 データ `monoiddata` から `LazySplayTree` を構築します。単位元eは、prodでl >= rのときのみ使用されるため、そのようなl, rを要求しないのであれば必要ありません。  
また、opも二項演算を必要としない場合は省略可能です。  
O(N)です。

### ```st.merge(other: SplayTree) -> None```
stにotherをmergeできます。

### ```st.split(k: int) -> Tuple[SplayTree, SplayTree]```
x, y = st.split(k)で、k番目で左右に分けたSplayTreeを返します。(xの長さがk。)

### ```st.insert(k: int, key: T) -> None```
kにkeyをinsesrtできます。

### ```st.append(key: T) / .appendleft(key: T) -> None```
末尾/先頭にkeyを追加します。

### ```st.pop(k: int=-1) / .popleft() -> T```
k番目/先頭を削除しその値を返します。

### ```st[k: int] -> T```
k番目を取得できます。

### ```st[k: int] = key```
setitemできます。

### ```st.copy() -> SplayTree```
copyできます。O(N)です。

### ```st.prod(l: int, r: int) -> T```
区間[l, r)にopを適用した結果を返します。l >= rのとき、単位元eを返します。

### ```st.to_l() -> List[T]```
リストに変換します。内部でsys.setrecursionlimit(len(self))をしているので安心です。O(N)です。

列aからLazySplayTreeを構築します。その他引数は遅延セグ木のアレです。時間計算量O(N)です。

### ```st.reverse(l: int, r: int) -> None```
区間[l, r)を反転します。reverse()メソッドを一度でも使用するならopには可換性が求められます(可換性がない場合、嘘の動作をします)。

### ```st.apply(l: int, r: int, f: F) -> None```
区間[l, r)にfを適用します。

### ```st.all_apply(f: F) -> None```
区間[0, N)にfを適用します。時間計算量O(1)です。


_____
# [SplayTreeSet](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeSet.py)
集合としてのSplayTreeです。任意の他要素と比較可能な要素が載ります。  
全機能をverifyしたわけではないのでコンテスト中の利用は控えると吉です。

### ```st = SplayTreeSet(a: Iterable[T]])```
aからSplayTreeSetを作ります。O(NlogN)時間です。ソート済みを仮定して内部をいじるとO(N)時間です。

### ```len(st)```
要素の個数を返します。O(1)時間です。

### ```x in st / x not in st```
存在判定です。

### ```st[k] -> T```
k番目に小さい値(0-indexed)を返します。負の添え字に対応しています。

### ```bool(st) / str(st) / reversed(st)```
よしなに動きます。

### ```st.add(x) -> bool```
xがなければxを追加しTrueを返します。xがあれば追加せずにFalseを返します。

### ```st.discard(x) -> bool```
xがあれば削除しTrueを返します。xがなければ何も削除せずにFalseを返します。

### ```st.le(x) / .lt(x) / .ge(x) / gt(x) -> Union[T, None]```
x(以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)の値を返します。存在しなければNoneを返します。

### ```st.index(x) / .index_right(x) -> int```
x(より小さい/以下の)要素の数を返します。

### ```st.pop(k=-1) / .popleft() -> T```
k番目の要素を削除し、その値を返します。

### ```st.clear() -> None```
stを工場出荷状態に戻します。O(1)です。

### ```st.to_l() -> List[T]```
リストに変換します。内部でsys.setrecursionlimit(len(self))をしているので安心です。O(N)です。

_____
# [SplayTreeMultiSet](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeMultiSet.py)
多重集合としてのSplayTreeです。[SplayTreeSet](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeSet.py)でできる操作に加えて以下の操作がができます。  

### ```st.add(key, val) -> None```
keyをval個追加します。

### ```st.discard(key, val) -> bool```
keyをval個削除します。valがkeyの数より大きいときは、keyを全て削除します。  
keyが無いときFalseを、そうでないときTrueを返します。

### ```st.discard_all(key) -> None```
keyを全て削除します。st.discard(key, st.count(key))と等価です。

### ```st.count(key) -> int```
stに含まれるkeyの数を返します。

### ```st.index_keys(x) / .index_right_keys(x) -> int```
x(より小さい/以下の)要素の種類数を返します。

### ```st.to_l_items() -> List[Tulpe[T, int]]```
stをリストに変換します。各要素は(key, st.count(key))です。

### ```st.get_elm(k) -> T```
stの重複を除いたときの、小さい方からk番目のkeyを返します。

### ```st.len_elm() -> int```
stの要素の種類数を返します。

### ```st.show() -> None```
よしなにprintします。
