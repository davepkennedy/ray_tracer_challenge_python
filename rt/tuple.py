from .linmath import approx_eq, POSITIVE_INFINITY as POS_INF, NEGATIVE_INFINITY as NEG_INF
import math

from operator import add, neg, mul

class __TupleMeta(type):
    @property
    def MIN(self):
        return self(NEG_INF,NEG_INF,NEG_INF)

    @property
    def MAX(self):
        return self(POS_INF,POS_INF,POS_INF)

class Tuple(metaclass=__TupleMeta):
    __slots__ = ['__arr']

    def __init__ (self, *args):
        assert len(args) == 4
        self.__arr = list(args)

    def __str__ (self):
        return f"Tuple({self.__arr})"

    def __repr__ (self):
        return str(self)

    def __eq__ (self, other):
        
        if isinstance(other, Tuple):
            a = other.__arr
        elif isinstance(other, tuple):
            a = other
        else:
            raise ValueError("Tuple.__eq__ is valid only for rt.Tuple or Python tuple")

        return 0 != len(list(filter(lambda x: x, map(approx_eq, self.__arr,a))))


    def __mul__ (self, other):
        if isinstance(other, Tuple):
            return Tuple(map(mul, self.__arr, other.__arr))
        elif isinstance(other, int) or isinstance(other, float):
            return Tuple(*map(lambda x: x*other, self.__arr))

    def __iter__ (self):
        for i in self.__arr:
            yield i

    def __truediv__ (self, other):
        return self * (1.0/other)

    def __add__ (self, other):
        return Tuple(*map(add, self.__arr, other.__arr))

    def __neg__ (self):
        return Tuple(*map(neg, self.__arr))

    def __sub__ (self, other):
        return self + (-other)

    @property
    def x(self):
        return self.__arr[0]
        
    @property
    def y(self):
        return self.__arr[1]
        
    @property
    def z(self):
        return self.__arr[2]
        
    @property
    def w(self):
        return self.__arr[3]

    @w.setter
    def w(self,value):
        self.__arr[3] = value

    @property
    def is_point(self):
        return self.w == 1

    @property
    def is_vector(self):
        return self.w == 0

    def magnitude(self):
        return math.sqrt(sum(map(mul, self.__arr, self.__arr)))

    def normalize(self):
        m = self.magnitude()
        return self / m
    

    def dot(self, other): 
        return sum(map(mul, self.__arr, other.__arr))

    def cross(self, other):
	    return Vector (
		    self.y * other.z - self.z * other.y,
		    self.z * other.x - self.x * other.z,
		    self.x * other.y - self.y * other.x,
	    )

    def reflect_on(self, normal):
        return self - normal * 2 * self.dot(normal)

    def to_point(self):
        return Point(self.x, self.y, self.z)

    def to_vector(self):
        return Vector(self.x, self.y, self.z)

class Point (Tuple):
    def __init__ (self, x, y, z):
        super().__init__(x, y, z, 1)

class Vector (Tuple):
    def __init__ (self, x, y, z):
        super().__init__(x, y, z, 0)