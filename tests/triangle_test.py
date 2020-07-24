from ..rt import Triangle
from ..rt import Point, Vector
from ..rt import Ray

def test_constructing_a_triangle():
    p1 = Point(0, 1, 0)
    p2 = Point(-1, 0, 0)
    p3 = Point(1, 0, 0)
    
    t = Triangle(p1, p2, p3)
    
    assert p1 == t.p1
    assert p2 == t.p2
    assert p3 == t.p3
    
    assert Vector(-1, -1, 0) == t.e1
    assert Vector(1, -1, 0) == t.e2
    
    assert Vector(0, 0, -1) == t.normal

def test_normal_on_triangle():
    t = Triangle(
        Point(0, 1, 0),
        Point(-1, 0, 0),
        Point(1, 0, 0))
        
    n1 = t.normal_at(Point(0, 0.5, 0), None)
    n2 = t.normal_at(Point(-0.5, 0.75, 0), None)
    n3 = t.normal_at(Point(0.5, 0.25, 0), None)
    
    assert t.normal == n1
    assert t.normal == n2
    assert t.normal == n3
    
def test_intersecting_a_ray_parallel_to_the_triangle():
    t = Triangle(
        Point(0, 1, 0),
        Point(-1, 0, 0),
        Point(1, 0, 0))

    r = Ray(Point(0,-1,-2), Vector(0,1,0))
    xs = t.intersects(r)
    assert 0 == len(xs)
            
def test_a_ray_misses_the_p1_p3_edge():
    t = Triangle(
        Point(0, 1, 0),
        Point(-1, 0, 0),
        Point(1, 0, 0))
    r = Ray(Point(1, 1, -2), Vector(0, 0, 1))
    xs = t.intersects(r)
    assert 0 == len(xs)
        
def test_a_ray_misses_the_p1_p2_edge():
    t = Triangle(
        Point(0, 1, 0),
        Point(-1, 0, 0),
        Point(1, 0, 0))
    r = Ray(Point(-1, 1, -2), Vector(0, 0, 1))
    xs = t.intersects(r)
    assert 0 == len(xs)
    
def test_a_ray_misses_the_p2_p3_edge():
    t = Triangle(
        Point(0, 1, 0),
        Point(-1, 0, 0),
        Point(1, 0, 0))
    r = Ray(Point(0, -1, -2), Vector(0, 0, 1))
    xs = t.intersects(r)
    assert 0 == len(xs)
    
def test_a_ray_strikes_a_triangle():
    t = Triangle(
        Point(0, 1, 0),
        Point(-1, 0, 0),
        Point(1, 0, 0))
    r = Ray(Point(0, 0.5, -2), Vector(0, 0, 1))
    xs = t.intersects(r)
    assert 1 == len(xs)
    assert 2 == xs[0].t
    
def test_a_triangle_has_a_bounding_box():
    p1 = Point(-3, 7, 2)
    p2 = Point(6,2,-4)
    p3 = Point(2,-1,-1)
    shape = Triangle(p1, p2, p3)
    
    box = shape.bounds()
    
    assert Point(-3, -1, -4) == box.min
    assert Point(6, 7, 2) == box.max
