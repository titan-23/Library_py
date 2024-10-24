from typing import Iterator


def gray_code(n) -> Iterator[int]:
    """長さ n の bit 列に対し、0,1,...,(1<<n) を列挙する。
    i 番目の返り値は、前と変化する位置を返す。
    """
    pre = 0
    for i in range(1, 1 << n):
        now = i ^ (i >> 1)
        yield (pre ^ now).bit_length() - 1
        pre = now
