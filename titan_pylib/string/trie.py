class Trie:
    class Node:
        def __init__(self):
            self.c = None
            self.child = {}
            self.count = 0
            self.stop_count = 0

    def __init__(self):
        self.root = Trie.Node()

    def add(self, s: str) -> None:
        node = self.root
        for dep, c in enumerate(s):
            node.count += 1
            if c not in node.child:
                node.child[c] = Trie.Node()
            node = node.child[c]
            node.c = c
        node.stop_count += 1

    def s_prefix(self, pref) -> int:
        node = self.root
        for dep, c in enumerate(pref):
            if c not in node.child:
                return dep
            node = node.child[c]
        return len(pref)

    def count(self, s: str) -> int:
        node = self.root
        for dep, c in enumerate(s):
            if c not in node.child:
                return 0
            node = node.child[c]
        return node.stop_count

    def __contains__(self, s: str) -> bool:
        return self.count(s) > 0

    def print(self) -> None:
        def dfs(node: Trie.Node, indent: str) -> None:
            if len(node.child) == 0:
                return
            a = list(node.child.items())
            # a.sort()
            for c, child in a[:-1]:
                if child.stop_count > 0:
                    c = "\033[32m" + c + "\033[m"
                print(f"{indent}├── {c}")
                dfs(child, f"{indent}|   ")
            c, child = a[-1]
            if child.stop_count > 0:
                c = "\033[32m" + c + "\033[m"
            print(f"{indent}└── {c}")
            dfs(child, f"{indent}    ")

        print("root")
        dfs(self.root, "")
