____

# [HashDict.py](https://github.com/titanium-22/Library_py/blob/main/DataStructures/Dict/HashDict.py)

最終更新：2023/05/25

ハッシュテーブルです。組み込み辞書の `dict` よりやや遅いです。使わないのが吉です。

## 仕様

### `d = HashDict(e: int=-1, default: Any=0)`
`e` , `default` から `HasiDict` を構築します。ここで、
- `e` は `int` 型で `key` として使用しない値
- `default` は存在しないキーにアクセスした値

です。 `key` を `int` 型以外のもので指定したいときは `_hash(key) -> int` 関数をいじってください。

### `d.reserve(n: int) -> None`
`reserve` します。あまり使わない方が良いかも？知らんけど。 `O(N)` です。

### `d.get(key: int, default: Any=None) -> Any`
キーが `key` の値を返します。存在しない場合、引数 `default` に `None` 以外を指定した場合は `default` が、そうでない場合はコンストラクタで設定した `default` が返ります。平均 `O(1)` です。

### `d.set(key: int, val: Any) -> None`
キーを `key` として `val` を格納します。 `key` が既に存在している場合は上書きされます。平均 `O(1)` です。

### `key: int in d`
`key` が存在すれば `True` を、そうでなければ `False` を返します。平均 `O(1)` です。  
**`key in d.keys()` は `O(N)` であることに注意してください。**

### `d[key] / d[key] = val`
`getitem / setitem` をサポートしてます。平均 `O(1)` です。

### `d.keys()` / `d.values()` / `d.items()`
`Iterator` です。それぞれ、 `key集合` / `val集合` / `keyとそれに対応するvalのタプル` を列挙します。 `O(N)` です。順序は特に決めてません。

### `str(d) / len(d)`
よしなよしなです。

