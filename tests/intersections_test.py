from ..rt import Intersection, Intersections
from ..rt import Sphere
from ..rt import Ray
from ..rt import Color
from ..rt import Point, Vector
from ..rt import default_world
from ..rt import PointLight
from ..rt import Plane
from ..rt import scaling, translation
from ..rt import Triangle

from ..rt.linmath import approx_eq, EPSILON

import math
import pytest

# Chapter 5
def test_intersection_encapsulates_t_and_object():
    t = 0.5
    o = Sphere()
    
    intersection = Intersection(t, o)
    
    assert t == intersection.t
    assert o == intersection.shape

# Chapter 5
def test_the_hit_when_all_intersections_have_positive_t():
    s = Sphere()
    i1 = Intersection(1, s)
    i2 = Intersection(2, s)
    xs = Intersections( i2, i1 )
    i = xs.hit()
    assert i1 == i

# Chapter 5
def test_the_hit_when_some_intersections_have_negative_t():
    s = Sphere()
    i1 = Intersection(-1, s)
    i2 = Intersection(1, s)
    xs = Intersections( i2, i1 )
    i = xs.hit()
    assert i2 == i

# Chapter 5
def test_the_hit_when_all_intersections_have_negative_t():
    s = Sphere()
    i1 = Intersection(-1, s)
    i2 = Intersection(-2, s)
    xs = Intersections( i2, i1 )
    i = xs.hit()
    assert i == None

# Chapter 5
def test_the_hit_is_always_the_lowest_non_negative_intersection():
    s = Sphere()
    i1 = Intersection(5, s)
    i2 = Intersection(7, s)
    i3 = Intersection(-3, s)
    i4 = Intersection(2, s)
    xs = Intersections( i1, i2, i3, i4 )
    i = xs.hit()
    assert i4 == i

#Chapter 7
def test_precomputing_the_state_of_an_intersection():
    r = Ray(Point(0,0,-5), Vector(0,0,1))
    shape = Sphere()
    i = Intersection(4, shape)
    
    comps = i.prepare_computations(r)
    assert i.t, comps.t
    assert i.shape == comps.shape
    assert Point(0, 0, -1) == comps.point
    assert Vector(0, 0, -1) == comps.eyev
    assert Vector(0, 0, -1) == comps.normalv
    

# Chapter 7
def test_hit_when_intersection_occurs_on_the_outside():
    r = Ray(Point(0,0,-5), Vector(0,0,1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = i.prepare_computations(r)
    assert not comps.inside

def test_hit_when_intersection_occurs_on_the_inside():
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(1, shape)
    comps = i.prepare_computations(r)
    assert Point(0,0,1) == comps.point
    assert Vector(0,0,-1) == comps.eyev
    assert comps.inside
    assert Vector(0,0,-1) == comps.normalv

def def_the_hit_should_offset_the_point():
    ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    shape.transform = translation(0, 0, 1)
    i = Intersection(5, shape)
    comps = i.prepare_computations(ray)
    assert comps.over_point.z < -EPSILON / 2
        
def test_precomputing_the_reflection_vector():
    rtot = math.sqrt(2) / 2
    shape = Plane()
    ray = Ray(Point(0, 1, -1), Vector(0, -rtot, rtot))
    i = Intersection(math.sqrt(2), shape)
    comps = i.prepare_computations(ray)
    assert Vector(0, rtot, rtot) == comps.reflectv
        
@pytest.mark.parametrize("index,n1,n2",[
        (0, 1.0, 1.5),
        (1, 1.5, 2.0),
        (2, 2.0, 2.5),
        (3, 2.5, 2.5),
        (4, 2.5, 1.5),
        (5, 1.5, 1.0)])
def test_finding_n1_and_n2_at_various_intersections(index, n1, n2):
    a = Sphere.glass()
    a.transform = scaling(2, 2, 2)
    a.material.refractive_index = 1.5
    
    b = Sphere.glass()
    b.transform = translation(0, 0, -0.25)
    b.material.refractive_index = 2.0
    
    c = Sphere.glass()
    c.transform = translation(0, 0, 0.25)
    c.material.refractive_index = 2.5
    
    r = Ray(Point(0, 0, -4), Vector(0, 0, 1))
    xs = Intersections(
        Intersection(2,a),
        Intersection(2.75,b),
        Intersection(3.25,c),
        Intersection(4.75,b),
        Intersection(5.25,c),
        Intersection(6,a))
    
    comps = xs[index].prepare_computations(r, xs)
    assert n1 == comps.n1
    assert n2 == comps.n2

def test_the_underpoint_is_offset_below_the_surface():
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere.glass()
    shape.transform = translation(0, 0, 1)
    i = Intersection(5, shape)
    xs = Intersections(i)
    comps = i.prepare_computations(r, xs)
    assert comps.under_point.z > EPSILON / 2
    assert comps.point.z < comps.under_point.z
        
def test_the_schlick_approximation_under_total_internal_reflection():
    shape = Sphere.glass()
    r = Ray(Point(0, 0, -math.sqrt(2)/2), Vector(0, 1, 0))
    xs = Intersections(
        Intersection(-math.sqrt(2)/2, shape),
        Intersection(math.sqrt(2)/2, shape))

    comps = xs[1].prepare_computations(r, xs)
    reflectance = comps.schlick()
    assert 1 == reflectance
        
def test_the_schlick_approximation_with_a_perpendicular_viewing_angle():
    shape = Sphere.glass()
    r = Ray(Point(0, 0, 0), Vector(0, 1, 0))
    xs = Intersections(
        Intersection(-1, shape),
        Intersection(1, shape))

    comps = xs[1].prepare_computations(r, xs)
    reflectance = comps.schlick()
    assert approx_eq(0.04, reflectance)

def test_the_schlick_approximation_with_small_angle_and_n2_more_than_n1():
    shape = Sphere.glass()
    r = Ray(Point(0, 0.99, -2), Vector(0, 0, 1))
    xs = Intersections(
        Intersection(1.8589, shape))
    comps = xs[0].prepare_computations(r, xs)
    reflectance = comps.schlick()
    assert approx_eq(0.48873, reflectance)

def test_shade_hit_with_a_reflective_transparent_material():
    rtot = math.sqrt(2)/2
    w = default_world()
    r = Ray(Point(0, 0, -3), Vector(0, -rtot, rtot))
    
    floor = Plane()
    floor.transform = translation(0, -1, 0)
    floor.material.reflective = 0.5
    floor.material.transparency = 0.5
    floor.material.refractive_index = 1.5
    w.add(floor)
    
    ball = Sphere()
    ball.material.color = Color(1, 0, 0)
    ball.material.ambient = 0.5
    ball.transform = translation(0, -3.5, -0.5)
    w.add(ball)
    
    xs = Intersections(
        Intersection(math.sqrt(2), floor))
    comps = xs[0].prepare_computations(r, xs)
    color = w.shade(comps, 5)
    assert Color(0.93391, 0.69643, 0.69243) == color
    
def test_an_intersection_can_encapsulate_u_and_v():
    shape = Triangle(
        Point(0, 1, 0),
        Point(-1, 0, 0),
        Point(1, 0, 0))
        
    i = Intersection(3.5, shape, 0.2, 0.4)
    assert 0.2 == i.u
    assert 0.4 == i.v