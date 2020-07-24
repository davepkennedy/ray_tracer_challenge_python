from ..rt import Material
from ..rt import Color
from ..rt import Point, Vector
from ..rt import PointLight, lighting
from ..rt import Sphere
from ..rt import StripePattern, Pattern

import math

def test_the_default_material():
	m = Material()
	assert Color(1, 1, 1) == m.color
	assert 0.1 == m.ambient
	assert 0.9 == m.diffuse
	assert 0.9 == m.specular
	assert 200.0 == m.shininess

def test_lighting_with_the_eye_between_the_light_and_the_surface():
	shape = Sphere()
	m = Material()
	position = Point(0, 0, 0)
	eyev = Vector(0, 0, -1)
	normalv = Vector(0, 0, -1)
	light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
	result = lighting(m, shape, light, position, eyev, normalv, False)
	assert Color(1.9, 1.9, 1.9) == result
	
def test_lighting_with_the_eye_between_the_light_and_the_surface_eye_offset_45():
	shape = Sphere()
	rtot = math.sqrt(2) / 2.0
	m = Material()
	position = Point(0, 0, 0)
	eyev = Vector(0, -rtot, -rtot)
	normalv = Vector(0, 0, -1)
	light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
	result = lighting(m, shape, light, position, eyev, normalv, False)
	assert Color(1.0, 1.0, 1.0) == result
	
def test_lighting_with_the_eye_between_the_light_and_the_surface_light_offset_45():
	shape = Sphere()
	rtot = math.sqrt(2) / 2.0
	m =  Material()
	position = Point(0, 0, 0)
	eyev =  Vector(0, 0, -1)
	normalv = Vector(0, 0, -1)
	light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
	result = lighting(m, shape, light, position, eyev, normalv, False)
	assert Color(0.7364, 0.7364, 0.7364) == result
	
def test_lighting_with_the_eye_in_the_path_of_the_reflection_vector():
	shape = Sphere()
	rtot = math.sqrt(2) / 2.0
	m =  Material()
	position = Point(0, 0, 0)
	eyev = Vector(0, -rtot, -rtot)
	normalv = Vector(0, 0, -1)
	light = PointLight(Point(0, 10, -10), Color(1, 1, 1))
	result = lighting(m, shape, light, position, eyev, normalv, False)
	assert Color(1.6364, 1.6364, 1.6364) == result

def test_lighting_with_light_behind_the_surface():
	shape = Sphere()
	m = Material()
	position = Point(0, 0, 0)
	eyev = Vector(0, 0, -1)
	normalv = Vector(0, 0, -1)
	light =  PointLight(Point(0, 0, 10), Color(1, 1, 1))
	result = lighting(m, shape, light, position, eyev, normalv, False)
	assert Color(0.1, 0.1, 0.1) == result

def test_lighting_with_the_surface_in_shadow():
	shape = Sphere()
	m = Material()
	position = Point(0, 0, 0)
	eyev = Vector(0, 0, -1)
	normalv = Vector(0, 0, -1)
	light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
	inShadow = True
	result = lighting(m, shape, light, position, eyev, normalv, inShadow)
	assert Color(0.1, 0.1, 0.1) == result
	
def test_lighting_with_a_pattern_applied():
	m = Material()
	m.pattern = StripePattern(Color.WHITE, Color.BLACK)
	m.ambient = 1
	m.diffuse = 0
	m.specular = 0
	
	shape = Sphere()
	eyev = Vector(0, 0, -1)
	normalv = Vector(0, 0, -1)
	light = PointLight(Point(0, 0, -10), Color.WHITE)
	c1 = lighting(m, shape, light, Point(0.9, 0, 0), eyev, normalv, False)
	c2 = lighting(m, shape, light, Point(1.1, 0, 0), eyev, normalv, False)
	assert Color.WHITE == c1
	assert Color.BLACK == c2
	
def test_reflectivity_for_the_default_material():
	m = Material()
	assert 0.0 == m.reflective
	
def test_transparency_and_refractive_index_for_the_default_world():
	m = Material()
	assert 0 == m.transparency
	assert 1 == m.refractive_index
	