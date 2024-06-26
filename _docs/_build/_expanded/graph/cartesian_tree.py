# from titan_pylib.graph.cartesian_tree import cartesian_tree
def cartesian_tree(a: list[int]) -> tuple[list[int], list[int], list[int]]:
    """Get cartesian_tree. / O(N)"""
    n = len(a)
    par = [-1] * n
    left = [-1] * n
    right = [-1] * n
    path = []
    for i, e in enumerate(a):
        pre = -1
        while path and e < a[path[-1]]:
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
