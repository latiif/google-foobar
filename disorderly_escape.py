from collections import Counter
from math import factorial
from fractions import gcd


def num_partitions(c, n):
    res = 1
    for number, times in Counter(c).items():
        res *= (number ** times) * factorial(times)
    return factorial(n) // res


def list_partitions(n, i=1):
    yield [n]
    for i in range(i, n // 2 + 1):
        for p in list_partitions(n - i, i):
            yield [i] + p


def solution(w, h, s):
    total = 0
    for ws in list_partitions(w):
        for hs in list_partitions(h):
            m = num_partitions(ws, w) * num_partitions(hs, h)
            total += m * (s ** sum([sum([gcd(i, j) for i in hs]) for j in ws]))
    res = total // (factorial(w) * factorial(h))
    return str(res)


print(solution(3, 3, 3))
