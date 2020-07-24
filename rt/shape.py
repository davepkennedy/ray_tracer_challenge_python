from .matrix import Identity
from .material import Material
from .tuple import Vector

class Shape:
    __slots__ = [
        'transform',
        'material', 
        'parent', 
        'bounding_box',
        'hit'
    ]

    def __eq__ (self, obj):
        if obj is self:
            return True

        # return isinstance(obj, Shape) and \
        return type(self) == type(obj) and \
            self.transform == obj.transform and \
            self.material == obj.material

    def __init__(self):
        self.hit = False
        self.parent = None
        self.transform = Identity()
        self.material = Material()

    def __iter__ (self):
        return self

    def bounds (self):
        return None

    def parent_space_bounds(self):
        b = self.bounds()
        return b.transform(self.transform)

    @property
    def has_parent(self):
        return self.parent != None
            
    def normal_at(self, pt, i):
        local_point = self.world_to_object(pt)
        local_normal = self.local_normal_at(local_point, i)
        return self.normal_to_world(local_normal)
        
    def world_to_object(self, pt):
        if self.has_parent:
            pt = self.parent.world_to_object(pt)
        return self.transform.inverse() * pt

    def normal_to_world (self, normal):
        normal = self.transform.inverse().transpose() * normal
        normal = Vector(normal.x, normal.y, normal.z)
        normal = normal.normalize()
        
        if self.has_parent:
            normal = self.parent.normal_to_world(normal)
        
        return normal

    def intersects(self, ray):
        r = ray.transform(self.transform.inverse())
        intersections = self.intersects_int(r)
        if len(intersections) > 0:
            self.hit = True
        return intersections
        
    def check_hits(self):
        if not self.hit:
            print(f"{self} had no hits")

    def __contains__ (self, other):
        return self == other
        
    def contains(self, other):
        return other in self

    def divide(self, n):
        pass