_____

# [EulerTourTree.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/EulerTourTree/EulerTourTree.py)


`Euler Tour Tree` です。森を管理します。部分木クエリの強さに定評があります。


## 解説

解説を入れます。嘘があるかもです。勝手に混乱していってください。  

森です。各連結成分(木)は独立なのでそれごとに見ていきます。  
基本戦術はオイラーツアー(Euler tour technique)です。これはググってください。  
実は、ある木をオイラーツアーした列と、その木に対して 根の変更 / 辺の追加 / 辺の削除 をした木のオイラーツアーした列との差分は多くはありません。実際に紙に書くとよいでしょう。これをうまいこと管理します。  

列を平衡二分木で管理します。ここで、オイラーツアーの列はでは頂点ではなく辺の列とします。例えば、  
`[0, 1, 0, 2, 0]`  
の頂点列は辺列  
`[{0, 0}, {0, 1}, {1, 1}, {1, 0}, {0, 2}, {2, 2}, {2, 0}]`  
などとなります。  
また、補助データ構造として辺からノードのポインタをたどれる辞書を保持します。  
各処理の流れは以下のようになります。

- 根の変更: `reroot(v)`
  - 辺`{v,v}` の頂点の直前で `split` し、それを順に `A, B` とする
  - `B` と `A` をこの順にマージする
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
`n/len(a)` 個の頂点からなる `EulerTourTree` を作成します。 `n_or_a` が `a` のとき、頂点の重みとみなします。

### `ett.build(G: List[List[int]]) -> None`
隣接リスト `G` をもとにして、 `ett` に辺を張り構築します。

### `ett.link(u: int, v: int) -> None`
辺 `{u, v}` を追加します。 `u` と `v` が同じ連結成分にいてはいけません。

### `ett.cut(u: int, v: int) -> None`
辺 `{u, v}` を削除します。辺 `{u, v}` が存在してなければいけません。

### `ett.merge(u: int, v: int) -> bool`
`u` と `v` が同じ連結成分にいる場合はなにもせず `False` を返します。そうでない場合は辺 `{u, v}` を追加し `True` を返します。

### `ett.split(u: int, v: int) -> bool`
辺 `{u, v}` が存在しない場合はなにもせず `False` を返します。そうでない場合は辺 `{u, v}` を削除し `True` を返します。

### `ett.leader(v: int) -> Node`
`v` を含む木の代表元を返します。 `reroot` すると変わるので注意です。

### `ett.reroot(v: int) -> None`
`v` を含む木の根を `v` にします。

### `ett.same(u: int, v: int) -> bool`
`u` と `v` が同じ連結成分にいれば `True` を、そうでなければ `False` を返します。

### `ett.show() -> None`
デバッグ用です。

### `ett.subtree_apply(v: int, p: int, f: F) -> None`
`v` を根としたときの部分木に `f` を適用します。ただし、 `v` の親は `p` です。 `v` の親が存在しないときは `p=-1` として下さい。

### `ett.subtree_sum(v: int, p: int) -> T`
`v` を根としたときの部分木の総和を返します。ただし、 `v` の親は `p` です。 `v` の親が存在しないときは `p=-1` として下さい。

### `ett.group_count() -> int`
連結成分の個数を返します。

### `ett.get_vertex(v: int) / ett[v: int] -> T`
`v` の `key` を返します。

### `ett.set_vertex(v: int, val: T) / ett[v: int] = val -> None`
`v` の `key` を `val` に更新します。

