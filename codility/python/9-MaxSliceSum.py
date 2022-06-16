def solution(A):
    max_slice = max_ending = 0
    for a in A:
        max_ending = max(0, max_ending + a)
        max_slice = max(max_slice, max_ending)
    if max_slice == 0:
        return max(A)
    else:
        return max_slice

