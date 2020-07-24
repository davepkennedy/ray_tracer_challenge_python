from .color import Color

import math

class PointLight:
    __slots__ = ['position', 'intensity']

    def __init__ (self, position, intensity):
        self.position = position
        self.intensity = intensity

    def __repr__ (self):
        return f"PointLight({repr(self.position)}, {repr(self.intensity)})"

    def __eq__ (self, other):
        if not isinstance(other, PointLight):
            return False

        return self.position == other.position \
            and self.intensity == other.intensity

def lighting(mat, shape, light, pt, eye, normal, in_shadow):
    diffuse = Color(0, 0, 0)
    specular = Color(0, 0, 0)

    color = mat.pattern.pattern_at_object(shape,pt) if mat.pattern else mat.color
    
    effective_color = color * light.intensity
    lightv = (light.position - pt).normalize()
    ambient = effective_color * mat.ambient
    
    if in_shadow:
        return ambient
        
    light_dot_normal = lightv.dot(normal)
    if light_dot_normal >= 0:
        diffuse = effective_color * mat.diffuse * light_dot_normal
        reflectv = (-lightv).reflect_on(normal)
        reflectDotEye = reflectv.dot(eye)
        
        if reflectDotEye > 0:
            factor = math.pow(reflectDotEye, mat.shininess)
            specular = light.intensity * mat.specular * factor
            
    return ambient + diffuse + specular