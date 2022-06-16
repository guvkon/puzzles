import math

def fib(n):
    fib = [0] * (n + 1)
    fib[1] = 1
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
    return fib[n]

def fib_formula(n):
    return int((math.pow((1 + math.sqrt(5)) / 2, n) - math.pow((1 - math.sqrt(5)) / 2, n)) / math.sqrt(5))

