# 展開に失敗しました
mod = 1000000007
mod = 998244353


def fastpow(a, b):
    res = 1
    while b:
        if b & 1:
            res = res * a % mod
        a = a * a % mod
        b >>= 1
    return res


# 拡張ユークリッド非再帰
def modinv(a, mod):
    b = mod
    x, y, u, v = 1, 0, 0, 1
    while b:
        k = a // b
        x -= k * u
        y -= k * v
        x, u = u, x
        y, v = v, y
        a, b = b, a % b
    x %= mod
    return x


def isqrt(n: int) -> int:
    assert n >= 0
    if n == 0:
        return 0
    x = 1 << (n.bit_length() + 1) >> 1
    y = (x + n // x) >> 1
    while y < x:
        x, y = y, (y + n // y) >> 1
    return x


"Return LCM % mod"
from collections import Counter
from titan_pylib.math.divisors import Divs


def lcm_mod(o: Divs.Osa_k, A: list, mod: int) -> int:
    cou = Counter()
    for a in A:
        for k, v in Counter(o.p_factorization(a)).items():
            cou[k] = max(cou[k], v)
    lcm = 1
    for k, v in cou.items():
        lcm *= pow(k, v, mod)
        lcm %= mod
    return lcm % mod


#  -----------------------  #

"Return (a // b) % mod"
"O(1), mod: prime"


def div_mod(a: int, b: int, mod: int) -> int:
    "Return (a // b) % mod"
    return (a % mod) * pow(b, mod - 2, mod) % mod


#  -----------------------  #


def large_pow(a, b, c, mod):
    "return (a^(b^c)) % mod. p: prime."
    if a % mod == 0:
        return 0
    return pow(a, pow(b, c, mod - 1), mod)


#  -----------------------  #


def mat_mul(A: list, B: list, mod: int) -> list:
    l, m = len(A), len(A[0])
    n = len(B[0])
    assert m == len(B)
    return [
        [sum([A[i][k] * B[k][j] for k in range(m)]) % mod for j in range(n)]
        for i in range(l)
    ]


def mat_powmod(A: list, n: int, mod: int) -> list:
    res = [[0] * len(A) for _ in range(len(A))]
    for i in range(len(A)):
        res[i][i] = 1
    while n > 0:
        if n & 1 == 1:
            res = mat_mul(A, res, mod)
        A = mat_mul(A, A, mod)
        n >>= 1
    return res


#  -----------------------  #
