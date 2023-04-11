最終更新
- uniteの戻り値をNoneからintに変更しました

更新：2022/12/04  
- WeightedUnionFindをアップロードしました。

_____
# [UnionFind](https://github.com/titanium-22/Library/blob/main/UnionFind/UnionFind.py)
UnionFindです。素集合データ構造です。 
以下、α(N)をアッカーマン関数の逆関数とします。  


### ```uf = UnionFind(n: int)```
n個の要素からなるUnionFindを構築します。時間計算量O(N)です。

### ```uf.root(x: int) -> int```
要素xを含む集合の代表元を返します。

### ```uf.unite(x: int, y: int) -> int```
要素xを含む集合と要素yを含む集合を併合し、併合後の集合の代表元を返します。時間計算量O(α(N))です。

### ```uf.same(x: int, y: int) -> bool```
要素xと要素yが同じ集合に属するならTrueを、そうでないならFalseを返します。時間計算量O(α(N))です。

### ```uf.size(x: int) -> int```
要素xを含む集合の要素数を返します。時間計算量O(α(N))です。

### ```uf.members(x: int) -> Set[int]```
要素xを含む集合を返します。時間計算量O(size(x))です(！)。

### ```uf.all_roots() -> List[int]```
全ての集合の代表元からなるリストを返します。時間計算量O(N)です。

### ```uf.group_count() -> int```
ufの集合の総数を返します。時間計算量O(1)です。

### ```uf.all_group_members() -> defaultdict[int, List[int]]```
keyに代表元、valueにkeyを代表元とする集合のリストをもつdefaultdictを返します。時間計算量O(Nα(N))です。

### ```uf.claer() -> None```
集合を工場出荷状態に戻します。時間計算量O(N)です。

### ```str(uf)```
よしなにします。時間計算量O(Nα(N))です。
