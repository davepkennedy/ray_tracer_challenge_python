from .shape import Shape
from .tuple import Point, Vector
from .bounding_box import BoundingBox
from .intersections import Intersection, Intersections
from .linmath import NEGATIVE_INFINITY, POSITIVE_INFINITY, EPSILON

class Plane (Shape):
     
    def bounds(self):
        return BoundingBox(
            Point(NEGATIVE_INFINITY, 0, NEGATIVE_INFINITY),
            Point(POSITIVE_INFINITY, 0, POSITIVE_INFINITY))
            
    def intersects_int(self, ray):
        if abs(ray.direction.y) < EPSILON:
            return Intersections()
            
        t = -ray.origin.y / ray.direction.y
        return Intersections(Intersection(t,self))
        
    def local_normal_at(self, pt, i):
        return Vector(0,1,0)