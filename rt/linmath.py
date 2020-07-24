EPSILON = 0.0001
POSITIVE_INFINITY = float('inf')
NEGATIVE_INFINITY = float('-inf')

def approx_eq(a,b):
    return abs(a-b) < EPSILON