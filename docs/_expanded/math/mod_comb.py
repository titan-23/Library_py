# from titan_pylib.math.mod_comb import ModComb
class ModComb998244353:

  # nCr2のみをつかうときなどは、limit=-1とかにすると吉
  def __init__(self, limit: int):
    n = max(1, limit) + 1
    fact = [0] * n
    factinv = [0] * n
    inv = [0] * n
    fact[0] = 1
    fact[1] = 1
    factinv[0] = 1
    factinv[1] = 1
    inv[1] = 1
    for i in range(2, limit+1):
      fact[i] = fact[i-1] * i % 998244353
      inv[i] = -inv[998244353 % i] * (998244353 // i) % 998244353
      factinv[i] = factinv[i-1] * inv[i] % 998244353
    self._fact = fact
    self._factinv = factinv
    self._inv = inv
    self._limit = limit

  def nPr(self, n: int, r: int) -> int:
    if r < 0 or n < r: return 0
    return self._fact[n] * self._factinv[n-r] % 998244353

  def nCr(self, n: int, r: int) -> int:
    if r < 0 or n < r: return 0
    return (self._fact[n] * self._factinv[r] % 998244353) * self._factinv[n-r] % 998244353

  def nHr(self, n: int, r: int) -> int:
    return self.nCr(n+r-1, n-1)

  def nCr2(self, n: int, r: int) -> int:
    ret = 1
    if r > n-r:
      r = n-r
    for i in range(r):
      ret *= n-i
      ret %= 998244353
    for i in range(1, r+1):
      ret *= pow(i, 998244351, 998244353)
      ret %= 998244353
    return ret


class ModComb():

  # nCr2のみをつかうときなどは、limit=-1とかにすると吉
  def __init__(self, limit: int, mod: int):
    n = max(1, limit) + 1
    fact = [0] * n
    factinv = [0] * n
    inv = [0] * n
    fact[0] = 1
    fact[1] = 1
    factinv[0] = 1
    factinv[1] = 1
    inv[1] = 1
    for i in range(2, limit+1):
      fact[i] = fact[i-1] * i % mod
      inv[i] = -inv[mod % i] * (mod // i) % mod
      factinv[i] = factinv[i-1] * inv[i] % mod
    self._fact = fact
    self._factinv = factinv
    self._inv = inv
    self._limit = limit
    self._mod = mod

  def nPr(self, n: int, r: int) -> int:
    if r < 0 or n < r: return 0
    return self._fact[n] * self._factinv[n-r] % self._mod

  def nCr(self, n: int, r: int) -> int:
    if r < 0 or n < r: return 0
    return (self._fact[n] * self._factinv[r] % self._mod) * self._factinv[n-r] % self._mod

  def nHr(self, n: int, r: int) -> int:
    return self.nCr(n+r-1, n-1)

  def nCr2(self, n: int, r: int) -> int:
    ret = 1
    if r > n-r:
      r = n-r
    for i in range(r):
      ret *= n-i
      ret %= self._mod
    for i in range(1, r+1):
      ret *= pow(i, self._mod-2, self._mod)
      ret %= self._mod
    return ret


class ModComb1000000007:

  # nCr2のみをつかうときなどは、limit=-1とかにすると吉
  def __init__(self, limit: int):
    n = max(1, limit) + 1
    fact = [0] * n
    factinv = [0] * n
    inv = [0] * n
    fact[0] = 1
    fact[1] = 1
    factinv[0] = 1
    factinv[1] = 1
    inv[1] = 1
    for i in range(2, limit+1):
      fact[i] = fact[i-1] * i % 1000000007
      inv[i] = -inv[1000000007 % i] * (1000000007 // i) % 1000000007
      factinv[i] = factinv[i-1] * inv[i] % 1000000007
    self._fact = fact
    self._factinv = factinv
    self._inv = inv
    self._limit = limit

  def nPr(self, n: int, r: int) -> int:
    if r < 0 or n < r: return 0
    return self._fact[n] * self._factinv[n-r] % 1000000007

  def nCr(self, n: int, r: int) -> int:
    if r < 0 or n < r: return 0
    return (self._fact[n] * self._factinv[r] % 1000000007) * self._factinv[n-r] % 1000000007

  def nHr(self, n: int, r: int) -> int:
    return self.nCr(n+r-1, n-1)

  def nCr2(self, n: int, r: int) -> int:
    ret = 1
    if r > n-r:
      r = n-r
    for i in range(r):
      ret *= n-i
      ret %= 1000000007
    for i in range(1, r+1):
      ret *= pow(i, 1000000005, 1000000007)
      ret %= 1000000007
    return ret


