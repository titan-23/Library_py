from titan_pylib.others.antirec import antirec


def get_scc_graph(
    G: list[list[int]],
) -> tuple[list[list[int]], list[list[int]], list[int], list[list[int]]]:
    """
    scc, 頂点を縮約した隣接リスト, もとの頂点->新たなグラフの頂点, 新たなグラフの頂点->もとの頂点
    """
    n = len(G)
    stack = [0] * n
    ptr = 0
    lowlink = [-1] * n
    order = [-1] * n
    ids = [0] * n
    cur_time = 0
    group_cnt = 0

    @antirec
    def dfs(v: int):
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

    F = [set() for _ in range(max(ids) + 1)]
    for v in range(n):
        for x in G[v]:
            if ids[v] != ids[x]:
                F[ids[v]].add(ids[x])
    F = [list(f) for f in F]
    ids_inv = [[] for _ in range(len(F))]
    for i, v in enumerate(ids):
        ids_inv[v].append(i)
    return groups, F, ids, ids_inv
