# from titan_pylib.graph.get_articulation_points import get_articulation_points
from types import GeneratorType

"""Return articulation points. / O(|V|+|E|)"""


# https://algo-logic.info/articulation-points/
def get_articulation_points(G: list[list[int]]) -> list[int]:
    n = len(G)
    order = [-1] * n
    res: list[int] = []
    cnt = 0

    def antirec(func):
        # 再帰用デコレータ
        # yieldにするのを忘れないこと
        # 参考: https://github.com/cheran-senthil/PyRival/blob/master/pyrival/misc/bootstrap.py
        stack = []

        def wrappedfunc(*args, **kwargs):
            if stack:
                return func(*args, **kwargs)
            to = func(*args, **kwargs)
            while True:
                if isinstance(to, GeneratorType):
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to

        return wrappedfunc

    @antirec
    def dfs(v: int, p: int) -> int:
        nonlocal cnt
        r_min = order[v] = cnt
        fcnt = 0
        p_art = 0
        cnt += 1
        for w in G[v]:
            if w == p:
                continue
            if order[w] == -1:
                ret = yield dfs(w, v)
                p_art |= order[v] <= ret
                r_min = min(r_min, ret)
                fcnt += 1
            else:
                r_min = min(r_min, order[w])
        p_art |= r_min == order[v] and len(G[v]) > 1
        if (p == -1 and fcnt > 1) or (p != -1 and p_art):
            res.append(v)
        yield r_min

    if G:
        dfs(0, -1)
    return res
