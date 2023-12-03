_____

# `RandomTree`

_____

## コード

[`RandomTree`](https://github.com/titan-23/Library_py/blob/main/Algorithm/Random/RandomTree.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/Algorithm\Random\RandomTree.py -->

_____

- ランダムな木を作ります。
- 作問作業にどうぞ

_____

## 仕様

### `RandomTreeType`
- `RandomTree`で木の形を指定するときに使用する列挙型クラスです。

### `RandomTree`

#### `RandomTree.build(n: int, typ: RandomTreeType=RandomTreeType.random, seed: Optional[int]=None)`
- 頂点数 `n` 、木の形 `typ` をもとにランダムな木を生成し、辺を返します。
  - `RandomTreeType.random` もしくは指定しないとき、ただのランダムです。
  - `RandomTreeType.path` のとき、ランダムなパスグラフです。
  - `RandomTreeType.star` のとき、ランダムなスターグラフです。
  - そうでないとき、`ValueError` を出します。
- 辺のインデックスは 0-indexed です。
- `O(nlogn)` です。

_____

## 使用例

```python
from Library_py.Algorithm.Random.RandomTree import RandomTreeType
from Library_py.Algorithm.Random.RandomTree import RandomTree

edges = RandomTree.build(5, RandomTreeType.random, seed=10)
for u, v in edges:
  print(u, v)
  # 2 0
  # 1 4
  # 0 3
  # 3 4
```
