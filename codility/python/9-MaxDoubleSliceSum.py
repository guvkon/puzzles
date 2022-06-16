def prefix_sums(A):
    n = len(A)
    P = [0] * (n + 1)
    for k in range(1, n + 1):
        P[k] = P[k - 1] + A[k - 1]
    return P


def solution(A):
    max_slice = -30000
    n = len(A)
    pref = prefix_sums(A)
    for x in range(0, n - 2):
        for y in range(x + 1, n - 1):
            for z in range(y + 1, n):
                slice = pref[z] - pref[x + 1] - A[y]
                max_slice = max(max_slice, slice)
    return max_slice
