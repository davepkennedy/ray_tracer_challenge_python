from .shape import Shape
from .bounding_box import BoundingBox
from .intersections import Intersections

class Group (Shape):
    __slots__ = ['shapes']
    
    def __init__(self, *args):
        super().__init__()
        self.shapes = list(args)
        for shape in self.shapes:
            shape.parent = self
            
    def intersects_int(self, r):
        if self.bounds().intersects(r):
            hits = []
            for shape in self.shapes:
                xs = shape.intersects(r)
                for i in xs:
                    if not i in hits:
                        hits.append(i)
            
            return Intersections(*sorted(hits, key=lambda x: x.t))
        return Intersections()
        
    def local_normal_at(self, pt, i):
        raise NotImplementedError
    
    def __len__(self):
        return len(self.shapes)
        
    def bounds(self):
        box = BoundingBox()
        for shape in self.shapes:
            box.add(shape.parent_space_bounds())
        return box

    def add(self, s):
        self.shapes.append(s)
        s.parent = self

    def contains(self, s):
        return s in self
    
    def __contains__ (self, s):
        return s in self.shapes
        
    def __getitem__ (self, idx):
        return self.shapes[idx]

    def partition_children(self):
        left_list = []
        right_list = []
        
        to_remove = []
        
        left, right = self.bounds().split()
        for shape in self.shapes:
            shape_parent_bounds = shape.parent_space_bounds()
            if left.contains(shape_parent_bounds):
                left_list.append(shape)
                to_remove.append(shape)
            if right.contains(shape_parent_bounds):
                right_list.append(shape)
                to_remove.append(shape)
                
        for s in to_remove:
            self.shapes.remove(s)

        return left_list, right_list
        
    def make_subgroup (self, *args):
        self.add(Group(*args))

    def divide(self, threshold):
        if threshold <= len(self):
            left, right = self.partition_children()
            if len(left):
                self.make_subgroup(*left)
            if len(right):
                self.make_subgroup(*right)
                
        for s in self.shapes:
            if hasattr(s, 'divide'):
                s.divide(threshold)

    def __eq__ (self, other):
        return isinstance(other, Group) and \
            _compare_shapes(self.shapes, other.shapes) and \
            len(self) == len(other)
            
    def __repr__(self):
        return f"Group({self.shapes})"
        

    def check_hits(self):
        for s in self.shapes:
            s.check_hits()


def _compare_shapes (first, second):
    first_not_second = list(filter(lambda x: x not in first, second))
    second_not_first = list(filter(lambda x: x not in second, first))
    return not bool (first_not_second or second_not_first)


def _hexagon_corner():
    sphere = Sphere()
    sphere = t.ransform = translation(0, 0, -1) * scaling(0.25, 0.25, 0.25)
    
def _hexagon_Edge():
    cylinder = Cylinder()
    cylinder.minimum = 0
    cylinder.maximum = 1
    cylinder.transform = translation(0, 0, -1) * \
        rotation_y(-Math.PI / 6) * \
        rotation_z(-Math.PI / 2) * \
        scaling(0.25, 1, 0.25)

def _hexagon_side():
    side = Group()
    side.add(_hexagon_corner())
    side.add(_hexagon_edge())
    return side
    
def hexagon():
    hex = Group()
    for i in range(6):
        side = _hexagon_side()
        side.transform = rotation_y(i * math.pi / 3)
        hex.add(side)
    return hex;