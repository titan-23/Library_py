____

# `HashDict.py`

____

## コード
[`HashDict.py`](https://github.com/titanium-22/Library_py/blob/main/DataStructures/Dict/HashDict.py)

____

ハッシュテーブルです。組み込み辞書の `dict` よりやや遅いです。使わないのが吉です。存在意義を教えてください。

再構築の基準: 50 %

一応 `uint` を想定しているので、 `e` は `int` 型の `-1` を設定しています。Hash関数やrehashの基準は適当。有識者求みます。( `int` を載せるのに `e` を `None` にすると、 `list` の `strategy` の問題で有意に遅くなる。注意。)

____

## 仕様

### `d = HashDict(e: int=-1, default: Any=0)`
- `e` , `default` から `HasiDict` を構築します。ここで、
  - `e` は `int` 型で `key` として使用しない値
  - `default` は存在しないキーにアクセスした値
です。 `key` を `int` 型以外のもので指定したいときは `_hash(key) -> int` 関数をいじってください。

### `d.reserve(n: int) -> None`
- `reserve` します。
- `Θ(n)` です。

### `d.get(key: int, default: Any=None) -> Any`
- キーが `key` の値を返します。存在しない場合、引数 `default` に `None` 以外を指定した場合は `default` が、そうでない場合はコンストラクタで設定した `default` が返ります。
- 期待 `O(1)` です。

### `d.set(key: int, val: Any) -> None`
- キーを `key` として `val` を格納します。 `key` が既に存在している場合は上書きされます。
- 期待 `O(1)` です。

### `key: int in d`
- `key` が存在すれば `True` を、そうでなければ `False` を返します。
- **`key in d.keys()` は `O(N)` であることに注意してください。**
- 期待 `O(1)` です。  

### `d[key] / d[key] = val`
- `getitem / setitem` をサポートしてます
- 期待 `O(1)` です。

### `d.keys() / d.values() / d.items()`
- `Iterator` です。それぞれ、 `key 集合` / `val 集合` / `key とそれに対応する val のタプル` を列挙します。順序は特に決めてません。
- `Θ(N)` です。

### `str(d) / len(d)`
- `len(d)` は `O(1)` です。

____

## 使用例

```python
d = HashDict()
```
