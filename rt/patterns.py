from .matrix import Identity

from .improved_noise import noise as improved_noise
import math

class Pattern:
    __slots__ = ['transform']
    
    def __init__ (self):
        self.transform = Identity(4)
        
        
    def pattern_at_object(self, shape, pt):
        object_point = shape.transform.inverse() * pt
        patternPoint = self.transform.inverse() * object_point
        return self.pattern_at(patternPoint.to_point())


class StripePattern(Pattern):
    __slots__ = ['a', 'b']
    
    def __init__ (self, a,b):
        super().__init__()
        self.a = a
        self.b = b

    def pattern_at(self, pt):
        if math.floor(pt.x) % 2 == 0:
            return self.a
        return self.b
        
class GradientPattern(Pattern):
    __slots__ = ['a','b']
    
    def __init__ (self, a, b):
        self.a = a
        self.b = b
        
    def pattern_at(self, pt):
        return self.a + (self.b - self.a) * (pt.x - math.floor(pt.x))

class RingPattern(Pattern):
    __slots__ = ['a','b']
    
    def __init__ (self, a, b):
        self.a = a
        self.b = b
        
    def pattern_at(self, pt):
        xs = pt.x * pt.x
        zs = pt.z * pt.z
        return self.a if math.floor(math.sqrt(xs+zs)) % 2 == 0 else self.b

class CheckersPattern (Pattern):
    __slots__ = ['a','b']
    
    def __init__(self,a,b):
        self.a = a
        self.b = b
        
    def pattern_at(self, pt):
        return self.a if (math.floor(pt.x) + math.floor(pt.y) + math.floor(pt.z)) % 2 == 0 else self.b
        
class PerlinPattern (Pattern):
    __slots__ = ['a','b']
    
    def __init__ (self, a, b):
        self.a = a
        self.b = b
        
    def pattern_at(self, pt):
        noise = improved_noise(pt.x, pt.y, pt.z)
        return self.a + (self.b - self.a) * noise