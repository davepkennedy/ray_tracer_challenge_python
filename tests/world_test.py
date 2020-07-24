from ..rt import World, default_world

from ..rt import PointLight, lighting
from ..rt import Point, Vector
from ..rt import Color
from ..rt import Material
from ..rt import Sphere, Plane
from ..rt import scaling, translation
from ..rt import Ray
from ..rt import Intersection, Intersections

from .patterns_test import PatternForTest
import math

ROOT_TWO=math.sqrt(2)
ROOT_TWO_OVER_TWO = ROOT_TWO/2

# Chapter 7
def test_creating_a_world():
    world = World()
    
    assert not world.has_light()
    assert world.is_empty()
    
# Chapter 7
def test_default_world():
    light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
    s1 = Sphere()
    material = Material()
    material.color = Color(0.8, 1.0, 0.6)
    material.diffuse = 0.7
    material.specular = 0.2
    s1.material = material

    s2 = Sphere()
    s2.transform = scaling(0.5, 0.5, 0.5)
    
    world = default_world()
    
    assert light == world.light
    assert True == world.contains(s1)
    assert True == world.contains(s2)

# Chapter 7
def test_intersect_a_world_with_a_ray():
    world = default_world()
    ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = world.intersections(ray)

    assert len(xs) == 4
    assert xs[0].t == 4
    assert xs[1].t == 4.5
    assert xs[2].t == 5.5
    assert xs[3].t == 6

def test_shading_an_intersection():
    w = default_world()
    r = Ray(Point(0,0,-5), Vector(0,0,1))
    shape = w[0]
    i = Intersection(4, shape)
    comps = i.prepare_computations(r)
    c = w.shade(comps,5)
    assert Color(0.38066, 0.47583, 0.2855) == c

def test_shading_an_intersection_from_the_inside():
    w = default_world()
    w.light = PointLight(Point(0,0.25,0), Color(1,1,1))
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = w[1]
    i = Intersection(0.5, shape)
    comps = i.prepare_computations(r)
    c = w.shade(comps,5)
    assert Color(0.90498, 0.90498, 0.90498), c
 
def test_the_color_when_a_ray_misses():
    w = default_world()
    r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
    assert Color(0, 0, 0) == w.color_at(r,5)

def test_the_color_when_a_ray_hits():
    w = default_world()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    assert Color(0.38066, 0.47583, 0.2855) == w.color_at(r,5)
    
def test_the_color_with_an_intersection_behind_the_ray():
    w = default_world()
    outer = w[0]
    outer.material.ambient = 1
    
    inner = w[1]
    inner.material.ambient = 1
    
    r = Ray(Point(0, 0, 0.75), Vector(0, 0, -1))
    c = w.color_at(r,5)
    
    assert inner.material.color == c
    
def test_there_is_no_shadow_when_nothing_is_collinear_with_point_and_light():
    world = default_world()
    p = Point(0, 10, 0)
    assert not world.is_shadowed(p)
        
def test_when_an_object_is_between_the_point_and_the_light():
    w = default_world()
    p = Point(10, -10, 10)
    assert w.is_shadowed(p)
        
def test_there_is_no_shadow_when_an_object_is_behind_the_light():        
    world = default_world()
    p = Point(0, 10, 0)
    assert not world.is_shadowed(p)
        
def test_there_is_no_shadow_when_an_object_is_behind_the_point():
    world = default_world()
    p = Point(0, 10, 0)
    assert not world.is_shadowed(p)
        
def test_shade_hit_is_given_an_intersection_in_shadow():
    w = World()
    w.light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    s1 = Sphere()
    w.add(s1)
    s2 = Sphere()
    
    s2.transform = translation(0, 0, 10)
    
    w.add(s2)
    ray = Ray(Point(0, 0, 5), Vector(0, 0, 1))
    i = Intersection(4, s2)
    comps = i.prepare_computations(ray)
    c = w.shade(comps,5)
    assert Color(0.1, 0.1, 0.1) == c
        
def test_the_reflected_color_for_a_nonreflective_material():
    w = default_world()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = w[1]
    shape.material.ambient = 1
    i = Intersection(1, shape)
    comps = i.prepare_computations(r)
    color = w.reflected_color(comps,5)
    assert Color.BLACK == color
        
def test__the_reflected_color_for_a_reflective_material():
    w = default_world()
    shape = Plane()
    shape.material.reflective = 0.5
    shape.transform = translation(0, -1, 0)
    w.add(shape)
    r = Ray(Point(0, 0, -3), Vector(0, -ROOT_TWO_OVER_TWO, ROOT_TWO_OVER_TWO))
    i = Intersection(math.sqrt(2), shape)
    comps = i.prepare_computations(r)
    color = w.reflected_color(comps,5)
    assert Color(0.19032, 0.2379, 0.14274) == color
    
