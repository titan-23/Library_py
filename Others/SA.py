from time import time
from copy import deepcopy
import random
from math import exp
from typing import Tuple

random.seed(0)

class State():

  def __init__(self):
    pass

  def copy(self) -> 'State':
    pass

  def 

class SA():

  def __init__(self):
    self.END_TEMP = 10
    self.START_TEMP = 100

  def make_ans_init(self) -> Tuple:
    return

  def modify(self, ans: State) -> Tuple:
    return

  def rollback(self, ans: State, changed) -> None:
    return

  def sovle(self, TIME_LIMIT=1.8) -> Tuple:
    START_TIME = time()
    START_TEMP, END_TEMP = self.START_TEMP, self.END_TEMP
    ans, score = self.make_ans_init()
    vest_ans = deepcopy(ans)
    vest_score = score
    cnt = 0
    while True:
      now_time = time() - START_TIME
      if now_time > TIME_LIMIT: break
      cnt += 1
      diff_score, changed = self.modify(ans)
      new_score = score + diff_score
      temp = START_TEMP + (END_TEMP - START_TEMP) * now_time / TIME_LIMIT
      arg = new_score - score
      if 1 if arg >= 1 else exp(arg/temp) > random.random():
        score = new_score
        if new_score > vest_score:
          vest_score = new_score
          vest_ans = deepcopy(ans)
      else:
        self.rollback(ans, changed)
    return vest_ans, vest_score, cnt
