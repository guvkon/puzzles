def solution(N):
    min_perimeter = 2 * (N + 1)
    i = 2
    while i * i < N:
        if N % i == 0:
            perimeter = 2 * (i + N // i)
            min_perimeter = min(min_perimeter, perimeter)
        i += 1
    if i * i == N:
        perimeter = 4 * i
        min_perimeter = min(min_perimeter, perimeter)
    return min_perimeter

