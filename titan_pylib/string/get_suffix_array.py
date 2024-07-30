from titan_pylib.string.hash_string import HashString
from titan_pylib.algorithm.sort.merge_sort import merge_sort


def get_suffix_array(s: str, hs: HashString) -> list[int]:
    """suffix_arrayを求めます。

    ロリハで大小比較をするため、比較関数に :math:`O(logn)` 、
    ソートが :math:`O(nlogn*(比較関数の計算量))` で、
    全体 :math:`O(nlog^2n)` です。

    Args:
        s (str): 文字列です。
        hs (HashString): ``HashString`` です。

    Returns:
        list[int]: suffix_array です。
    """

    def cmp(u: int, v: int) -> bool:
        ok, ng = 0, min(n - u, n - v)
        while ng - ok > 1:
            mid = (ok + ng) >> 1
            if hs.get(u, u + mid) == hs.get(v, v + mid):
                ok = mid
            else:
                ng = mid
        return s[u + ok] < s[v + ok]

    n = len(s)
    return merge_sort(range(n), key=cmp)
