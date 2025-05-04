class Trie:

    class Node:

        __slots__ = "child", "count", "stop_count"

        def __init__(self):
            self.child: dict[str, Trie.Node] = {}
            self.count = 0
            self.stop_count = 0

    def __init__(self):
        self.root = Trie.Node()

    def add(self, s: str) -> None:
        node = self.root
        for c in s:
            node.count += 1
            ch = node.child.get(c)
            if ch is None:
                ch = Trie.Node()
                node.child[c] = ch
            node = ch
        node.stop_count += 1

    def s_prefix(self, pref) -> int:
        """?"""
        node = self.root
        for dep, c in enumerate(pref):
            if c not in node.child:
                return dep
            node = node.child[c]
        return len(pref)

    def erase(self, s) -> None:
        """sがあればsを一つ削除する / O(|s|)"""
        if s not in self:
            return
        node = self.root
        for c in s:
            node.count -= 1
            node = node.child[c]
        node.stop_count -= 1

        node = self.root
        for c in s:
            if node.child[c].count + node.child[c].stop_count == 0:
                del node.child[c]
                break
            node = node.child[c]

    def erase_prefix(self, pref) -> int:
        """prefを接頭辞に持つすべての文字列を削除し、削除した文字列の個数を返す / O(|pref|)"""
        node = self.root
        for c in pref:
            if c not in node.child:
                return 0
            node = node.child[c]
        remove_cnt = node.count + node.stop_count
        node = self.root
        if node.count - remove_cnt == 0:  # 全部消える
            self.root = Trie.Node()
            return remove_cnt
        par = None
        for c in pref:
            node.count -= remove_cnt
            if (node.child[c].count + node.child[c].stop_count) - remove_cnt == 0:
                del node.child[c]
                return remove_cnt
            par = node
            node = node.child[c]
        if par is not None:
            del par.child[node.c]
        return remove_cnt

    def contains_prefix(self, pref: str) -> bool:
        """prefを接頭辞に持つ文字列があるかどうか / O(|pref|)"""
        node = self.root
        for c in pref:
            if c not in node.child:
                return False
            node = node.child[c]
        return True

    def contains_prefix_inv(self, s: str) -> bool:
        """sの接頭辞になり得る文字列が存在しているか / O(|s|)"""
        node = self.root
        for c in s:
            if c not in node.child:
                return False
            if node.stop_count > 0:
                return True
            node = node.child[c]
            if node.stop_count > 0:
                return True
        return False

    def count_prefix(self, s: str) -> list[int]:
        """sを接頭辞に持つ文字列がいくつあるか a[i]:=s[:i]スタートの文字列がいくつあるか"""
        node = self.root
        n = len(s)
        ans = [0] * (n + 1)
        for dep, c in enumerate(s):
            ans[dep] = node.count + node.stop_count
            node = node.child.get(c)
            if node is None:
                return ans
        ans[n] = node.count + node.stop_count
        return ans

    def count(self, s: str) -> int:
        """sがいくつ含まれているか"""
        node = self.root
        for c in s:
            if c not in node.child:
                return 0
            node = node.child[c]
        return node.stop_count

    def tolist(self) -> list[str]:
        res = []
        s = []

        def dfs(node: Trie.Node):
            if not node:
                return
            if node.stop_count > 0:
                t = "".join(s)
                for _ in range(node.stop_count):
                    res.append(t)
            for k, v in node.child.items():
                s.append(k)
                dfs(v)
                s.pop()

        dfs(self.root)
        return res

    def __len__(self) -> int:
        return self.root.count

    def __contains__(self, s: str) -> bool:
        return self.count(s) > 0

    def print(self, is_sort=False) -> None:
        def dfs(node: Trie.Node, indent: str) -> None:
            if len(node.child) == 0:
                return
            a = list(node.child.items())
            if is_sort:
                a.sort()  # 挿入順にするかどうか
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
