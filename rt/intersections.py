from .tuple import Point
from .linmath import EPSILON

import math

class Computation:
    __slots__ = [
        't',
        'shape',
        'point',
        'eyev',
        'normalv',
        'reflectv',
        'inside',
        'over_point',
        'under_point',
        'n1','n2'
    ]

    def __init__(self):
        self.inside = False

    def schlick(self):
        cos = self.eyev.dot(self.normalv)
        if self.n1 > self.n2:
            n = self.n1 / self.n2
            sin2t = (n * n) * (1 - (cos * cos))
            if sin2t > 1:
                return 1
            cos_t = math.sqrt(1 - sin2t)
            cos = cos_t
        r0 = math.pow((self.n1 - self.n2) / (self.n1 + self.n2), 2)
        return r0 + (1 - r0) * math.pow(1 - cos, 5)

class Intersection:
    __slots__ = ['t','shape','u','v']
    
    def __init__ (self, t, shape, u = None, v = None):
        self.t = t
        self.shape = shape
        self.u = u
        self.v = v
        
    def __eq__ (self, other):
        return isinstance(other, Intersection) and \
            self.t == other.t and \
            self.shape == other.shape
            
    def __repr__ (self):
        return f"Intersection({self.t}, {self.shape})"
        
    def prepare_computations(self, ray, xs = None):
        xs = xs or Intersections(self)
        
        comps = Computation()
        comps.t = self.t
        comps.shape = self.shape
        
        comps.point = ray.position(self.t)
        comps.eyev = -ray.direction
        
        comps.normalv = self.shape.normal_at(comps.point, self)
        comps.reflectv = ray.direction.reflect_on(comps.normalv)
        
        if comps.normalv.dot(comps.eyev) < 0:
            comps.inside = True
            comps.normalv = -comps.normalv
            
        comps.over_point = (comps.point + comps.normalv * EPSILON).to_point()
        comps.under_point = (comps.point - comps.normalv * EPSILON).to_point()
        
        containers = []
        for i in xs:
            if i == self:
                if len(containers) == 0:
                    comps.n1 = 1.0
                else:
                    comps.n1 = containers[-1].material.refractive_index
                    
            if i.shape in containers:
                containers.remove(i.shape)
            else:
                containers.append(i.shape)
                
            if i == self:
                if len(containers) == 0:
                    comps.n2 = 1.0
                else:
                    comps.n2 = containers[-1].material.refractive_index                    
                break    

        return comps
        
    


class Intersections:
    __slots__ = ['__intersections']

    def __init__ (self, *args):
        self.__intersections = list(args)

    def __repr__ (self):
        return f"Intersections({self.__intersections})"

    def __add__ (self, other):
        if isinstance(other, Intersection):
            return self + Intersections(other)
        if isinstance(other, Intersections):
            return Intersections(*sorted(self.__intersections + other.__intersections, key=lambda x: x.t))
        raise ValueError
            
    def add (self, intersection):
        self.__intersections.append(intersection)
        
    def __len__ (self):
        return len (self.__intersections)
        
    def __getitem__(self, key):
        return self.__intersections[key]

    def __iter__ (self):
        for i in self.__intersections:
            yield i

#    public Intersections Filter(Func<Intersection, bool> f) =>
#        Intersections(List<Intersection>(intersections.Where(f)))

    def first(self):
        return self.__intersections and self.__intersections[0] or None
            
    def hit(self):
        positives = [i for i in self.__intersections if i.t >= 0]
        positives = sorted(positives, key=lambda x: x.t)
        
        if len(positives):
            return positives[0]
        return None