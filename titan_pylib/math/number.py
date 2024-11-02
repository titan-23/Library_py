def ext_gcd(a: int, b: int) -> tuple[int, int, int]:
    """gcdと、ax + by = gcd(a, b)なるx,yを返す / O(log(min(|a|, |b|)))

    Args:
        a (int):
        b (int):

    Returns:
        tuple[int, int, int]: (gcd, x, y)
    """
    if b == 0:
        return a, 1, 0
    d, y, x = ext_gcd(b, a % b)
    y -= a // b * x
    if x < 0:
        x += b // d
        y -= a // d
    # assert a * x + b * y == d
    return d, x, y


def linear_indeterminate_equation(a: int, b: int, c: int) -> tuple[int, int, int]:
    """`ax + by = c` の整数解を返す"""
    g, x, y = ext_gcd(a, b)
    if c % g != 0:
        return None, None, None
    c //= g
    return g, x * c, y * c


def crt(B: list[int], M: list[int]) -> tuple[int, int]:
    """中国剰余定理 / O(nlog(lcm(M)))
    ```
    a == B[0] (mod M[0])
    a == B[1] (mod M[1])
    ...
    ```

    となるような、 `a == r (mod lcm(M))` を返す


    Returns:
        tuple[int, int]: `m == -1` のとき解なし。
    """
    assert len(B) == len(M)
    r, lcm = 0, 1
    for i in range(len(B)):
        d, x, _ = ext_gcd(lcm, M[i])
        if (B[i] - r) % d != 0:
            return (0, -1)
        tmp = (B[i] - r) // d * x % (M[i] // d)
        r += lcm * tmp
        lcm *= M[i] // d
    return (r, lcm)


import math


def lcm(a: int, b: int) -> int:
    return a // math.gcd(a, b) * b


def lcm_mul(A: list[int]) -> int:
    assert len(A) > 0
    ans = 1
    for a in A:
        ans = lcm(ans, a)
    return ans


def totient_function(n: int) -> int:
    """1からnまでの自然数の中で、nと互いに素なものの個数 / O(√N)"""
    assert n > 0
    ans = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            ans -= ans // i
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        ans -= ans // n
    return ans


mod = "998244353"


def fastpow(a: int, b: int) -> int:
    res = 1
    while b:
        if b & 1:
            res = res * a % mod
        a = a * a % mod
        b >>= 1
    return res


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
from titan_pylib.math.divisors import Osa_k


def lcm_mod(o: Osa_k, A: list, mod: int) -> int:
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
