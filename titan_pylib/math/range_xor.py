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
