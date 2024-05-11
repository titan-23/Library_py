from __pypy__ import newlist_hint
from typing import List, Tuple


def cartesian_tree(a: List[int]) -> Tuple[List[int], List[int], List[int]]:
    """Get cartesian_tree. / O(N)"""
    n = len(a)
    par = [-1] * n
    left = [-1] * n
    right = [-1] * n
    path = newlist_hint(n)
    for i, aa in enumerate(a):
        pre = -1
        while path and aa < a[path[-1]]:
            pre = path.pop()
        if pre != -1:
            par[pre] = i
        if path:
            par[i] = path[-1]
        path.append(i)
    for i, p in enumerate(par):
        if p == -1:
            continue
        if i < p:
            left[p] = i
        else:
            right[p] = i
    return par, left, right
