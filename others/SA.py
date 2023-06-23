from time import time
from copy import deepcopy
import random
from math import exp
from typing import Tuple

random.seed(0)

START_TIME = time()
TIME_LIMIT = 1.8
END_TEMP = 10
START_TEMP = 100

def make_ans_init() -> Tuple:
  return

def modify(ans) -> Tuple:
  return

def rollback(ans, changed) -> None:
  return

def SA_solver() -> Tuple:
  ans, score = make_ans_init()
  vest_ans = deepcopy(ans)
  vest_score = score
  cnt = 0
  while True:
    now_time = time() - START_TIME
    if now_time > TIME_LIMIT: break
    cnt += 1
    diff_score, changed = modify(ans)
    new_score = score + diff_score
    temp = START_TEMP + (END_TEMP - START_TEMP) * now_time / TIME_LIMIT
    arg = new_score - score
    if 1 if arg >= 1 else exp(arg/temp) > random.random():
      score = new_score
      if new_score > vest_score:
        vest_score = new_score
        vest_ans = deepcopy(ans)
    else:
      rollback(ans, changed)
  return vest_ans, vest_score, cnt
