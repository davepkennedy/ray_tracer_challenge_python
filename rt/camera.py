from .matrix import Identity
from .tuple import Point
from .ray import Ray
from .canvas import Canvas

import math
class Camera:
    __slots__ = [
        'h_size',
        'v_size',
        'field_of_view',
        'transform',
        'half_width',
        'half_height',
        'pixel_size'
    ]

    def __init__ (self, hsize, vsize, fov):
        self.h_size = hsize
        self.v_size = vsize
        self.field_of_view = fov
        self.transform = Identity()

        half_view = math.tan(fov / 2)
        aspect = hsize / vsize

        if (aspect >= 1):
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view
        
        self.pixel_size = (self.half_width * 2) / hsize

    def ray_for_pixel(self, px, py):
        xoffset = (px + 0.5) * self.pixel_size
        yoffset = (py + 0.5) * self.pixel_size
        
        worldX = self.half_width - xoffset
        worldY = self.half_height - yoffset
        
        pixel = self.transform.inverse() * Point(worldX, worldY, -1)
        origin = self.transform.inverse() * Point(0, 0, 0)
        direction = (pixel - origin).normalize()
        
        return Ray(origin, direction)

    def render (self, world):
        image = Canvas(self.h_size, self.v_size)
    
        for y in range(self.v_size):
            for x in range(self.h_size):
                ray = self.ray_for_pixel(x, y)
                color = world.color_at(ray,5)
                image[x, y] = color
        return image