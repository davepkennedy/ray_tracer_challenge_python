from ..rt import Plane
from ..rt import Point, Vector
from ..rt import Ray
from ..rt.linmath import NEGATIVE_INFINITY, POSITIVE_INFINITY

def test_the_normal_of_a_plane_is_constant_everywhere():
    plane = Plane()
    n1 = plane.normal_at(Point(0, 0, 0), None)
    n2 = plane.normal_at(Point(10, 0, -10), None)
    n3 = plane.normal_at(Point(-5, 0, 150), None)
    
    assert Vector(0, 1, 0) == n1
    assert Vector(0, 1, 0) == n2
    assert Vector(0, 1, 0) == n3
        

def test_intersect_a_ray_parallel_to_the_plane():
    plane = Plane()
    ray = Ray(Point(0, 10, 0), Vector(0, 0, 1))
    xs = plane.intersects(ray)
    assert 0 == len(xs)
    
def test_intersects_with_a_coplanar_ray():
    plane = Plane()
    ray = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    xs = plane.intersects(ray)
    assert 0 == len(xs)
    
def test_a_ray_intersecting_a_plane_from_above():
    plane = Plane()
    ray = Ray(Point(0, 1, 0), Vector(0, -1, 0))
    xs = plane.intersects(ray)
    
    assert 1 == len(xs)
    assert 1 == xs[0].t
    assert plane == xs[0].shape
    
def test_a_ray_intersecting_a_plane_from_below():
    plane = Plane()
    ray = Ray(Point(0, -1, 0), Vector(0, 1, 0))
    xs = plane.intersects(ray)
    
    assert 1 == len(xs)
    assert 1 == xs[0].t
    assert plane == xs[0].shape
        
def test_a_plane_has_a_bounding_box():
    shape = Plane()
    box = shape.bounds()
    assert Point(NEGATIVE_INFINITY, 0, NEGATIVE_INFINITY) == box.min
    assert Point(POSITIVE_INFINITY, 0, POSITIVE_INFINITY) == box.max