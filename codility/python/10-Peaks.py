def get_peaks(A):
    peaks = []
    for p in range(1, len(A) - 1):
        if A[p - 1] < A[p] and A[p] > A[p + 1]:
            peaks.append(p)
    return peaks

def can_be_divided(n, num_blocks, peaks):
    block_len = n // num_blocks
    blocks = [0] * num_blocks
    for p in peaks:
        blocks[p // block_len] += 1
    for count in blocks:
        if count == 0:
            return False
    return True

def solution(A):
    peaks = get_peaks(A)
    peaks_num = len(peaks)
    if peaks_num == 0:
        return 0

    n = len(A)
    for num_blocks in range(peaks_num, 1, -1):
        if n % num_blocks == 0 and can_be_divided(n, num_blocks, peaks):
            return num_blocks
    return 1

