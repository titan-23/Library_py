raise NotImplementedError


class TrieNode:

    def __init__(self) -> None:
        self.child: dict["TrieNode"] = {}
        self.cnt: int = 0
        self.leaf: int = 0


class Trie:

    def __init__(self) -> None:
        self.root = TrieNode()

    def find(self, key: str):
        node = self.root
        for c in key:
            if c not in node.child:
                return None
            node = node.child[c]
        return node

    def __contains__(self, key: str) -> bool:
        node = self.find(key)
        return node and node.leaf > 0

    def add(self, key: str) -> None:
        self.root.cnt += 1
        node = self.root
        for c in key:
            if c not in node.child:
                node.child[c] = TrieNode()
            node = node.child[c]
            node.cnt += 1
        node.leaf += 1

    def __len__(self) -> int:
        return self.root.cnt

    def lcp(self, key: str) -> int:
        assert key in self
        node = self.root
        for dep, c in enumerate(key):
            if c not in node.child:
                return dep
            if node.cnt <= 1:
                return dep
            node = node.child[c]
        return len(key)
