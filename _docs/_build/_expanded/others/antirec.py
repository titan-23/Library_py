# from titan_pylib.others.antirec import antirec
from types import GeneratorType

# ref: https://github.com/cheran-senthil/PyRival/blob/master/pyrival/misc/bootstrap.py
# ref: https://twitter.com/onakasuita_py/status/1731535542305907041


def antirec(func):
    stack = []

    def wrappedfunc(*args, **kwargs):
        if stack:
            return func(*args, **kwargs)
        to = func(*args, **kwargs)
        while True:
            if isinstance(to, GeneratorType):
                stack.append(to)
                to = next(to)
            else:
                stack.pop()
                if not stack:
                    break
                to = stack[-1].send(to)
        return to

    return wrappedfunc


def antirec_cache(func):
    stack = []
    memo = {}
    args_list = []

    def wrappedfunc(*args):
        args_list.append(args)
        if stack:
            return func(*args)
        to = func(*args)
        while True:
            if args_list[-1] in memo:
                res = memo[args_list.pop()]
                if not stack:
                    return res
                to = stack[-1].send(res)
                continue
            if isinstance(to, GeneratorType):
                stack.append(to)
                to = next(to)
            else:
                memo[args_list.pop()] = to
                stack.pop()
                if not stack:
                    break
                to = stack[-1].send(to)
        return to

    return wrappedfunc
