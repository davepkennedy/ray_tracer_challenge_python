from .color import Color

class Material:
    __slots__ = [
        'color', 
        'ambient', 
        'diffuse', 
        'specular', 
        'shininess',
        'reflective',
        'transparency',
        'refractive_index',
        'pattern'
    ]
    
    def __init__ (self, 
            color = None,
            ambient = None, 
            diffuse = None, 
            specular = None, 
            shininess = None,
            reflective = None,
            transparency = None,
            refractive_index = None,
            pattern = None):
        self.color = color or Color(1,1,1)
        self.ambient = ambient or 0.1
        self.diffuse = diffuse or 0.9
        self.specular = specular or 0.9
        self.shininess = shininess or 200.0
        self.reflective = reflective or 0
        self.transparency = transparency or 0
        self.refractive_index = refractive_index or 1
        self.pattern = pattern
        
    def __eq__ (self, other):
        if not isinstance(other, Material):
            return False

        for slot in Material.__slots__:
            if getattr(self, slot) != getattr(other, slot):
                return False
        return True