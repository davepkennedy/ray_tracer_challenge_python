from ..rt import Cube
from ..rt import Point, Vector
from ..rt import Ray

import pytest

@pytest.mark.parametrize("px,py,pz, dx,dy,dz,   t1,t2", [
    (5, 0.5, 0,   -1, 0, 0,     4, 6),
    (-5, 0.5, 0,    1, 0, 0,    4, 6),
         
    (0.5, 5, 0,     0, -1, 0,   4, 6),
    (0.5, -5, 0,    0, 1, 0,    4, 6),

    (0.5, 0, 5,     0, 0, -1,   4, 6),
    (0.5, 0, -5,    0, 0, 1,    4, 6),

    (0, 0.5, 0,     0, 0, 1,    -1, 1)])
def test_a_ray_intersects_a_cube(px,py,pz,   dx,dy,dz,   t1,t2):
    c =  Cube()
    r =  Ray(Point(px,py,pz), Vector(dx,dy,dz))
    xs = c.intersects(r)
    assert t1 == xs[0].t
    assert t2 == xs[1].t

@pytest.mark.parametrize("px,py,pz, dx,dy,dz", [
    (-2, 0, 0, 0.2673, 0.5345, 0.8018),
    (0, -2, 0, 0.8018, 0.2673, 0.5345),
    (0, 0, -2, 0.5345, 0.8018, 0.2673),

    (2, 0, 2, 0, 0, -1),
    (0, 2, 2, 0, -1, 0),
    (2, 2, 0, -1, 0, 0)])
def test_a_ray_misses_a_cube(px,py,pz,   dx,dy,dz):
    c = Cube()
    r = Ray( Point(px, py, pz),  Vector(dx, dy, dz))
    xs = c.intersects(r)
    assert 0 == len(xs)

@pytest.mark.parametrize("px,py,pz, nx,ny,nz", [
        (1, 0.5, -0.8,      1, 0, 0),
        (-1, -0.2, 0.9,     -1, 0, 0),

        (-0.4, 1, -0.1,     0, 1, 0),
        (0.3, -1, -0.7,     0, -1, 0),

        (-0.6, 0.3, 1,      0, 0, 1),
        (0.4, 0.4, -1,      0, 0, -1),

        (1, 1, 1,           1, 0, 0),
        (-1, -1, -1,        -1, 0, 0)])
def test_the_normal_on_the_surface_of_a_cube(px,py,pz,   nx,ny,nz):
    c = Cube()
    normal = c.normal_at(Point(px, py, pz), None)
    assert Vector(nx, ny, nz) == normal

def test_cube_has_a_bounding_box():
    shape = Cube()
    box = shape.bounds()
    
    assert Point(-1, -1, -1) == box.min
    assert Point(1, 1, 1) == box.max
        