from sys import setrecursionlimit

setrecursionlimit(3200)

lookup = {}


def solution(n):
    n = int(n)
    if n == 1:
        lookup[1] = 0
        return 0
    val = lookup.get(n)
    if val:
        return val
    if n % 2 == 0:
        res = 1 + solution(n // 2)
        lookup[n] = res
        return res
    plus = 1 + solution(n + 1)
    minus = 1 + solution(n - 1)
    best = min(plus, minus)
    lookup[n] = best
    return best
