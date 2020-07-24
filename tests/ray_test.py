from ..rt import Ray
from ..rt import Point
from ..rt import Vector
from ..rt import translation, scaling

def test_create_and_query_a_ray():
    origin = Point(1, 2, 3)
    direction = Vector(4, 5, 6)
    ray = Ray(origin, direction)
    
    assert origin == ray.origin
    assert direction == ray.direction

def test_computing_a_point_from_a_distance():
    origin = Point(2,3,4)
    direction = Vector(1,0,0)
    ray = Ray(origin, direction)
    
    assert Point(2, 3, 4) == ray.position(0)
    assert Point(3, 3, 4) == ray.position(1)
    assert Point(1, 3, 4) == ray.position(-1)
    assert Point(4.5, 3, 4) == ray.position(2.5)
    
def test_translating_a_ray():
	r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
	m = translation(3, 4, 5)
	r2 = r.transform(m)
	
	assert Point(4,6,8) == r2.origin
	assert Vector(0, 1, 0) == r2.direction
	
def test_scaling_a_ray():
	r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
	m = scaling(2,3,4)
	r2 = r.transform(m)
	
	assert Point(2,6,12) == r2.origin
	assert Vector(0, 3, 0) == r2.direction