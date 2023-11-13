_____

# `FastO`

_____

## コード

[`FastO`](https://github.com/titan-23/Library_py/blob/main/IO/FastO.py)
<!-- code=https://github.com/titan-23/Library_py/blob/main/IO\FastO.py -->

_____

- 標準出力高速化ライブラリです。
- `__pypy__.StringBuilder` を利用しています。

_____

## 仕様

#### `FastO.write(*args, sep: str=' ', end: str='\n', flush: bool=False)`
標準出力します。次の`FastO.flush()`が起きるとprintします。

#### `FastO.flush()`
flushします。これを実行しないとwriteした内容が表示されないので忘れないでください。

_____

## 使用例

```python
from Library_py.IO.FastO import FastO
write, flush = FastO.write, FastO.flush

for i in range(10):
  write(i)
flush()
```
