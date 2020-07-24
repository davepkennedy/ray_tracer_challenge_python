from .matrix import Identity
from .shape import Shape
from .tuple import Point
from .bounding_box import BoundingBox

from .intersections import Intersection, Intersections

import math

class Sphere (Shape):

    def __init__(self):
        super().__init__()

    def local_normal_at(self, pt, i):
        return pt - Point(0, 0, 0)
        
    def intersects_int(self, ray):
        sphere_to_ray = ray.origin - Point(0, 0, 0)
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        
        discriminant = (b * b) - 4 * a * c
        
        if discriminant < 0:
            return Intersections()
            
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        
        
        return Intersections( 
            Intersection(t1, self),
            Intersection(t2, self) 
        )

    def bounds (self):
        return BoundingBox(Point(-1, -1, -1), Point(1, 1, 1))

    @staticmethod
    def glass ():
        s = Sphere()
        s.material.transparency = 1
        s.material.refractive_index = 1.5
        return s
