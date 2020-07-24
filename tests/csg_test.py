from ..rt import Sphere
from ..rt import Cube
from ..rt import CSG, union_operation, difference_operation, operation_from_string
from ..rt import Ray
from ..rt import Point, Vector
from ..rt import translation
from ..rt import Intersection, Intersections

from .shapes_test import ShapeFixture

import pytest

def test_csg_is_created_with_an_operation_and_two_shapes():
    s1 = Sphere()
    s2 = Cube()
    c = CSG(union_operation, s1, s2)
    
    assert union_operation == c.operation
    assert s1 == c.left
    assert s2 == c.right
    assert c == s1.parent
    assert c == s2.parent
        
@pytest.mark.parametrize("op, lhit, inl, inr, result", [
        ("union", True, True, True, False),
        ("union", True, True, False, True),
        ("union", True, False, True, False),
        ("union", True, False, False, True),
        ("union", False, True, True, False),
        ("union", False, True, False, False),
        ("union", False, False, True, True),
        ("union", False, False, False, True),

        ("intersection", True, True, True, True),
        ("intersection", True, True, False, False),
        ("intersection", True, False, True, True),
        ("intersection", True, False, False, False),
        ("intersection", True, True, True, True),
        ("intersection", False, True, False, True),
        ("intersection", False, False, True, False),
        ("intersection", False, False, False, False),

        ("difference", True, True, True, False),
        ("difference", True, True, False, True),
        ("difference", True, False, True, False),
        ("difference", True, False, False, True),
        ("difference", False, True, True, True),
        ("difference", False, True, False, True),
        ("difference", False, False, True, False),
        ("difference", False, False, False, False)])
def test_EvaluatingTheRuleForACAGOperation(
    op, lhit, inl, inr, result):
    
    assert result == operation_from_string(op)(lhit, inl, inr)
        
@pytest.mark.parametrize('operation,x0,x1', [
    ("union", 0, 3),
    ("intersection", 1, 2),
    ("difference", 0, 1)])
def test_FilteringAListOfIntersections(operation, x0, x1):
    s1 = Sphere()
    s2 = Cube()
    
    c = CSG(operation_from_string(operation), s1, s1)
    xs = Intersections(
        Intersection(1, s1),
        Intersection(2, s2),
        Intersection(3, s1),
        Intersection(4, s2))
    result = c.filter_intersections(xs)
    assert 2 == len(result)
    assert xs[x0] == result[0]
    assert xs[x1] == result[1]

def test_ARayMissesACSGObject():
    c = CSG(union_operation, Sphere(), Cube())
    r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
    xs = c.intersects(r)
    assert 0 == len(xs)
        
def test_ARayHitsACSGObject():
    s1 = Sphere()
    s2 = Sphere()
    s2.transform = translation(0, 0, 0.5)
    
    c = CSG(union_operation, s1, s2)
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = c.intersects(r)
    
    assert 2 == len(xs)
    assert 4 == xs[0].t
    assert s1 == xs[0].shape
    assert 6.5 == xs[1].t
    assert s2 == xs[1].shape
        
def test_ACSGShapeHasABoundingBoxThatContainsItsChildren():
    left = Sphere()
    right = Sphere()
    right.transform = translation(2, 3, 4)
    
    shape = CSG(difference_operation, left, right)
    box = shape.bounds()
    assert Point(-1, -1, -1) == box.min
    assert Point(3, 4, 5) == box.max
        
def test_IntersectingRayAndCsgDoesntTestChildrenIfBoxIsMissed():
    left = ShapeFixture()
    right = ShapeFixture()
    shape = CSG(difference_operation, left, right)
    r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
    xs = shape.intersects(r)
    assert None == left.saved_ray
    assert None == right.saved_ray
    
def testIntersectingRayAndCsgTestsChildrenIfBoxIsHit():
    left = ShapeFixture()
    right = ShapeFixture()
    shape = CSG(difference_operation, left, right)
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = shape.intersects(r)
    assert None != left.saved_ray
    assert None != right.saved_ray
        
def SubdividingACSGShapeSubdividesItsChildren():
    s1 = Sphere()
    s1.transform = translation(-1.5, 0, 0)
    
    s2 = Sphere()
    s2.transform = translation(1.5, 0, 0)
    
    left = Group.Of(s1, s2)
    
    s3 = Sphere()
    s3.transform = translation(0, 0, -1.5)
    
    s4 = Sphere()
    s4.transform = translation(0, 0, 1.5)
    
    right = Group(s3, s4)
    
    shape = CSG(difference_operation, left, right)
    shape.divide(1)
    assert Group(s1), left[0]
    assert Group(s2), left[1]
    assert Group(s3), right[0]
    assert Group(s4), right[1]