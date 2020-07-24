from .tuple import Tuple, Point
from .linmath import EPSILON, POSITIVE_INFINITY as POS_INF

import math

class BoundingBox:
    __slots__ = ['min', 'max']
    
    def __init__ (self, min=None, max=None):
        self.min = min or Point.MAX
        self.max = max or Point.MIN
    
    def bounds(self):
        return self     

    def __add__ (self, other):
        return BoundingBox().add(self).add(other)

    def add(self, val):
        if isinstance(val, Point):
            if (val.x < self.min.x): self.min = Point(val.x, self.min.y, self.min.z)
            if (val.x > self.max.x): self.max = Point(val.x, self.max.y, self.max.z)
        
            if (val.y < self.min.y): self.min = Point(self.min.x, val.y, self.min.z)
            if (val.y > self.max.y): self.max = Point(self.max.x, val.y, self.max.z)
        
            if (val.z < self.min.z): self.min = Point(self.min.x, self.min.y, val.z)
            if (val.z > self.max.z): self.max = Point(self.max.x, self.max.y, val.z)
        elif isinstance(val, BoundingBox):
            self.add(val.min)
            self.add(val.max)
        return self

    def __contains__ (self, other):
        return self.contains(other)
        
    def contains(self, other):
        if isinstance(other, Tuple):
            contains_x = self.min.x <= other.x and other.x <= self.max.x
            contains_y = self.min.y <= other.y and other.y <= self.max.y
            contains_z = self.min.z <= other.z and other.z <= self.max.z
            return contains_x and contains_y and contains_z
        elif isinstance(other, BoundingBox):
            contains_min = self.contains(other.min)
            contains_max = self.contains(other.max)
            return contains_min and contains_max
        return False
        
    def transform(self, matrix):
        points = [
            self.min,
            Point(self.min.x, self.min.y, self.max.z),
            Point(self.min.x, self.max.y, self.min.z),
            Point(self.min.x, self.max.y, self.max.z),
            Point(self.max.x, self.min.y, self.min.z),
            Point(self.max.x, self.min.y, self.max.z),
            Point(self.max.x, self.max.y, self.min.z),
            self.max
        ]
        
        box = BoundingBox()
        for pt in points:
            box.add((matrix * pt).to_point())

        return box

    def check_axis(self, min, max, origin, direction):
        tmin_numerator = (min - origin)
        tmax_numerator = (max - origin)
        
        if abs(direction) >= EPSILON:
            tmin = tmin_numerator / direction
            tmax = tmax_numerator / direction
        else:
            tmin = tmin_numerator * POS_INF
            tmax = tmax_numerator * POS_INF
            
        if tmin > tmax:
             tmin, tmax=tmax, tmin
        return tmin, tmax
        
        
    def intersects(self, ray):
        xtmin, xtmax = self.check_axis(self.min.x, self.max.x, ray.origin.x, ray.direction.x)
        ytmin, ytmax = self.check_axis(self.min.y, self.max.y, ray.origin.y, ray.direction.y)
        ztmin, ztmax = self.check_axis(self.min.z, self.max.z, ray.origin.z, ray.direction.z)

        tmin = max(xtmin, ytmin, ztmin)
        tmax = min(xtmax, ytmax, ztmax)

        return False if tmin > tmax else True

    def split(self):
        # figure out the box's largest dimension
        dx = self.max.x - self.min.x
        dy = self.max.y - self.min.y
        dz = self.max.z - self.min.z

        greatest = max(dx, dy, dz)

        # variables to help construct the points on
        # the dividing plane
        x0 = self.min.x
        y0 = self.min.y
        z0 = self.min.z

        x1 = self.max.x
        y1 = self.max.y
        z1 = self.max.z

        # adjust the points so that they lie on the
        # dividing plane
        if greatest == dx:
            x0 = x1 = x0 + dx / 2.0
        elif greatest == dy:
            y0 = y1 = y0 + dy / 2.0
        else:
            z0 = z1 = z0 + dz / 2.0
            
        mid_min = Point(x0, y0, z0)
        mid_max = Point(x1, y1, z1)

        # construct and return the two halves of
        # the bounding box
        return BoundingBox(self.min, mid_max), BoundingBox(mid_min, self.max)