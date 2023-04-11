最終更新：2023/02/23  

- 色々更新しました  

_____
# [SegmentTree](https://github.com/titanium-22/Library/blob/main/DataStructures/SegmentTree/SegmentTree.py)
SegmentTreeです。  
ACLのsegtreeを大々的に参考にしてます。  
非再帰です。

```seg = SegmentTree(n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T], e: T)```  
第1引数n_or_aがn: intのとき、eを初期値として長さnのSegmentTreeを構築します。  
第1引数n_or_aがa: Iterable[T]のとき、aからSegmentTreeを構築します。  
いずれもO(N)です。

```seg.set(k: int, val: T) -> None / seg[k] = val```  
列k番目の値をvalに更新します。O(logN)です。

```seg.get(k: int) -> T / seg[k]```  
列k番目の値を返します。O(logN)です。

```seg.prod(l: int, r: int) -> T```  
区間[l, r)の総積を返します。O(logN)です。

```seg.all_prod() -> T```  
区間[l, N)の総積を返します。O(1)です。

```seg.max_right(l: int, f: Callable[[T], bool]) -> int```  
Find the largest index R s.t. f([l, R)) == True. / O(logN)

```seg.min_left(r: int, f: Callable[[T], bool]) -> int```  
Find the smallest index L s.t. f([L, r)) == True. / O(logN)
