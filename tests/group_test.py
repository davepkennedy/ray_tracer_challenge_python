from ..rt import Group
from ..rt import Identity
from ..rt import Ray
from ..rt import Point, Vector
from ..rt import translation, scaling
from ..rt import Sphere, Cylinder

from .shapes_test import ShapeFixture

def test_creating_a_new_group():
    g = Group()
    assert Identity(4) == g.transform
    assert 0 == len(g)
        
def test_adding_a_child_to_a_group():
    g = Group()
    s = ShapeFixture()
    
    g.add(s)
    
    assert 0 != len(g)
    assert s in g
    assert g == s.parent
        

def test_intersecting_a_ray_with_an_empty_group():
    g = Group()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    xs = g.intersects(r)
    assert 0 == len(xs)
        

def test_intesecting_a_ray_with_a_non_empty_group():
    g = Group()
    s1 = Sphere()
    s2 = Sphere()
    s2.transform = translation(0, 0, -3)
    
    s3 = Sphere()
    s3.transform = translation(5, 0, 0)
    
    g.add(s1)
    g.add(s2)
    g.add(s3)
    
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    
    xs = g.intersects(r)
    
    assert 4 == len(xs)
    assert s2 == xs[0].shape
    assert s2 == xs[1].shape
    assert s1 == xs[2].shape
    assert s1 == xs[3].shape
        
def test_intersecting_a_transformed_group():
    g = Group()
    g.transform = scaling(2, 2, 2)
    
    s = Sphere()
    s.transform = translation(5, 0, 0)
    
    g.add(s)
    r = Ray(Point(10, 0, -10), Vector(0, 0, 1))
    xs = g.intersects(r)
    assert 2 == len(xs)
        
def test_a_group_has_a_bounding_box_that_contains_its_children():
    s = Sphere()
    s.transform = translation(2, 5, -3) * scaling(2, 2, 2)
    
    c = Cylinder()
    c.minimum = -2
    c.maximum = 2
    c.transform = translation(-4, -1, 4) * scaling(0.5, 1, 0.5)
    
    shape = Group()
    shape.add(s)
    shape.add(c)
    
    box = shape.bounds()
    assert Point(-4.5, -3, -5) == box.min
    assert Point(4, 7, 4.5) == box.max
        
def test_intersecting_ray_and_group_doesnt_test_children_if_box_is_missed() :
    child = ShapeFixture()
    shape = Group()
    shape.add(child)
    r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
    xs = shape.intersects(r)
    assert None == child.saved_ray
        
def test_intersecting_ray_group_tests_children_if_box_is_hit():
    child = ShapeFixture()
    shape = Group()
    shape.add(child)
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = shape.intersects(r)
    assert None != child.saved_ray
    
def test_partitioning_a_groups_children():
    s1 = Sphere()
    s1.transform = translation(-2, 0, 0)
    
    s2 = Sphere()
    s2.transform = translation(2, 0, 0)
    
    s3 = Sphere()
    g = Group(s1, s2, s3)
    
    left, right = g.partition_children()
    assert Group(s3) == g
    assert s1 in left
    assert s2 in right
        
def test_creating_a_sub_group_from_a_list_of_children():
    s1 = Sphere()
    s2 = Sphere()
    g = Group()
    g.make_subgroup(s1, s2)
    
    assert 1 == len(g)
    assert Group(s1, s2) == g[0]
        
def test_subdividing_a_group_partitions_its_children():
    s1 = Sphere()
    s1.transform = translation(-2, -2, 0)
    
    s2 = Sphere()
    s2.transform = translation(-2, 2, 0)
    
    s3 = Sphere()
    s3.transform = scaling(4, 4, 4)
    
    g = Group(s1, s2, s3)
    g.divide(1)
    
    assert s3 == g[0]
    
    subgroup = g[1]
    assert None != subgroup
    assert 2 == len(subgroup)
    
    assert Group(s1) == subgroup[0]
    assert Group(s2) == subgroup[1]
        

def test_subdividing_a_group_with_too_few_children():
    s1 = Sphere()
    s1.transform = translation(-2, 0, 0)
    
    s2 = Sphere()
    s2.transform = translation(2, 1, 0)
    
    s3 = Sphere()
    s3.transform = translation(2, -1, 0)
    
    subgroup = Group(s1, s2, s3)
    
    s4 = Sphere()
    g = Group(subgroup, s4)
    g.divide(3)
    
    assert subgroup == g[0]
    assert s4 == g[1]
    assert 2 == len(subgroup)
    assert Group(s1) == subgroup[0]
    assert Group(s2, s3) == subgroup[1]