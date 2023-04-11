def next_permutation(a: list, l: int=0, r: int=-1) -> bool:
  if r == -1:
    r = len(a)
  for i in range(r-2, l-1, -1):
    if a[i] < a[i+1]:
      for j in range(r-1, i, -1):
        if a[i] < a[j]:
          a[i], a[j] = a[j], a[i]
          p = i + 1
          q = r - 1
          while p < q:
            a[p], a[q] = a[q], a[p]
            p += 1
            q -= 1
          return True
  return False


def prev_permutation(a: list) -> bool:
  l = 0
  r = len(a)
  for i in range(r-2, l-1, -1):
    if a[i] > a[i+1]:
      for j in range(r-1, i, -1):
        if a[i] > a[j]:
          a[i], a[j] = a[j], a[i]
          p = i + 1
          q = r - 1
          while p < q:
            a[p], a[q] = a[q], a[p]
            p += 1
            q -= 1
          return True
  return False
