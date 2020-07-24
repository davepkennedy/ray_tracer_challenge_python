from .shape import Shape
from .intersections import Intersection, Intersections
from .bounding_box import BoundingBox
from .linmath import EPSILON

class Triangle(Shape):
    __slots__ = ['p1','p2','p3','e1','e2','normal']
    
    def __init__ (self, p1, p2, p3):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        
        self.e1 = (p2 - p1).to_vector()
        self.e2 = (p3 - p1).to_vector()
        
        self.normal = self.e2.cross(self.e1).normalize().to_vector()    

    def __repr__ (self):
        return f"Triangle({self.p1},{self.p2},{self.p3})"

    def bounds(self):
        bounds = BoundingBox()
        bounds.add(self.p1)
        bounds.add(self.p2)
        bounds.add(self.p3)
        return bounds

    def local_normal_at(self, pt, i):
        return self.normal
        
    def intersects_int(self, r):
        dir_cross_e2 = r.direction.cross(self.e2)
        det = self.e1.dot(dir_cross_e2)
        if abs(det) < EPSILON:
            return Intersections()
            
        f = 1.0 / det
        p1_to_origin = r.origin - self.p1
        u = f * p1_to_origin.dot(dir_cross_e2)
        if u < 0 or u > 1:
            return Intersections()
            
        origin_cross_e1 = p1_to_origin.cross(self.e1)
        v = f * r.direction.dot(origin_cross_e1)
        if v < 0 or (u+v) > 1:
            return Intersections()
            
        t = f * self.e2.dot(origin_cross_e1)
        return Intersections(
                Intersection(t, self, u, v))