from ..rt import Sphere
from ..rt import Point, Vector
from ..rt import Material
from ..rt import Matrix, Identity
from ..rt import Ray
from ..rt import translation, scaling, rotation_z

import math
  
def test_intersecting_a_scaled_sphere_with_a_ray():
	r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
	s = Sphere()
	s.transform = scaling (2, 2, 2)
	
	xs = s.intersects(r)

	assert 2 == len(xs)
	assert 3.0 == xs[0].t
	assert 7.0 == xs[1].t
        

def test_intersecting_a_translated_sphere_with_a_ray():
	r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
	s = Sphere()
	s.transform = translation (5, 0, 0)
	
	xs = s.intersects(r)
	
	assert 0 == len(xs)
        
def test_the_normal_on_a_sphere_at_a_point_on_the_x_axis():
	s = Sphere()
	n = s.normal_at(Point(1, 0, 0), None)
	
	assert Vector(1, 0, 0) == n
	
def test_the_normal_on_a_sphere_at_a_point_on_the_y_axis():
	s = Sphere()
	n = s.normal_at(Point(0, 1, 0), None)
	
	assert Vector(0, 1, 0) == n
	
def test_the_normal_on_a_sphere_at_a_point_on_the_z_axis():
	s = Sphere()
	n = s.normal_at(Point(0, 0, 1), None)
	assert Vector(0, 0, 1) == n
	
def test_the_normal_on_a_sphere_at_a_non_axis_point():
	rtot = math.sqrt(3.0) / 3.0
	s = Sphere()
	n = s.normal_at(Point(rtot, rtot, rtot), None)
	assert Vector(rtot, rtot, rtot) == n
	
def test_the_normal_is_a_normalized_vector():
	rtot = math.sqrt(3.0) / 3.0
	s = Sphere()
	n = s.normal_at(Point(rtot, rtot, rtot), None)
	assert n == n.normalize()
	
def test_computing_the_normal_on_a_translated_sphere():
	s = Sphere()
	s.Transform = translation(0, 1, 0)
	n = s.normal_at(Point(0, 1.70711, -0.70711), None)
	assert Vector(0, 0.70711, -0.70711) == n
        
def test_ComputingTheNormalOnATransformedSphere():
	rtot = math.sqrt(2) / 2.0
	s = Sphere()
	m = scaling (1, 0.5, 1) * rotation_z((math.pi / 5.0))
	s.Transform = m
	n = s.normal_at(Point(0, rtot, -rtot), None)
	assert Vector(0, 0.97014, -0.24254) == n
        
def test_helper_for_creating_a_sphere_with_a_glassy_material():
	s = Sphere.glass()
	
	assert Identity(4) == s.transform
	assert 1 == s.material.transparency
	assert 1.5 == s.material.refractive_index

def test_a_sphere_has_a_bounding_box():
	shape = Sphere()
	box = shape.bounds()
	assert Point(-1, -1, -1) == box.min
	assert Point(1, 1, 1) == box.max