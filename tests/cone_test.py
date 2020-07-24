from ..rt.linmath import approx_eq

from ..rt import Cone
from ..rt import Point, Vector
from ..rt import Ray

import pytest

@pytest.mark.parametrize("px,py,pz,dx,dy,dz,t0,t1", [
        (0, 0, -5,  0, 0, 1,    5,5),
        (0, 0, -5,  1, 1, 1,    8.66025, 8.66025),
        (1, 1, -5,  -0.5,-1,    1, 4.55006, 49.44994)])
def test_intersecting_a_cone_with_a_ray(px, py, pz, dx, dy, dz, t0, t1):
    shape = Cone()
    direction = Vector(dx, dy, dz).normalize()
    r = Ray(Point(px, py, pz), direction)
    xs = shape.intersects(r)
    assert 2, len(xs)
    assert approx_eq(t0, xs[0].t)
    assert approx_eq(t1, xs[1].t)
        
def test_intersecting_a_cone_with_a_ray_parallel_to_one_of_its_halves():
    shape = Cone()
    direction = Vector(0, 1, 1).normalize()
    r = Ray(Point(0, 0, -1), direction)
    xs = shape.intersects(r)
    
    assert 1 == len(xs)
    assert approx_eq(0.35355, xs[0].t)
   
@pytest.mark.parametrize("px,py,pz,dx,dy,dz, count",[        
        (0, 0, -5,      0, 1, 0,    0),
        (0, 0, -0.25,   0, 1, 1,    2),
        (0, 0, -0.25,   0, 1, 0,    4)])
def test_intersecting_a_cones_end_caps(px, py, pz, dx, dy, dz, count):
    shape = Cone()
    shape.minimum = -0.5
    shape.maximum = 0.5
    shape.closed = True
    
    direction = Vector(dx, dy, dz).normalize()
    r = Ray(Point(px, py, pz), direction)
    xs = shape.intersects(r)
    assert count == len(xs)   
        
@pytest.mark.parametrize("px,py,pz, nx,ny,nz",[        
        (0, 0, 0,       0, 0, 0),
        (1, 1, 1,       1, -1.41421356, 1),
        (-1, -1, 0,     -1, 1, 0)])
def test_computing_the_normal_vector_on_a_cone(px, py, pz, nx, ny, nz):
    shape = ConeFixture()
    n = shape.normal_at_test(Point(px, py, pz))
    assert Vector(nx, ny, nz) == n
    
def test_an_unbounded_cone_has_a_bounding_box():
    shape = Cone()
    box = shape.bounds()
    assert Point.MIN == box.min
    assert Point.MAX == box.max
    
def test_a_bounded_cone_has_a_bounding_box():
    shape = Cone()
    shape.minimum = -5
    shape.maximum = 3
    
    box = shape.bounds()
    assert Point(-5,-5,-5) == box.min
    assert Point(5, 3, 5) == box.max

class ConeFixture (Cone):
    def normal_at_test(self, pt):
        return self.local_normal_at(pt,None)

    