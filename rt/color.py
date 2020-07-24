from .linmath import approx_eq

def _clamp_component(c):
    c = 255 * c
    if c > 255:
        return 255
    if c < 0:
        return 0
    return round(c)

class ColorMeta(type):
    @property
    def BLACK(cls):
        return Color(0,0,0)

    @property
    def WHITE(cls):
        return Color(1,1,1)


class Color(metaclass=ColorMeta):
    __slots__ = ['red','green','blue']

    def __init__ (self, r,g,b):
        self.red = r
        self.green = g
        self.blue = b

    def __str__(self):
        r = _clamp_component(self.red)
        g = _clamp_component(self.green)
        b = _clamp_component(self.blue)
        return f"{r} {g} {b}"

    def __repr__(self):
        return f"Color({self.red}, {self.green}, {self.blue})"

    def __eq__(self, value):
        print(f"Testing equality of {self} and {value}")
        return approx_eq(self.red, value.red) and \
            approx_eq(self.green, value.green) and \
            approx_eq(self.blue, value.blue)

    def __mul__(self, value):        
        if isinstance (value, Color):
            return Color(
                self.red * value.red,
                self.green * value.green,
                self.blue * value.blue)
        elif isinstance(value, float) or isinstance(value, int):
            return Color(
                self.red * value,
                self.green * value,
                self.blue * value)

    def __add__ (self, other):
        return Color(
            self.red + other.red,
            self.green + other.green,
            self.blue + other.blue)
    
    def __sub__ (self, other):
        return Color(
            self.red - other.red,
            self.green - other.green,
            self.blue - other.blue)