# from titan_pylib.algorithm.parser import Parser
class Parser():

  '''Parser
  expression: < 四則演算の式 > ::= < 乗算除算の式 > (+ or -) < 乗算除算の式 > (+ or -) ...
  term      : < 乗算除算の式 > ::= < 括弧か数 > (* or /) < 括弧か数 > (* or /) ...
  term2 など

  factor    : < 括弧か数 >     ::= '(' < 四則演算の式 > ')' or < 数 >
  number    : < 数 >          ::= ...
  '''

  def __init__(self, s: str):
    self.s = s
    self.n = len(s)
    self.ptr = 0

  def parse(self):
    return self.expression()

  # 四則演算の式をパースして、その評価結果を返す。
  def expression(self):
    ret = self.term()
    while self.ptr < self.n:
      if self.get_char() == '+':
        self.consume('+')
        ret += self.term()
      elif self.get_char() == '-':
        self.consume('-')
        ret -= self.term()
      else:
        break
    return ret

  # 乗算除算の式をパースして、その評価結果を返す。
  def term(self):
    ret = self.factor()
    while self.ptr < self.n:
      if self.get_char() == '*':
        self.consume('*')
        ret *= self.factor()
      elif self.get_char() == '/':
        self.consume('/')
        ret = ret // self.factor()  # 切り捨て
      else:
        break
    return ret

  # 括弧か数をパースして、その評価結果を返す。
  def factor(self):
    if self.ptr >= self.n:
      return 0
    if self.get_char() == '(':
      self.consume('(')
      ret = self.expression()
      self.consume(')')
      return ret
    else:
      return self.number()

  # 数字の列をパースして、その数を返す。
  def number(self) -> int:
    ret = 0
    while self.ptr < self.n and self.get_char().isdigit():
      ret *= 10
      ret += int(self.get_char())
      self.ptr += 1
    return ret

  # begin が expected を指していたら begin を一つ進める。
  def consume(self, expected: str) -> None:
    assert self.s[self.ptr] == expected, \
        f'Expected: {expected} but got {self.s[self.ptr]}, s={self.s}'
    self.ptr += 1

  def get_char(self):
    return self.s[self.ptr]


