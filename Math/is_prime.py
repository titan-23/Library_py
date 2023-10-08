def is_prime64(n: int) -> bool:
  # assert 1 <= n and n <= 1<<64 # = 18446744073709551616
  if n == 1:
    return False
  if n == 2:
    return True
  if not n & 1:
    return False  
  p = [2, 7, 61] if n < 1<<30 else [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
  d = n - 1
  d >>= (d & -d).bit_length() - 1
  for a in p:
    if n <= a: break
    t = d
    y = pow(a, t, n)
    while t != n-1 and y != 1 and y != n-1:
      y = pow(y, 2, n)
      t <<= 1
    if y != n-1 and not t&1:
      return False
  return True

