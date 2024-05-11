from collections import Counter
from typing import List, Tuple


class Divisors:

    # 高速素因数分解
    # init: O(NloglogN)
    # N個の数の素因数分解 : O(NlogA)
    class Osa_k:

        def __init__(self, n: int):
            _min_factor = list(range(n + 1))
            for i in range(2, int(n**0.5) + 1):
                if _min_factor[i] == i:
                    for j in range(2, int(n // i) + 1):
                        if _min_factor[i * j] > i:
                            _min_factor[i * j] = i
            self._min_factor = _min_factor

        def p_factorization(self, n: int) -> List[int]:
            ret = []
            _min_factor = self._min_factor
            while n > 1:
                ret.append(_min_factor[n])
                n //= _min_factor[n]
            return ret

        def p_factorization_Counter(self, n: int) -> Counter:
            ret = Counter()
            _min_factor = self._min_factor
            while n > 1:
                ret[_min_factor[n]] += 1
                n //= _min_factor[n]
            return ret

        def get_divisors(self, n: int) -> set:
            def dfs(indx, val):
                nonlocal f, m, ret
                k, v = f[indx]
                if indx + 1 < m:
                    for i in range(v + 1):
                        dfs(indx + 1, val * k**i)
                else:
                    for i in range(v + 1):
                        ret.add(val * k**i)

            f = list(self.p_factorization_Counter(n).items())
            m = len(f)
            ret = set()
            dfs(0, 1)
            return ret

    """約数全列挙. / O(√N)"""

    @staticmethod
    def get_divisors(n: int) -> List[int]:
        l = []
        r = []
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                l.append(i)
                if i != n // i:
                    r.append(n // i)
        return l + r[::-1]

    "Nを1回素因数c分解する / O(√N)"

    @staticmethod
    def factorization(n: int) -> List[Tuple[int, int]]:
        ret = []
        if n == 1:
            return ret
        for i in range(2, int(-(-(n**0.5) // 1)) + 1):
            if n == 1:
                break
            if n % i == 0:
                cnt = 0
                while n % i == 0:
                    cnt += 1
                    n //= i
                ret.append((i, cnt))
        if n != 1:
            ret.append((n, 1))
        return ret

    "Nを1回素因数分解する / O(√N)"

    @staticmethod
    def factorization_counter(n: int) -> Counter:
        ret = Counter()
        if n == 1:
            return ret
        for i in range(2, int(-(-(n**0.5) // 1)) + 1):
            if n == 1:
                break
            if n % i == 0:
                cnt = 0
                while n % i == 0:
                    cnt += 1
                    n //= i
                ret[i] = cnt
        if n != 1:
            ret[n] = 1
        return ret

    "Nの約数の個数を求める / O(√N)"

    @staticmethod
    def divisors_num(n: int) -> int:
        cnt = 0
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                cnt += 1
                if i != n // i:
                    cnt += 1
        return cnt

    "N以下のそれぞれの数の約数の個数を求める / O(NlogN)"

    @staticmethod
    def divisors_num_all(n) -> List[int]:
        li = [0] * (n + 1)
        for i in range(1, n + 1):
            for j in range(i, n + 1, i):
                li[j] += 1
        return li

    "N以下のそれぞれの数の素因数の種類数を求める / O(NloglogN)"

    @staticmethod
    def primefactor_num(n) -> List[int]:
        cnt = [0] * (n + 1)
        for i in range(2, n + 1):
            if cnt[i] >= 1:
                continue
            for j in range(i, n + 1, i):
                cnt[j] += 1
        return cnt

    "エラトステネスの篩(N以下の素数を返す) / O(NloglogN)"

    @staticmethod
    def get_primelist(limit: int) -> List[int]:
        p = [1] * (limit + 1)
        p[0] = 0
        p[1] = 0
        for i in range(2, int(limit**0.5) + 1):
            if not p[i]:
                continue
            for j in range(i + i, limit + 1, i):
                p[j] = 0
        return [i for i, x in enumerate(p) if x]

    "N以下の素数の個数を求める / O(NloglogN)"

    @staticmethod
    def get_prime_count(limit: int) -> int:
        ret = 0
        for i in range(2, limit):
            for j in range(2, int(limit**0.5) + 1):
                if i % j == 0:
                    break
            else:
                ret += 1
        return ret

    "事前にエラトステネスとかでsart(N)以下の素数を全列挙しておく"
    "O(sqrt(N)log(log(sqrt(N)) + log(N))"

    @staticmethod
    def factorization_eratos(n: int, primes: List[int]) -> List[int]:
        res = []
        for p in primes:
            # if is_prime64(n): break
            if p * p > n:
                break
            if n % p == 0:
                n //= p
                while n % p == 0:
                    n //= p
                res.append(p)
        if n != 1:
            res.append(n)
        return res
