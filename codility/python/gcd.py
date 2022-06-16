def gcd_sub(a, b):
    if a == b:
        return a
    if a > b:
        return gcd_sub(a - b, b)
    else:
        return gcd_sub(a, b - a)

def gcd_div(a, b):
    if a % b == 0:
        return b
    else:
        return gcd_div(b, a % b)

def gcd_bin(a, b, res = 1):
    if a == b:
        return res * a
    elif a % 2 == 0 and b % 2 == 0:
        return gcd_bin(a // 2, b // 2, 2 * res)
    elif a % 2 == 0:
        return gcd_bin(a // 2, b, res)
    elif b % 2 == 0:
        return gcd_bin(a, b // 2, res)
    elif a > b:
        return gcd_bin(a - b, b, res)
    else:
        return gcd_bin(a, b - a, res)

def lcm(a, b):
    return a * b / gcd_bin(a, b)

