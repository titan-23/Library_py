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
        for c in pref:
            node.count -= remove_cnt
            assert node.count > 0
            assert c in node.child
            if node.child[c].count - remove_cnt == 0:
                del node.child[c]
                return remove_cnt
            node = node.child[c]
        node.count = 0
        node.stop_count = 0
        node.child.clear()
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

    def count(self, s: str) -> int:
        """sがいくつ含まれているか"""
        node = self.root
        for dep, c in enumerate(s):
            if c not in node.child:
                return 0
            node = node.child[c]
        return node.stop_count

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
