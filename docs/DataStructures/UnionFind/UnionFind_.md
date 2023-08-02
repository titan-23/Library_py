# [UnionFind.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/UnionFind/UnionFind.py)
UnionFindです。素集合データ構造です。 

- uniteの戻り値をNoneからintに変更しました

以下、α(N)をアッカーマン関数の逆関数とします。  

### `uf = UnionFind(n: int)`
`n` 個の要素からなる `UnionFind` を構築します。時間計算量 `Θ(N)` です。

### `uf.root(x: int) -> int`
要素 `x` を含む集合の代表元を返します。

### `uf.unite(x: int, y: int) -> int`
要素 `x` を含む集合と要素 `y` を含む集合を併合し、併合後の集合の代表元を返します。 `Θ(α(N))` です。

### `uf.same(x: int, y: int) -> bool`
要素 `x` と `y` が同じ集合に属するなら `True` を、そうでないなら `False` を返します。 `Θ(α(N))` です。

### `uf.size(x: int) -> int`
要素` x` を含む集合の要素数を返します。 `Θ(α(N))` です。

### `uf.members(x: int) -> Set[int]`
要素` x` を含む集合を返します。 `Θ(size(x))` です(！)。

### `uf.all_roots() -> List[int]`
全ての集合の代表元からなるリストを返します。 `Θ(N)` です。

### `uf.group_count() -> int`
ufの集合の総数を返します。 `Θ(1)` です。

### `uf.all_group_members() -> defaultdict[int, List[int]]`
keyに代表元、valueにkeyを代表元とする集合のリストをもつdefaultdictを返します。 `Θ(Nα(N))` です。

### `uf.claer() -> None`
集合を工場出荷状態に戻します。 `Θ(N)` です。

### `str(uf)`
よしなにします。 `ΘNα(N))` です。

