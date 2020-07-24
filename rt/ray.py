import math

from .intersections import Intersection, Intersections
from .tuple import Point, Vector


class Ray:
    __slots__ = ['origin', 'direction']

    def __init__ (self, origin, direction):
        self.origin = origin
        self.direction = direction

    def __repr__(self):
        return f"Ray({self.origin}, {self.direction})"

    def _intersects(self, shape):
        shape_to_ray = self.origin - Point(0, 0, 0)
        a = self.direction.dot(self.direction)
        b = 2 * self.direction.dot(shape_to_ray)
        c = shape_to_ray.dot(shape_to_ray) - 1
        
        discriminant = (b * b) - 4 * a * c
        if discriminant < 0:
            return Intersections()
                
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        
        return Intersections (
            Intersection(t1, shape),
            Intersection(t2, shape)
        )

    def position(self, t):
        return self.origin + self.direction * t

    def transform(self, matrix):
        return Ray(matrix * self.origin, matrix * self.direction)

    def intersects(self, shape):
        return self.transform(shape.transform.inverse())._intersects(shape)