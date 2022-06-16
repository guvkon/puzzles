import math

def solution(A, B):
    maxA = max(A)
    fib = [1] * (maxA + 1)
    for i in range(2, maxA + 1):
        fib[i] = fib[i - 1] + fib[i - 2]

    n = len(A)
    answers = [0] * n
    for i in range(n):
        answers[i] = fib[A[i]] % int(math.pow(2, B[i]))
    return answers

