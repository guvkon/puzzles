def arrayF(n):
    F = [0] * (n + 1)
    i = 2
    while i * i <= n:
        if F[i] == 0:
            k = i * i
            while k <= n:
                if F[k] == 0:
                    F[k] = i
                k += i
        i += 1
    return F

def factorization(n, F):
    factors = []
    while F[n] > 0:
        factors.append(F[n])
        n //= F[n]
    factors.append(n)
    return factors

def is_semiprime(n, F):
    return len(factorization(n, F)) == 2

def get_semiprimes(n, F):
    semiprimes = [False] * (n + 1)
    for i in range(4, n + 1):
        if is_semiprime(i, F):
            semiprimes[i] = True
    return semiprimes

def solution(N, P, Q):
    F = arrayF(N)
    semiprimes = get_semiprimes(N, F)
    m = len(P)
    answers = [0] * m
    for i in range(m):
        for k in range(P[i], Q[i] + 1):
            if semiprimes[k]:
                answers[i] += 1
    return answers

