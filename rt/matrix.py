import math
from operator import mul

from .tuple import Tuple
from .linmath import approx_eq

def Identity (size=4):
    return Matrix(*[1 if i % size == int(i / size) else 0 for i in range(size*size)])


class Matrix:
    __slots__ = ['m', 'size']
    def __init__ (self, *elems):
        size = math.sqrt(len(elems))
        self.size = round(size)
        if size - self.size > 0:
            raise ValueError(f"The matrix needs to be square; size = {len(elems)}")
        self.m = [float(e) for e in elems]

    def __repr__(self):
        return f"Matrix({','.join(map(str, self.m))}"
        
    def __eq__ (self, other):
        if not isinstance(other, Matrix):
            return False
        if self.size != other.size:
            return False

        neq = list(
            filter(
                lambda x: not x, map(
                    lambda x: approx_eq(x[0], x[1]), zip(self.m, other.m))))
        return len(neq) == 0

    def __getitem__(self ,key):
        x,y = key
        return self.m[x * self.size + y]

    def __setitem__ (self, key, value):
        x,y = key
        self.m[x * self.size + y] = value

    def __mul__ (self, other):
        if isinstance(other, Matrix) and other.size == self.size:
            a = [self.m[i*self.size:i*self.size+self.size] for i in range(self.size)]
            b = [other.transpose().m[i*self.size:i*self.size+self.size] for i in range(self.size)]
            return Matrix(*[sum(map(mul, aa, bb)) for aa in a for bb in b ])

        elif isinstance(other, tuple) and len(other) == self.size:
            return tuple(sum(map(mul,self.m[i*self.size:i*self.size+self.size],other)) for i in range(self.size))
        elif isinstance(other, int) or isinstance(other, float):
            return Matrix(*list(map(lambda x: x*other, self.m)))

        elif isinstance(other, Tuple):
            return Tuple(*(self * tuple(other)))

        raise ValueError(f"Other needs to be a matrix or tuple of the same size, or a number ({type(other)})")

    def transpose(self):
        return Matrix(*[self.m[j*4+i] 
            for i in range(self.size) 
            for j in range(self.size)])

    def determinant(self):
        if self.size == 2:
            return (self.m[0] * self.m[3]) - (self.m[1] * self.m[2])
        
        return sum([self[(0, col)] * self.cofactor(0, col) for col in range(self.size)])
        

    def submatrix(self, row, col):
        return Matrix(* [val for idx, val in enumerate(self.m) if (idx % self.size) != col and int(idx / self.size) != row])

    def minor(self, row, col):
        return self.submatrix(row, col).determinant()

    def cofactor(self, row, col):
        return self.minor(row, col) * (-1 if (row + col) % 2 == 1 else 1)

    @property
    def is_invertible(self):
        return 0 != self.determinant()


    def inverse(self):
        m = Matrix(*[self.cofactor(x, y) for y in range(self.size) for x in range(self.size)])
        d = self.determinant()
        return m * (1/d)