_____

# `PersistentArray`

_____

## コード

[`PersistentArray`](https://github.com/titan-23/Library_py/blob/main/DataStructures/Array/PersistentArray.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/DataStructures/Array/PersistentArray.py -->

_____

- 永続配列です。
  - 過去の更新とアクセスが可能です。

_____

## 仕様

#### `pa = PersistentArray(a: Iterable[T]=[], init_t: int=0)`

- `a` から永続配列 `PersistentArray` を構築します。
- `init_t` は初期時刻です。
- 計算量 `Θ(N)` です。

#### `pa.set(k: int, v: T, pre_t: int, new_t: int) -> None`

- `pa` を更新します。
  - 位置 `k` を `v` に更新します。
  - 更新前のバージョンを `pre_t` 、更新後のバージョンを `new_t` とします。
- 計算量は時間・空間ともに `Θ(logN)` です。

#### `pa.get(k: int, t: int) -> T`

- 位置 `k` 、バージョン `t` の要素を返します。
- 時間計算量 `Θ(1)` です。

#### `pa.copy(pre_t: int, new_t: int) -> None`

- バージョン `pre_t` を変更せずバージョン `new_t` へコピーします。
- 計算量は時間・空間ともに `Θ(1)` です。

#### `pa.tolist(t: int) -> List[T]`

- バージョン `t` の配列をリストにして返します。
- 計算量は時間・空間ともに `Θ(N)` です。

_____

## 使用例

```python
from Library_py.DataStructures.Array.PersistentArray import PersistentArray

pa = PersistentArray()
```
