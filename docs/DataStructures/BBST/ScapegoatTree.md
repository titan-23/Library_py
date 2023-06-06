____

# [`ScapegoatTree`](https://github.com/titanium-22/Library_py/tree/main/DataStructures/BBST/ScapegoatTree)

最終更新：2023/5/25

- 子が `None` にならないことで無限ループが発生する事象を解消しました。

`ScapegoatTree` です。ノードを追加したとき、「大きく偏る」部分木があれば、その部分木をO(部分木のサイズ)時間かけてならします。これにより、回転動作(=軽いが多くの処理をする)がなくなり、嬉しいことがあるかもしれません。  
以下、計算量を明示していないものは計算量 `O(logN)` とします( `N` はそのときどきのサイズではないですが、些細な問題です(?))。

_____

# [`ScapegoatTreeSet.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/ScapegoatTree/ScapegoatTreeSet.pyy)

集合としての `ScapegoatTree` です。全順序集合が乗ります。  
全機能を $verify$ したわけではないのでコンテスト中の利用は控えると吉です。

### `st = ScapegoatTree(a: Iterable[T]=[])`
- `a` から `ScapegoatTree` を作ります。 `O(NlogN)` 時間です。ソート済みを仮定して内部をいじると `O(N)` 時間です。

### `len(st)`
- 要素の総数を返します。 `O(1)` 時間です。

### `x in st`
- 存在判定です。

### `st[k] -> T`
- `k` 番目に小さい値 (0-indexed) を返します。負の添え字に対応しています。

### `bool(st) / str(st) / reversed(st)`
- よしなに動きます。

### `st.add(key) -> bool`
- `key` がなければ `key` を追加し `True` を返します。 `key` があれば追加せずに `False` を返します。償却計算量O(logN)です。

### `st.discard(x) -> bool`
- xがあれば削除し `True` を返します。xがなければ何も削除せずに `False` を返します。

### `st.le(x) / .lt(x) / .ge(x) / gt(x) -> Union[T, None]`
- `x` (以下の / より小さい / 以上の / より大きい)値で(最大 / 最大 / 最小 / 最小)の値を返します。存在しなければ `None` を返します。

### `st.index(x) / .index_right(x) -> int`
- `x` (より小さい / 以下の)要素の数を返します。

### `st.pop(k=-1) / .popleft() -> T`
- `k` 番目の要素を削除し、その値を返します。

### `st.clear() -> None`
- `st` を工場出荷状態に戻します。 `O(1)` です。

### `st.tolist() -> List[T]`
- リストに変換します。 `O(N)` です。

_____

# [`ScapegoatTreeMultiSet.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/ScapegoatTree/ScapegoatTreeMultiset.py)

多重集合としての `ScapegoatTree` です。[`ScapegoatTreeSet`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/BBST/ScapegoatTree/ScapegoatTreeSet.py)でできる操作に加えて以下の操作がができます。  

### `st.add(key, val) -> None`
- `key` を `val` 個追加します。償却計算量 `O(logN)` です。

### `st.discard(key, val) -> bool`
- `key` を `val` 個削除します。 `val` が `key` の数より大きいときは `key` を全て削除します。  
`key` が無いとき `False` を、そうでないとき `True` を返します。

### `st.discard_all(key) -> None`
- `key` を全て削除します。 `st.discard(key, st.count(key))` と等価です。

### `st.count(key) -> int`
- `st` に含まれる `key` の数を返します。

### `st.tolist_items() -> List[Tulpe[T, int]]`
- stをリストに変換します。各要素は `(key, st.count(key))` です。

### `st.get_elm(k) -> T`
- `st` の重複を除いたときの、小さい方から `k` 番目の `key` を返します。

### `st.len_elm() -> int`
- `st` の要素の種類数を返します。

### `st.show() -> None`
- よしなに `print` します。
