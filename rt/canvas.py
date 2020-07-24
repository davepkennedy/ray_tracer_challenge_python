from .color import Color

class Canvas:
    __slots__ = ['width', 'height', 'pixels']

    def __init__ (self, width, height):
        self.width = width
        self.height = height

        self.pixels = [Color(0,0,0) for i in range(width*height)]

    def __setitem__ (self, key, value):
        x,y = key
        self.pixels[y * self.width + x] = value

    def __getitem__ (self, key):
        x,y = key
        return self.pixels[y * self.width + x]

    def to_ppm (self, buffer):
        buffer.write(f"P3\n{self.width} {self.height}\n255\n")

        for i in range(self.height):
            buffer.write(' '.join( map( str, self.pixels[i * self.width:i*self.width+self.width])))
            buffer.write('\n')