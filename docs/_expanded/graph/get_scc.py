# from titan_pylib.graph.get_scc import get_scc
def get_scc(G: list[list[int]]) -> list[list[int]]:
    n = len(G)
    rG = [[] for _ in range(n)]
    for v in range(n):
        for x in G[v]:
            rG[x].append(v)
    visited = [0] * n
    dfsid = [0] * n
    now = n
    for s in range(n):
        if visited[s]:
            continue
        todo = [~s, s]
        while todo:
            v = todo.pop()
            if v >= 0:
                if visited[v]:
                    continue
                visited[v] = 2
                for x in G[v]:
                    if visited[x]:
                        continue
                    todo.append(~x)
                    todo.append(x)
            else:
                v = ~v
                if visited[v] == 1:
                    continue
                visited[v] = 1
                now -= 1
                dfsid[now] = v
    res = []
    for s in dfsid:
        if not visited[s]:
            continue
        todo = [s]
        visited[s] = 0
        for v in todo:
            for x in rG[v]:
                if not visited[x]:
                    continue
                visited[x] = 0
                todo.append(x)
        res.append(todo)
    # 閉路検出: len(res) == n
    return res
