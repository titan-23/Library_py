from titan_pylib.string.hash_string import HashString
from titan_pylib.algorithm.sort.merge_sort import merge_sort
from typing import List

def get_suffix_array(s: str, hs: HashString) -> List[int]:
  def cmp(u: int, v: int) -> bool:
    ok, ng = 0, min(n-u, n-v)
    while ng - ok > 1:
      mid = (ok + ng) >> 1
      if hs.get(u, u+mid) == hs.get(v, v+mid):
        ok = mid
      else:
        ng = mid
    return s[u+ok] < s[v+ok]
  n = len(s)
  return merge_sort(range(n), key=cmp)

