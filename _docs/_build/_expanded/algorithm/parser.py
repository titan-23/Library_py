# from titan_pylib.algorithm.parser import Parser
class Parser:
    """Parser

    Examples:
        expression: < 四則演算の式 > ::= < 乗算除算の式 > (+ or -) < 乗算除算の式 > (+ or -) ...
        term      : < 乗算除算の式 > ::= < 括弧か数 > (* or /) < 括弧か数 > (* or /) ...
        term2 など

        factor    : < 括弧か数 >     ::= '(' < 四則演算の式 > ')' or < 数 >
        number    : < 数 >          ::= ...
    """

    def __init__(self, s: str) -> None:
        self.s: str = s
        self.n: int = len(s)
        self.ptr: int = 0

    def parse(self) -> int:
        return self.expression()

    def expression(self) -> int:
        """四則演算の式をパースして、その評価結果を返す。"""
        ret = self.term()
        while self.ptr < self.n:
            if self.get_char() == "+":
                self.consume("+")
                ret += self.term()
            elif self.get_char() == "-":
                self.consume("-")
                ret -= self.term()
            else:
                break
        return ret

    def term(self) -> int:
        """乗算除算の式をパースして、その評価結果を返す。"""
        ret = self.factor()
        while self.ptr < self.n:
            if self.get_char() == "*":
                self.consume("*")
                ret *= self.factor()
            elif self.get_char() == "/":
                self.consume("/")
                ret = ret // self.factor()  # 切り捨て
            else:
                break
        return ret

    def factor(self) -> int:
        """括弧か数をパースして、その評価結果を返す。"""
        if self.ptr >= self.n:
            return 0
        if self.get_char() == "(":
            self.consume("(")
            ret = self.expression()
            self.consume(")")
            return ret
        else:
            return self.number()

    def number(self) -> int:
        """数字の列をパースして、その数を返す。"""
        ret = 0
        while self.ptr < self.n and self.get_char().isdigit():
            ret *= 10
            ret += int(self.get_char())
            self.ptr += 1
        return ret

    def consume(self, expected: str) -> None:
        """begin が expected を指していたら begin を一つ進める。"""
        assert (
            self.s[self.ptr] == expected
        ), f"Expected: {expected} but got {self.s[self.ptr]}, s={self.s}"
        self.ptr += 1

    def get_char(self) -> str:
        return self.s[self.ptr]


# import sys
# from lark import Lark
# from lark import Transformer
# from functools import reduce


# class CalcTransformer(Transformer):
#     def expr(self, tree):
#         return reduce(lambda x, y: x + y, tree)

#     def term(self, tree):
#         return reduce(lambda x, y: x * y, tree)

#     def factor(self, tree):
#         return tree[0]

#     def number(self, tree):
#         return int(tree[0])


# G = """
# expr  : term [ "+" expr ]
# term  : factor [ "*" term ]
# factor : number | "(" expr ")"
# number : /[0-9]+/
# """

# text = "(1+5)*3+2"
# parser = Lark(G, start="expr")
# tree = parser.parse(text)
# print(tree)
# result = CalcTransformer().transform(tree)
# print(result)
