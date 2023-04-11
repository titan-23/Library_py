最終更新：2022/12/12  
・子がNoneにならないことで無限ループが発生する事象を解消しました。

# ScapegoatTree
ScapegoatTreeです。  
ノードを追加したとき、「大きく偏る」部分木があれば、その部分木をO(部分木のサイズ)時間かけてならします。これにより、回転動作(=軽いが多くの処理をする)がなくなり、嬉しいことがあるかもしれません。  
以下、計算量を明示していないものは計算量O(logN)とします(Nはそのときどきのサイズではないですが、些細な問題です(?))。

_____
# [ScapegoatTreeSet](https://github.com/titanium-22/Library/blob/main/BST/ScapegoatTree/ScapegoatTreeSet.py)
集合としてのScapegoatTreeです。任意の他要素と比較可能な要素が載ります。  
全機能をverifyしたわけではないのでコンテスト中の利用は控えると吉です。

### ```st = ScapegoatTree(a: Iterable[T]])```
aからScapegoatTreeを作ります。O(NlogN)時間です。ソート済みを仮定して内部をいじるとO(N)時間です。

### ```len(st)```
要素の個数を返します。O(1)時間です。

### ```x in st / x not in st```
存在判定です。

### ```st[k] -> T```
k番目に小さい値(0-indexed)を返します。負の添え字に対応しています。

### ```bool(st) / str(st) / reversed(st)```
よしなに動きます。

### ```st.add(x) -> bool```
xがなければxを追加しTrueを返します。xがあれば追加せずにFalseを返します。償却計算量O(logN)です。

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
# [ScapegoatTreeMultiSet](https://github.com/titanium-22/Library/blob/main/BST/ScapegoatTree/ScapegoatTreeMultiSet.py)
多重集合としてのScapegoatTreeです。[ScapegoatTreeSet](https://github.com/titanium-22/Library/blob/main/BST/ScapegoatTree/ScapegoatTreeSet.py)でできる操作に加えて以下の操作がができます。  

### ```st.add(key, val) -> None```
keyをval個追加します。償却計算量O(logN)です。

### ```st.discard(key, val) -> bool```
keyをval個削除します。valがkeyの数より大きいときは、keyを全て削除します。  
keyが無いときFalseを、そうでないときTrueを返します。

### ```st.discard_all(key) -> None```
keyを全て削除します。st.discard(key, st.count(key))と等価です。

### ```st.count(key) -> int```
stに含まれるkeyの数を返します。

### ```st.to_l_items() -> List[Tulpe[T, int]]```
stをリストに変換します。各要素は(key, st.count(key))です。

### ```st.get_elm(k) -> T```
stの重複を除いたときの、小さい方からk番目のkeyを返します。

### ```st.len_elm() -> int```
stの要素の種類数を返します。

### ```st.show() -> None```
よしなにprintします。
