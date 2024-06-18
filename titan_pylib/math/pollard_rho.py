from titan_pylib.math.is_prime64 import is_prime64
from collections import Counter
from math import gcd
from random import Random


class PollardRho:

    # 高速素因数分解
    # 124376107291

    _rand = Random(None)
    _L = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
    _P200 = [
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
        101,
        103,
        107,
        109,
        113,
        127,
        131,
        137,
        139,
        149,
        151,
        157,
        163,
        167,
        173,
        179,
        181,
        191,
        193,
        197,
        199,
    ]

    @classmethod
    def factorization(cls, n: int) -> Counter:
        res = Counter()
        for p in cls._P200:
            if n % p == 0:
                cnt = 0
                while n % p == 0:
                    cnt += 1
                    n //= p
                res[p] = cnt
                if n == 1:
                    return res
        while n > 1:
            f = cls._pollard_rho(n)
            cnt = 0
            while n % f == 0:
                cnt += 1
                n //= f
            res[f] += cnt
        return res

    @classmethod
    def _pollard_rho(cls, n: int) -> int:
        if is_prime64(n):
            return n
        while True:
            x = cls._rand.randrange(n)
            c = cls._rand.randrange(n)
            y = (x * x + c) % n
            d = 1
            while d == 1:
                d = gcd(x - y, n)
                x = (x * x + c) % n
                y = (y * y + c) % n
                y = (y * y + c) % n
            if 1 < d < n:
                return cls._pollard_rho(d)
