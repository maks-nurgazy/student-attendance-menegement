import math



def square(s):
    p = 4 * s
    a = s * s
    d = int(math.sqrt(2) * s)
    return (p, a, d)


s = int(input())
p, a, d = square(s)
print("{},{},{}".format(p, a, d))
