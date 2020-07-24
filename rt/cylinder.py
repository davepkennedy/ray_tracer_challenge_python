from .shape import Shape
from .bounding_box import BoundingBox
from .tuple import Point, Vector
from .linmath import EPSILON, NEGATIVE_INFINITY, POSITIVE_INFINITY
from .intersections import Intersection, Intersections

import math

class Cylinder(Shape):
    __slots__ = ['minimum', 'maximum','closed']

    def __init__(self):
        super().__init__()
        self.minimum = NEGATIVE_INFINITY
        self.maximum = POSITIVE_INFINITY
        self.closed = False

    def __eq__ (self, obj):
        if obj is self:
            return True
        return super().__eq__(self, obj) and \
            self.minimum == obj.minimum and \
            self.maximum == obj.maximum and \
            self.closed == obj.closed

    def bounds(self):
        return BoundingBox(Point(-1, self.minimum, -1), Point(1, self.maximum, 1))

    def intersects_int(self, r):
        a = (r.direction.x * r.direction.x) + (r.direction.z * r.direction.z)
        print (f"a {a}")
        
        b = 2 * r.origin.x * r.direction.x + 2 * r.origin.z * r.direction.z

        c = (r.origin.x * r.origin.x) + (r.origin.z * r.origin.z) - 1

        disc = (b * b) - 4 * a * c
        print (f"disc {disc}")
        if disc < 0:
            return Intersections()
            
        t0 = float('nan') if a == 0 else (-b - math.sqrt(disc)) / (2 * a)
        t1 = float('nan') if a == 0 else (-b + math.sqrt(disc)) / (2 * a)

        if t0 > t1:
            t1, t0 = t0, t1

        xs = Intersections()
        y0 = r.origin.y + t0 * r.direction.y
        if self.minimum < y0 and y0 < self.maximum:
            xs.add(Intersection(t0, self))
            
        y1 = r.origin.y + t1 * r.direction.y
        if self.minimum < y1 and y1 < self.maximum:
            xs.add(Intersection(t1, self))
            
        self.intersect_caps(r, xs)
        return xs
        
    def intersect_caps (self, r, xs):
        if not self.closed or abs(r.direction.y) < EPSILON:
            return

        for v in [self.minimum, self.maximum]:
            t = (v - r.origin.y) / r.direction.y
            if self.check_cap(r, t):
                xs.add(Intersection(t, self))

    def check_cap (self, r, t):
        x = r.origin.x + t * r.direction.x
        z = r.origin.z + t * r.direction.z
        return (x * x + z * z) <= 1

    def local_normal_at(self, pt, i):
        dist = (pt.x * pt.x) + (pt.z * pt.z)
        if dist < 1 and pt.y >= (self.maximum - EPSILON):
            return Vector(0, 1, 0)
        if dist < 1 and pt.y <= self.minimum + EPSILON:
            return Vector(0, -1, 0)
            
        return Vector(pt.x, 0, pt.z)