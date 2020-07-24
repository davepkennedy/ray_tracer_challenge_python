from .color import Color
from .tuple import Point
from .lights import PointLight, lighting
from .ray import Ray
from .sphere import Sphere
from .material import Material
from .transform import scaling
from .intersections import Intersection, Intersections

import math

class World:

    __slots__ = [
        '__shapes',
        'light'
    ]

    def __init__(self):
        self.__shapes = []
        self.light = None

    def __len__(self):
        return len(self.__shapes)

    def __iter__(self):
        for val in self.__shapes:
            yield val

    def __getitem__(self,key):
        return self.__shapes[key]
    
    def is_empty (self):
        return len(self) == 0
        
    def add (self, shape):
        self.__shapes.append(shape)
        
    def __contains__ (self,val):
        return self.__shapes.__contains__(val)

    def has_light(self):
        return self.light != None

    def contains(self, shape):
        return shape in self
        
    def intersections(self, ray):
        intersections_list = map (lambda shape: shape.intersects(ray), self.__shapes)
        intersections = [intersection for intersections in intersections_list for intersection in intersections]
        return Intersections(*sorted(intersections, key=lambda i: i.t))
        
    
    def shade(self, comps, stack_depth):
        shadowed = self.is_shadowed(comps.over_point)
        surface = lighting(comps.shape.material, comps.shape,  
                self.light, comps.over_point, comps.eyev, comps.normalv, shadowed)
        reflected = self.reflected_color(comps, stack_depth)
        refracted = self.refracted_color(comps, stack_depth)
        
        if comps.shape.material.reflective > 0 and comps.shape.material.transparency > 0:
            reflectance = comps.schlick()
            return surface + (reflected * reflectance) + (refracted * (1 - reflectance))
            
        return surface + reflected + refracted
        

    def color_at(self, r, stack_depth):
        intersections = self.intersections(r)
        intersection = intersections.hit()
        if intersection != None:
            comps = intersection.prepare_computations(r, intersections)
            return self.shade(comps, stack_depth)
        return Color.BLACK
        

    def is_shadowed(self, point):
        v = self.light.position - point
        distance = v.magnitude()
        direction = v.normalize()
        ray = Ray(point, direction)
        intersections = self.intersections(ray)
        h = intersections.hit()
        if (h and h.t < distance):
            return True
        return False
        

    def reflected_color(self, comps, stack_depth):
        if stack_depth <= 0:
            return Color.BLACK
        
        if comps.shape.material.reflective == 0:
            return Color.BLACK
            
        reflect_ray = Ray(comps.over_point, comps.reflectv)
        color = self.color_at(reflect_ray, stack_depth-1)
        return color * comps.shape.material.reflective
        
    def refracted_color(self, comps, remaining):
        if remaining == 0:
            return Color.BLACK
            
        if comps.shape.material.transparency == 0:
            return Color.BLACK
            
        n_ratio = comps.n1 / comps.n2
        cosI = comps.eyev.dot(comps.normalv)
        sin2t = (n_ratio * n_ratio) * (1 - (cosI * cosI))
        if sin2t > 1:
            return Color.BLACK
            
        cosT = math.sqrt(1.0 - sin2t)
        direction = comps.normalv * (n_ratio * cosI - cosT) - comps.eyev * n_ratio
        refract_ray = Ray(comps.under_point, direction)
        return self.color_at(refract_ray, remaining - 1) * comps.shape.material.transparency
        
    

def default_world():
    w = World()
    w.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
    s1 = Sphere()
    s1.material.color = Color(0.8, 1.0, 0.6)
    s1.material.diffuse = 0.7
    s1.material.specular = 0.2
    s2 = Sphere()
    s2.transform = scaling(0.5, 0.5, 0.5)
    w.add(s1)
    w.add(s2)
    return w
        