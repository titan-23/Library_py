def range_xor(l: int, r: int) -> int:
    """[l, r)の総XORを返す / O(1)"""

    def F(n):
        if n % 4 == 0:
            return 0
        elif n % 4 == 1:
            return n - 1
        elif n % 4 == 2:
            return 1
        else:
            return n

    return F(r) ^ F(l)


def range_xor_step(start: int, stop: int, step: int) -> int:
    """range(start, stop, step)の総XORを返す / O(log(stop))"""
    if start >= stop:
        return 0
    cnt = (stop - start + step - 1) // step
    res = 0
    bit_max = stop.bit_length() + 1
    for b in range(bit_max):
        bit = 1 << b
        s = (start >> b) & 1
        t = (step >> b) & 1
        one = s * cnt if t == 0 else (cnt + s) // 2
        if one % 2 == 1:
            res |= bit
    return res
