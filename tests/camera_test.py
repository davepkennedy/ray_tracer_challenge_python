from ..rt import Camera
from ..rt import Color
from ..rt import Identity
from ..rt import Point, Vector
from ..rt import translation, rotation_y, view
from ..rt import default_world
from ..rt.linmath import approx_eq

import math

def test_constructing_a_camera():
    hsize = 160
    vsize = 120
    field_of_view = math.pi / 2.0
    
    camera = Camera(hsize, vsize, field_of_view)
    
    assert hsize == camera.h_size
    assert vsize == camera.v_size
    assert field_of_view == camera.field_of_view
    assert Identity(4) == camera.transform

def test_pixel_size_for_a_horizontal_canvas():
    camera = Camera(200, 125, math.pi / 2)
    assert approx_eq(0.01, camera.pixel_size)

def test_pixel_size_for_a_vertical_canvas():
    camera = Camera(125, 200, math.pi / 2)
    assert approx_eq(0.01, camera.pixel_size)

def test_ConstructingARayThroughTheCenterOfTheCanvas():
    camera = Camera(201, 101, math.pi / 2)
    r = camera.ray_for_pixel(100, 50)
    assert Point(0, 0, 0) == r.origin
    assert Vector(0, 0, -1) == r.direction
    
def test_constructing_a_ray_through_the_corner_of_the_canvas():
    camera = Camera(201, 101, math.pi / 2)
    r = camera.ray_for_pixel(0, 0)
    assert Point(0, 0, 0) == r.origin
    assert Vector(0.66519, 0.33259, -0.66851) == r.direction
    
def test_constructing_a_ray_when_the_canvas_is_transformed():
    rtot = math.sqrt(2) / 2
    camera = Camera(201, 101, math.pi / 2)
    camera.transform = rotation_y(math.pi / 4) * translation(0, -2, 5)
    r = camera.ray_for_pixel(100, 50)
    assert Point(0, 2, -5) == r.origin
    assert Vector(rtot, 0, -rtot) == r.direction

def test_rendering_a_world_with_a_camera():
    w = default_world()
    c = Camera(11, 11, math.pi / 2)
    f = Point(0, 0, -5)
    t = Point(0, 0, 0)
    u = Vector(0, 1, 0)
    c.transform = view(f, t, u)
    
    image = c.render(w)
    assert Color(0.38066, 0.47583, 0.2855) == image[(5, 5)]