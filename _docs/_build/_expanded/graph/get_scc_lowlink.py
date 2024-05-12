# from titan_pylib.graph.get_scc_lowlink import get_scc_lowlink
# from titan_pylib.others.antirec import antirec
from types import GeneratorType

# ref: https://github.com/cheran-senthil/PyRival/blob/master/pyrival/misc/bootstrap.py
# ref: https://twitter.com/onakasuita_py/status/1731535542305907041


def antirec(func):
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


def antirec_cache(func):
    stack = []
    memo = {}
    args_list = []

    def wrappedfunc(*args):
        args_list.append(args)
        if stack:
            return func(*args)
        to = func(*args)
        while True:
            if args_list[-1] in memo:
                res = memo[args_list.pop()]
                if not stack:
                    return res
                to = stack[-1].send(res)
                continue
            if isinstance(to, GeneratorType):
                stack.append(to)
                to = next(to)
            else:
                memo[args_list.pop()] = to
                stack.pop()
                if not stack:
                    break
                to = stack[-1].send(to)
        return to

    return wrappedfunc


def get_scc_lowlink(G: list[list[int]]) -> list[list[int]]:
    n = len(G)
    stack = [0] * n
    ptr = 0
    lowlink = [-1] * n
    order = [-1] * n
    ids = [0] * n
    cur_time = 0
    group_cnt = 0

    @antirec
    def dfs(v: int) -> None:
        nonlocal cur_time, ptr
        order[v] = cur_time
        lowlink[v] = cur_time
        cur_time += 1
        stack[ptr] = v
        ptr += 1
        for x in G[v]:
            if order[x] == -1:
                yield dfs(x)
                lowlink[v] = min(lowlink[v], lowlink[x])
            else:
                lowlink[v] = min(lowlink[v], order[x])
        if lowlink[v] == order[v]:
            nonlocal group_cnt
            while True:
                u = stack[ptr - 1]
                ptr -= 1
                order[u] = n
                ids[u] = group_cnt
                if u == v:
                    break
            group_cnt += 1
        yield

    for v in range(n):
        if order[v] == -1:
            dfs(v)
    groups = [[] for _ in range(group_cnt)]
    for v in range(n):
        groups[group_cnt - 1 - ids[v]].append(v)
    return groups
