from ..rt import Cylinder
from ..rt import Point, Vector
from ..rt import Ray
from ..rt.linmath import approx_eq, POSITIVE_INFINITY, NEGATIVE_INFINITY

import pytest

@pytest.mark.parametrize("px,py,pz, dx,dy,dz", [
        (1, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 1, 0),
        (0, 0, -5, 1, 1, 1)])
def test_a_ray_misses_a_cylinder(
            px, py, pz,
            dx, dy, dz):
    cyl = Cylinder()
    direction = Vector(dx, dy, dz).normalize()
    r = Ray(Point(px, py, pz), direction)
    xs = cyl.intersects(r)
    assert 0 == len(xs)
    
@pytest.mark.parametrize("px,py,pz, dx,dy,dz,   t0,t1", [
        (1,0,-5,0,0,1,5,5),
        (0, 0, -5, 0, 0, 1, 4, 6),
        (0.5, 0, -5, 0.1, 1, 1, 6.80798, 7.08872)])
def test_a_ray_strikes_a_cylinder(
            px, py, pz,
            dx, dy, dz,
            t0, t1):
    cyl = Cylinder()
    direction = Vector(dx, dy, dz).normalize()
    r = Ray(Point(px, py, pz), direction)
    xs = cyl.intersects(r)
    
    assert 2, len(xs)
    assert approx_eq(t0, xs[0].t)
    assert approx_eq(t1, xs[1].t)
   
@pytest.mark.parametrize("px,py,pz, nx,ny,nz", [
        (1,0,0,1,0,0),
        (0,5,-1,0,0,-1),
        (0,-2,1,0,0,1),
        (-1,1,0,-1,0,0)])
def test_normal_vector_on_a_cylinder(
            px, py, pz,
            nx, ny, nz):
    cyl = Cylinder()
    assert Vector(nx, ny, nz) == cyl.normal_at(Point(px, py, pz), None)
        
def test_the_default_minimum_and_maximum_for_a_cylinder():
    c = Cylinder()
    assert POSITIVE_INFINITY == c.maximum
    assert NEGATIVE_INFINITY == c.minimum
        
@pytest.mark.parametrize("px,py,pz, dx,dy,dz, count", [
        (0, 1.5, 0, 0.1, 1, 0, 0),
        (0, 3, -5, 0, 0, 1, 0),
        (0, 0, -5, 0, 0, 1, 0),
        (0, 2, -5, 0, 0, 1, 0),
        (0, 1, -5, 0, 0, 1, 0),
        (0, 1.5, -2, 0, 0, 1, 2)])
def test_intersecting_a_constrained_cylinder(
            px, py, pz,
            dx, dy, dz,
            count):
    cyl = Cylinder()
    cyl.minimum = 1
    cyl.maximum = 2
    
    direction = Vector(dx, dy, dz).normalize()
    r = Ray(Point(px, py, pz), direction)
    xs = cyl.intersects(r)
    assert count == len(xs)
        
def test_the_default_closed_value_for_a_cylinder():
    cyl = Cylinder()
    assert not cyl.closed
        
@pytest.mark.parametrize("px,py,pz, dx,dy,dz,   count", [
        (0, 3, 0,       0, -1, 0,   2),
        (0, 3, -2,      0, -1, 2,   2),
        (0, 4, -2,      0, -1, 1,   2),
        (0, 0, -2,      0, 1, 2,    2),
        (0, -1, -2,     0, 1, 1,    2)])
def test_intersecting_the_caps_of_a_closed_cylinder(
            px, py, pz,
            dx, dy, dz,
            count):
    cyl = Cylinder()
    cyl.minimum = 1
    cyl.maximum = 2
    cyl.closed = True
    
    direction = Vector(dx, dy, dz).normalize()
    r = Ray(Point(px, py, pz), direction)
    xs = cyl.intersects(r)
    assert count == len(xs)
    
@pytest.mark.parametrize("px,py,pz, vx,vy,vz", [
        (0,   1, 0,     0, -1,0),
        (0.5, 1, 0,     0, -1, 0),
        (0,   1, 0.5,   0, -1, 0),
        (0,   2, 0,     0, 1, 0),
        (0.5, 2, 0,     0, 1, 0),
        (0,   2, 0.5,   0, 1, 0)])
def test_the_normal_vector_on_a_cylinders_end_caps(
            px, py, pz,
            vx, vy, vz):
    cyl = Cylinder()
    cyl.minimum = 1
    cyl.maximum = 2
    cyl.closed = True
    
    n = cyl.normal_at(Point(px, py, pz), None)
    assert Vector(vx, vy, vz) == n
   
def test_an_unbounded_cylinder_has_a_bounding_box():
    shape = Cylinder()
    box = shape.bounds()
    assert Point(-1,NEGATIVE_INFINITY, -1) == box.min
    assert Point(1,POSITIVE_INFINITY, 1) == box.max

def test_a_bounded_cylinder_has_a_bounding_box():
    shape = Cylinder()
    shape.minimum = -5
    shape.maximum = 3
    
    box = shape.bounds()
    assert Point(-1, -5, -1) == box.min
    assert Point(1, 3, 1) == box.max