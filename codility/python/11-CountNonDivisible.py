def solution(A):
    n = len(A)
    answers = [0] * n
    for i in range(n):
        for j in range(n):
            if i != j and A[i] % A[j] != 0:
                answers[i] += 1
    return answers

