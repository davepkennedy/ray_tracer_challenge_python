from .shape import Shape
from .bounding_box import BoundingBox
from .intersections import Intersection, Intersections

#public abstract class Operation
#    {
#        public static Operation UNION = new UnionOp();
#        public static Operation INTERSECTION = new IntersectionOp();
#        public static Operation DIFFERENCE = new DifferenceOp();
#        public abstract bool IntersectionAllowed(bool lhit, bool inl, bool inr);
#
#        public static Operation OfKind (string op)
#        {
#            switch (op)
#            {
#                case "union":
#                    return UNION;
#                case "intersection":
#                    return INTERSECTION;
#                case "difference":
#                    return DIFFERENCE; 
#            }
#            return null;
#        }
#    }

def union_operation(lhit, inl, inr):
    a = (lhit and not inr) 
    b = (not lhit and not inl)
    return a or b

def intersection_operation(lhit, inl, inr):
     a = (lhit and inr) 
     b = (not lhit and inl)
     return a or b
     
def difference_operation(lhit, inl, inr):
    a = (lhit and not inr) 
    b = (not lhit and inl)
    return a or b

def operation_from_string(s):
    ops = {
        'union': union_operation,
        'intersection': intersection_operation,
        'difference': difference_operation
    }
    if s in ops:
        return ops[s]
    return None

class CSG (Shape):
    __slots__ = ['operation', 'left', 'right']

    def bounds(self):
        #box = BoundingBox()
        print (repr(self))
        lpsb = self.left.parent_space_bounds()
        rpsb = self.right.parent_space_bounds()

        return lpsb + rpsb

        #box.add(self.left.parent_space_bounds())
        #box.add(self.right.parent_space_bounds())
        #return box

        
    def __init__ (self, operation, left, right):
        super().__init__()
        self.operation = operation
        self.left = left
        self.right = right

        self.left.parent = self
        self.right.parent = self

    def __repr__ (self):
        return f"CSG({self.left}, {self.right})"

    def contains(self, shape):
        return shape in self

    def __contains__ (self, shape):
            return shape in self.left or shape in shape.right
            
    def local_normal_at(self, pt, i):
        raise NotImplementedError

    def intersects_int(self, r):
        if self.bounds().intersects(r):
            return self.filter_intersections(self.left.intersects(r) + self.right.intersects(r))
        return Intersections()

    def filter_intersections(self, xs):
        inl = False
        inr = False
        
        result = Intersections()

        for i in xs:
            lhit = i.shape in self.left
            if self.operation (lhit, inl, inr):
                result.add(i)
            
            if lhit:
                inl = not inl
            else:
                inr = not inr
        return result

    def divide(self, threshold):
        hasattr(self.left, 'divide') and self.left.divide(threshold)
        hasattr(self.right, 'divide') and self.right.divide(threshold)

        