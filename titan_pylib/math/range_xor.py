def range_xor(l: int, r: int) -> int:
    """[l, r)の総XORを返す / O(1)"""

    def F(n):
        if n % 4 == 0:
            return n
        elif n % 4 == 1:
            return 1
        elif n % 4 == 2:
            return n + 1
        else:
            return 0

    return F(r - 1) ^ F(l - 1)


def range_xor_step(start: int, stop: int, step: int) -> int:
    """range(start, stop, step)の総XORを返す / O(log stop)"""
    if start >= stop or step <= 0:
        return 0
    # 範囲内の要素数
    cnt = (stop - start + step - 1) // step
    res = 0
    bit_max = max(start, stop, step).bit_length()
    for b in range(bit_max):
        bit = 1 << b
        # ステップがビット b で 1 なら、等差数列の各項のビット b の値を考慮
        if (step >> b) & 1:
            # 等差数列 start, start + step, ... のビット b の 1 の出現回数を計算
            one_count = 0
            for i in range(cnt):
                if ((start + i * step) >> b) & 1:
                    one_count += 1
            if one_count % 2:
                res |= bit
        else:
            # ステップのビット b が 0 なら、start のビット b の値が全項に反映
            if (start >> b) & 1:
                if cnt % 2:
                    res |= bit
    return res
