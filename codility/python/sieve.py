def sieve(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    i = 2
    while i * i <= n:
        if sieve[i]:
            k = i * i
            while k <= n:
                sieve[k] = False
                k += i
        i += 1
    return sieve

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

def factorization(x, F):
    primeFactors = []
    while F[x] > 0:
        primeFactors.append(F[x])
        x //= F[x]
    primeFactors.append(x)
    return primeFactors

