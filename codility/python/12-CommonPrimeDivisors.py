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

def get_factors(x):
    F = arrayF(x)
    primeFactors = {}
    while F[x] > 0:
        primeFactors[F[x]] = True
        x //= F[x]
    primeFactors[x] = True
    return primeFactors

def solution(A, B):
    result = 0
    for k in range(len(A)):
        A_factors = get_factors(A[k])
        B_factors = get_factors(B[k])
        if A_factors == B_factors:
            result += 1
    return result