def test_shade_hit_with_a_reflective_material():
    w = default_world()
    shape = Plane()
    shape.material.reflective = 0.5
    shape.transform = translation(0, -1, 0)
    w.add(shape)
    r = Ray(Point(0, 0, -3), Vector(0, -ROOT_TWO_OVER_TWO, ROOT_TWO_OVER_TWO))
    i = Intersection(math.sqrt(2), shape)
    comps = i.prepare_computations(r)
    color = w.shade(comps,5)
    assert Color(0.87677, 0.92436, 0.82918) == color

# [Timeout (300)]
def test_color_at_with_mutually_reflective_surfaces():
    w = World()
    w.light = PointLight(Point(0, 0, 0), Color.WHITE)

    lower = Plane()
    lower.material.reflective = 1
    lower.transform = translation(0, -1, 0)
    w.add(lower)

    upper = Plane()
    upper.material.reflective = 1
    upper.transform = translation(0, 1, 0)
    w.add(upper)

    ray = Ray(Point(0, 0, 0), Vector(0, 1, 0))
    w.color_at(ray,5)
        
def test_TheReflectiveColorAtTheMaximumRecursionDepth():
    w = default_world()
    
    shape = Plane()
    shape.material.reflective = 1
    shape.transform = translation(0, -1, 0)
    w.add(shape)

    r = Ray(Point(0, 0, -3), Vector(0, -ROOT_TWO_OVER_TWO, ROOT_TWO_OVER_TWO))
    i = Intersection(ROOT_TWO, shape)
    comps = i.prepare_computations(r)
    color = w.reflected_color(comps, 0)
    assert Color.BLACK == color
        
def test_TheRefractedColorWithAnOpaqueSurface():
    w = default_world()
    shape = w[0]
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = Intersections(
        Intersection(4, shape),
        Intersection(6, shape))
    comps = xs[0].prepare_computations(r, xs)
    c = w.refracted_color(comps, 5)
    assert Color.BLACK == c
        
def test_TheRefractedColorAtTheMaximumRecursiveDepth():
    w = default_world()
    shape = w[0]
    shape.material.transparency = 1.0
    shape.material.refractive_index = 1.5
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = Intersections(
        Intersection(4, shape),
        Intersection(6, shape))
    comps = xs[0].prepare_computations(r, xs)
    c = w.refracted_color(comps, 0)
    assert Color.BLACK == c
        
def test_TheRefractedColorUnderTotalInternalReflection():
    rtot = math.sqrt(2) / 2
    w = default_world()
    shape = w[0]
    shape.material.transparency = 1
    shape.material.refractive_index = 1.5
    r = Ray(Point(0, 0, -rtot), Vector(0, 1, 0))
    xs = Intersections(
        Intersection(-rtot, shape),
        Intersection(rtot, shape))
    comps = xs[1].prepare_computations(r, xs)
    c = w.refracted_color(comps, 5)
    assert Color.BLACK == c
        
def test_TheRefractedColorWithARefractedRay():
    w = default_world()
    A = w[0]
    A.material.ambient = 1
    A.material.pattern = PatternForTest()

    B = w[1]
    B.material.transparency = 1
    B.material.refractive_index = 1.5

    r = Ray(Point(0, 0, 0.1), Vector(0, 1, 0))
    xs = Intersections(
    Intersection(-0.9899,A),
    Intersection(-0.4899,B),
    Intersection(0.4899,B),
    Intersection(0.9899,A))

    comps = xs[2].prepare_computations(r, xs)
    c = w.refracted_color(comps, 5)
    assert Color(0, 0.99888, 0.04725) == c
        
def test_ShadeHitWithATransparentMaterial():
    w = default_world()

    floor = Plane()
    floor.transform = translation(0, -1, 0)
    floor.material.transparency = 0.5
    floor.material.refractive_index = 1.5
    w.add(floor)

    ball = Sphere()
    ball.material.color = Color(1, 0, 0)
    ball.material.ambient = 0.5
    ball.transform = translation(0, -3.5, -0.5)
    w.add(ball)

    r = Ray(Point(0, 0, -3), Vector(0, -ROOT_TWO_OVER_TWO, ROOT_TWO_OVER_TWO))
    xs = Intersections(Intersection(ROOT_TWO, floor))
    comps = xs[0].prepare_computations(r, xs)
    color = w.shade(comps, 5)
    assert Color(0.93642, 0.68642, 0.68642) == color