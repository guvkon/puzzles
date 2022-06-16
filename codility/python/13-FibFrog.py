def fib(limit):
    fib = [0]
    fib.append(1)
    while fib[-1] < limit:
        fib.append(fib[-1] + fib[-2])
    fib.pop()
    return fib

def get_jumps(limit):
    jumps = fib(limit)
    jumps.reverse()
    jumps.pop()
    jumps.pop()
    return jumps

def solution(A):
    N = len(A)
    jumps = get_jumps(N)
    position = -1
    A.append(1)
    jumps_made = 0
    while position < N:
        for jump in jumps:
            if position + jump <= N and A[position + jump] == 1:
                position += jump
                jumps_made += 1
                break
    return jumps_made

