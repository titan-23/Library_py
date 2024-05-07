import sys
from time import process_time
from math import exp
from typing import Tuple, TypeVar
from titan_pylib.algorithm.random.random import Random


class State:

    def __init__(self) -> None:
        pass

    def copy(self) -> "State":
        pass


class SA:

    Changed = TypeVar("Changed")

    def __init__(self):
        self.random = Random()

    def make_ans_init(self) -> Tuple[State, int]:
        return

    def modify(self, state: State) -> Tuple[int, Changed]:
        # state は変更される
        return

    def rollback(self, state: State, changed: Changed) -> None:
        return

    def sovle(
        self, START_TEMP: float = 100, END_TEMP: float = 10, TIME_LIMIT: float = 1.8
    ) -> Tuple[State, int]:
        START_TIME = process_time()
        random = self.random
        ans, score = self.make_ans_init()
        vest_ans = ans.copy()
        vest_score = score
        cnt = 0
        while True:
            now_time = process_time() - START_TIME
            if now_time > TIME_LIMIT:
                break
            cnt += 1
            diff_score, changed = self.modify(ans)
            new_score = score + diff_score
            temp = START_TEMP + (END_TEMP - START_TEMP) * now_time / TIME_LIMIT
            arg = new_score - score
            if arg >= 1 or exp(arg / temp) > random.random():
                score = new_score
                if new_score > vest_score:
                    vest_score = new_score
                    vest_ans = ans.copy()
            else:
                self.rollback(ans, changed)
        print(f"{cnt=}", file=sys.stderr)
        return vest_ans, vest_score
