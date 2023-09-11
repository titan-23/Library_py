from .is_prime import is_prime64
from .is_prime import is_prime64
from functools import lru_cache
from collections import Counter
from random import randrange
from math import gcd

class PollardRho():
  
  # 高速素因数分解

  L = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
  P200 = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 
    89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 
    181, 191, 193, 197, 199,
  ]

  @classmethod
  def factorization(cls, n: int) -> Counter:
    res = Counter()
    for p in cls.P200:
      if n % p == 0:
        cnt = 0
        while n % p == 0:
          cnt += 1
          n //= p
        res[p] = cnt
        if n == 1:
          return res
    todo = [n]
    while todo:
      v = todo.pop()
      if v <= 1: continue
      f = cls._pollard_rho(v)
      if is_prime64(f):
        cnt = 0
        while v % f == 0:
          cnt += 1
          v //= f
        res[f] += cnt
        todo.append(v)
      elif is_prime64(v//f):
        f = v // f
        cnt = 0
        while v % f == 0:
          cnt += 1
          v //= f
        res[f] += cnt
        todo.append(v)
      else:
        todo.append(f)
        todo.append(v//f)
    return res

  @staticmethod
  def _pollard_rho(n: int) -> int:
    if n & 1 == 0: return 2
    if n % 3 == 0: return 3
    s = ((n-1) & (1-n)).bit_length() - 1
    d = n >> s
    for a in PollardRho.L:
      p = pow(a, d, n)
      if p == 1 or p == n-1 or a%n == 0:
        continue
      for _ in range(s):
        prev = p
        p = (p*p) % n
        if p == 1:
          return gcd(prev-1, n)
        if p == n-1:
          break
      else:
        for i in range(2, n):
          x = i
          y = (i*i+1)%n
          f = gcd(abs(x-y), n)
          while f == 1:
            x = (x*x+1) % n
            y = (y*y+1) % n
            y = (y*y+1) % n
            f = gcd(abs(x-y), n)
          if f != n:
            return f
    return n

