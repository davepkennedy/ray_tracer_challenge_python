from .shape import Shape
from .linmath import POSITIVE_INFINITY, NEGATIVE_INFINITY, EPSILON
from .intersections import Intersection, Intersections
from .tuple import Point, Vector
from .bounding_box import BoundingBox

import math

class Cone (Shape):
    __slots__ = [
        'minimum',
        'maximum',
        'closed'
    ]
    

    def __init__(self):
        super().__init__()

        self.minimum = NEGATIVE_INFINITY
        self.maximum = POSITIVE_INFINITY

        self.closed = False
        
    def __eq__ (self, obj):
        if obj is self:
            return True

        return super().__eq__(obj) and \
            self.minimum == obj.minimum and \
            self.maximum == obj.maximum and \
            self.closed == obj.closed

    def bounds(self):
        limit = max(abs(self.minimum), abs(self.maximum))
        return BoundingBox(
            Point(-limit, self.minimum, -limit),
            Point(limit, self.maximum, limit))
            
        
    def intersects_int(self, r):
        a = (r.direction.x * r.direction.x) - \
            (r.direction.y * r.direction.y) + \
            (r.direction.z * r.direction.z)
        
        b = 2 * r.origin.x * r.direction.x - \
            2 * r.origin.y * r.direction.y + \
            2 * r.origin.z * r.direction.z
            
        c = (r.origin.x * r.origin.x) - \
            (r.origin.y * r.origin.y) + \
            (r.origin.z * r.origin.z)
            
        disc = (b * b) - 4 * a * c
        
        if disc < 0:
            return Intersections()
            
        if a == 0:
            ts = [-c / (2 * b)]
        else:
            t0 = (-b - math.sqrt(disc)) / (2 * a)
            t1 = (-b + math.sqrt(disc)) / (2 * a)
            
            if t0 > t1:
                t0, t1 = t1, t0
            
            ts = [t0, t1]
            
        xs = Intersections()
        for t in ts:
            y = r.origin.y + t * r.direction.y
            if self.minimum < y and y < self.maximum:                
                xs.add(Intersection(t, self))

        self.intersect_caps(r, xs)
        return xs
        
    def intersect_caps(self, r, xs):
        if not self.closed or abs(r.direction.y) < EPSILON:
            return
            
        for v in  [self.minimum, self.maximum]:
            t = (v - r.origin.y) / r.direction.y
            
            if self.check_cap(r, t, abs(v)):
                xs.add(Intersection(t, self))
    
    def check_cap(self, r, t, radius):
        x = r.origin.x + t * r.direction.x
        z = r.origin.z + t * r.direction.z
        
        return (x * x + z * z) <= radius
        
    def local_normal_at(self, pt, i):
        dist = (pt.x * pt.x) + (pt.z * pt.z)
        if dist < 1 and pt.y >= (self.maximum - EPSILON):
            return  Vector(0, 1, 0)
            
        if dist < 1 and pt.y <= self.minimum + EPSILON:
            return  Vector(0, -1, 0)
            
        y = math.sqrt(pt.x * pt.x + pt.z * pt.z)
        if pt.y > 0:
            y = -y
            
        return  Vector(pt.x, y, pt.z)
        
    