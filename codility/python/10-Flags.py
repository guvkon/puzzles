def get_peaks(A):
    peaks = []
    N = len(A)
    for p in range(1, N - 1):
        if A[p - 1] < A[p] and A[p] > A[p + 1]:
            peaks.append(p)
    return peaks

def get_initial_max_flags(peaks):
    peaks_num = len(peaks)
    min_distance = peaks[1] - peaks[0]
    for p in range(1, peaks_num - 1):
        dist = peaks[p + 1] - peaks[p]
        min_distance = min(min_distance, dist)
    return min(min_distance, peaks_num)

def get_planted_flags(peaks, flags_num):
    planted_flags = 1
    last_planted = peaks[0]
    for p in range(1, len(peaks)):
        if peaks[p] - last_planted >= flags_num:
            planted_flags += 1
            last_planted = peaks[p]
    return planted_flags

def solution(A):
    peaks = get_peaks(A)
    peaks_num = len(peaks)
    if peaks_num < 2:
        return peaks_num

    max_flags = get_initial_max_flags(peaks)
    flags_num = peaks_num
    while flags_num > max_flags:
        planted_flags = get_planted_flags(peaks, flags_num)
        max_flags = max(max_flags, planted_flags)
        flags_num -= 1
    return max_flags

