class FunctionalGraph:

    def __init__(self, A: list[int]) -> None:
        # i -> A[i]
        n = len(A)
        G = [[] for _ in range(n)]
        revG = [[] for _ in range(n)]
        for i, p in enumerate(A):
            G[i].append(p)
            revG[p].append(i)

        dataG = [[] for _ in range(n)]
        data_cycle = []
        cycle_ids = [-1] * n
        cycle_id_now = 0

        def calc(v: int):
            nonlocal cycle_id_now
            # vを持つ連結成分に対して処理する
            todo = [v]
            seen[v] = True
            cycle = []
            while todo:
                v = todo.pop()
                cycle.append(v)
                for x in G[v]:
                    if seen[x]:
                        cycle.append(x)
                        break
                    seen[x] = True
                    todo.append(x)
            goal = cycle.pop()
            for i in range(len(cycle)):
                if cycle[i] == goal:
                    cycle = cycle[i:]
                    break
            data_cycle.append(cycle)
            for c in cycle:
                seen_cycle[c] = True
                cycle_ids[c] = cycle_id_now
            for root in cycle:
                todo = [root]
                while todo:
                    v = todo.pop()
                    seen[v] = True
                    cycle_ids[v] = cycle_id_now
                    for x in revG[v]:
                        if seen_cycle[x]:
                            continue
                        todo.append(x)
                        dataG[v].append(x)
                        dataG[x].append(v)
            cycle_id_now += 1

        seen_cycle = [False] * n
        seen = [False] * n
        for i in range(n):
            if seen[i]:
                continue
            calc(i)
        # vが属する連結成分に含まれるサイクルが、data_cycleの何番目か
        # ex: https://atcoder.jp/contests/abc357/submissions/59220690
        self.cycle_ids = cycle_ids
        self.data_cycle = data_cycle
        self.dataG = dataG
