_____

# `Random`

_____

## コード

[`Random`](https://github.com/titan-23/Library_py/blob/main/Algorithm/Random/Random.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/Algorithm\Random\Random.py -->

_____

乱数系のライブラリです。標準ライブラリより高速なつもりでいます。

_____

## 仕様

#### `Random.random() -> float`
- 0以上1以下の一様ランダムな値を1つ生成して返すはずです。

#### `Random.randint(begin: int, end: int) -> int`
- `begin` 以上 `end` **以下**のランダムな整数を返します。

#### `Random.randrange(begin: int, end: int) -> int`
- `begin` 以上 `end` **未満**のランダムな整数を返します。

#### `Random.shuffle(a: List[Any]) -> None`
- `a` をインプレースにシャッフルします。
- `O(N)` です。
_____

## 使用例

```python
from Library_py.Algorithm.Random.Random import Random
```
