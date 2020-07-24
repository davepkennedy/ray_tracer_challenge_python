from .shape import Shape
from .bounding_box import BoundingBox
from .tuple import Point, Vector
from .intersections import Intersection, Intersections

from .linmath import EPSILON, POSITIVE_INFINITY, NEGATIVE_INFINITY

class Cube(Shape):
    def __init__(self):
        super().__init__()
        
    def bounds(self):
        return BoundingBox(
            Point(-1, -1, -1),
            Point(1, 1, 1))

    def check_axis(self, origin, direction):
        tmin_numerator = (-1 - origin)
        tmax_numerator = (1 - origin)
        
        if abs(direction) >= EPSILON:
            tmin = tmin_numerator / direction
            tmax = tmax_numerator / direction
        else:
            tmin = tmin_numerator * POSITIVE_INFINITY
            tmax = tmax_numerator * POSITIVE_INFINITY
            
        return (tmax, tmin) if tmin > tmax else (tmin, tmax)
        

    def intersects_int(self, r):
        xtmin, xtmax = self.check_axis(r.origin.x, r.direction.x)
        ytmin, ytmax = self.check_axis(r.origin.y, r.direction.y)
        ztmin, ztmax = self.check_axis(r.origin.z, r.direction.z)
        
        tmin = max(xtmin, ytmin, ztmin)
        tmax = min(xtmax, ytmax, ztmax)

        return Intersections() if (tmin > tmax) else Intersections(
            Intersection(tmin, self),
            Intersection(tmax, self))
        

    def local_normal_at(self, pt, i):
        maxc = max(map(abs, pt))
        
        if maxc == abs(pt.x):
            return Vector(pt.x, 0, 0)
        elif maxc == abs(pt.y):
            return Vector(0, pt.y, 0)
        return Vector(0, 0, pt.z)
        
    