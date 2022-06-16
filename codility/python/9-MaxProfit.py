def solution(A):
    if len(A) == 0:
        return 0

    profit = 0
    minValue = A[0]
    for a in A:
        minValue = min(minValue, a)
        profit = max(profit, a - minValue)
    return profit

