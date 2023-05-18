_____

# [EulerTourTree](https://github.com/titanium-22/Library_py/blob/main/DataStructures/EulerTourTree)

_____

# [EulerTourTree.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/EulerTourTree/EulerTourTree.py)

`Euler Tour Tree` です。森を管理します。部分木クエリの強さに定評があります。  

## 解説

解説を入れます。嘘があるかもです。勝手に混乱していってください。  

森です。各連結成分(木)は独立なのでそれごとに見ていきます。  
基本戦術はオイラーツアー(Euler tour technique)です。これはググってください。  
実は、ある木をオイラーツアーした列と、その木に対して根の変更/辺の追加/辺の削除をした時のオイラーツアーした列の差分は多くはありません。実際に紙に書くとよいでしょう。これをうまいこと管理します。  

列を平衡二分木で管理します。ここで、オイラーツアーの列はでは頂点ではなく辺の列とします。例えば、  
`[0, 1, 0, 2, 0]`  
の頂点列は辺列  
`[{0, 0}, {0, 1}, {1, 1}, {1, 0}, {0, 2}, {2, 2}, {2, 0}]`  
などとなります。  
また、補助データ構造として辺からノードのポインタをたどれる辞書を保持します。  
各処理の流れは以下のようになります。
- 根の変更: `reroot(v)`
  - 辺`{v,v}` の頂点の直前で `split` し、それを順に `A, B` とする
  - BとAをこの順にマージする
- 辺の追加: `link(u, v)`
  - `reroot(u); reroot(v)`
  - `u, v` が属する木(のオイラーツアーした辺の列)をそれぞれ `E1, E2` とする
  - `E1, [{u, v}], E2, [{v, u}]` をこの順にマージする
- 辺の削除: `cut(u, v)`
  - `reroot(v); reroot(u)`
  - `{u, v}, {v, u}` で `split` してできたものを順に `A, B, C` とする。ただし、 `{u, v}` は `A` に含まれ、 `{v, u}` は `C` に含まれる。
  - `A` の末尾と `C` の先頭を削除し、 `A` と `C` をこの順にマージする 
- 連結性判定: `same(u, v)`
  - `u, v` を `splay` して、 `u` の親が `None` じゃなければ連結。 `u == v` のときは別途処理をする。

計算量は、オイラーツアーの管理と辺→ノードの管理に赤黒木を使えば最悪 `O(logN)` です。この実装ではsplay木とハッシュテーブルで管理するので償却 `O(logN)` +期待 `O(1)` です(ここで `N` と書いたものは平衡二分木の総頂点数です。オイラーツアーすると `(元の頂点数)+(辺数)*2?` の頂点ができるので、たしかに `O(元のグラフの頂点数)` ではありますが、定数倍がバカです)。  
オイラーツアーがあれば、部分木クエリは簡単に処理できます。

## 仕様

### `ett = EulerTourTree(n_or_a: Union[int, Iterable[T]], op: Callable[[T, T], T]=lambda x, y: None, mapping: Callable[[F, T], T]=lambda x, y: None, composition: Callable[[F, F], F]=lambda x, y: None, e: T=None, id: F=None)`
n/len(a)個の頂点からなるEulerTourTreeを作成します。n_or_aがaのとき、頂点の重みとみなします。

### `ett.build(G: List[List[int]]) -> None`
隣接リストGをもとにして、etに辺を張り構築します。

### `link(u: int, v: int) -> None`

### `cut(u: int, v: int) -> None`

### `merge(u: int, v: int) -> bool`

### `split(u: int, v: int) -> bool`

### `leader(v: int) -> Node`

### `reroot(v: int) -> None`

### `same(u: int, v: int) -> bool`

### `show() -> None`

### `subtree_apply(v: int, p: int, f: F) -> None`

### `subtree_sum(v: int, p: int) -> T`

### `get_vertex(v: int) -> T`

### `set_vertex(v: int, val: T) -> None`

### `group_count() -> int`

### `ett[v: int] -> T`

### `ett[v: int] = val: T -> None`
