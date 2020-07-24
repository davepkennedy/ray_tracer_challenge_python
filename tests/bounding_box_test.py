from ..rt import BoundingBox
from ..rt import Point, Vector
from ..rt import Ray
from ..rt import rotation_x, rotation_y
from ..rt.linmath import POSITIVE_INFINITY as POS_INF

import pytest
import math

def test_creating_an_empty_bounding_box():
    box = BoundingBox()
    assert POS_INF == POS_INF
    assert Point.MAX == box.min
    assert Point.MIN == box.max
    
def test_creating_a_bounding_box_with_volume():
    box = BoundingBox(
        Point(-1, -2, -3),
        Point(1, 2, 3))
    assert Point(-1, -2, -3) == box.min
    assert Point(1, 2, 3) == box.max
    
def test_adding_points_to_an_empty_bounding_box():
    box = BoundingBox()
    box.add(Point(-5, 2, 0))
    box.add(Point(7, 0, -3))
    
    assert Point(-5, 0, -3) == box.min
    assert Point( 7, 2,  0) == box.max
    
def test_adding_one_bounding_box_to_another():
    box1 = BoundingBox(Point(-5, -2, 0), Point(7, 4, 4))
    box2 = BoundingBox(Point(8, -7, -2), Point(14, 2, 8))
    
    box1.add(box2)
    
    assert Point(-5, -7, -2) == box1.min
    assert Point(14, 4, 8) == box1.max

@pytest.mark.parametrize("px,py,pz, expect", [
        (5, -2, 0, True),
        (11, 4, 7, True),
        (8, 1, 3, True),
        (3, 0, 3, False),
        (8, -4, 3, False),
        (8, 1, -1, False),
        (13, 1, 3, False),
        (8, 5, 3, False),
        (8, 1, 8, False)
])
def test_checking_to_see_if_a_box_contains_a_given_point (px, py, pz, expect):
    box = BoundingBox(Point(5, -2, 0), Point(11, 4, 7))
    p = Point(px, py, pz)
    assert expect == box.contains(p)
    assert expect == (p in box)
    
@pytest.mark.parametrize('minx, miny, minz, maxx, maxy, maxz, expect', [
    (5, -2, 0, 11, 4, 7, True),
    (6, -1, 1,10, 3, 6, True),
    (4, -3, -1, 10, 3, 6, False),
    (6, -1, 1, 12, 5, 8, False)])
def test_checking_to_see_if_a_box_contains_a_given_box (
        minx, miny, minz, maxx, maxy, maxz, expect):
    box = BoundingBox(Point(5, -2, 0), Point(11, 4, 7))
    box2 = BoundingBox(Point(minx, miny, minz), Point(maxx, maxy, maxz))
    assert expect == box.contains(box2)
    assert expect == (box2 in box)
        
def test_transforming_a_bounding_box():
    box = BoundingBox(Point(-1, -1, -1), Point(1, 1, 1))
    matrix = rotation_x(math.pi / 4) * rotation_y(math.pi / 4)
    box2 = box.transform(matrix)
    assert Point(-1.4142, -1.7071, -1.7071) == box2.min
    assert Point(1.4142, 1.7071, 1.7071) == box2.max
        
@pytest.mark.parametrize('px,py,pz,dx,dy,dz,result', [        
        (5, 0.5, 0, -1, 0, 0, True),
        (-5, 0.5, 0, 1, 0, 0, True),
        (0.5, 5, 0,0, -1, 0, True),
        (0.5, -5, 0,0, 1, 0, True),
        (0.5, 0, 5,0, 0, -1, True),
        (0.5, 0, -5, 0, 0, 1, True),
        (0, 0.5, 0,0, 0, 1, True),
        (-2, 0, 0, 2, 4, 6, False),
        (0, -2, 0, 6, 2, 4, False),
        (0, 0, -2, 4, 6, 2, False),
        (2, 0, 2, 0, 0, -1, False),
        (0, 2, 2, 0, -1, 0, False),
        (2, 2, 0, -1, 0, 0, False)])
def test_intersecting_a_ray_with_a_bounding_box_at_the_origin(px, py, pz, dx, dy, dz, result):
    box = BoundingBox(Point(-1, -1, -1), Point(1, 1, 1))
    direction = Vector(dx, dy, dz).normalize()
    r = Ray(Point(px, py, pz), direction)
    
    assert result == box.intersects(r)
        
@pytest.mark.parametrize('px,py,pz,dx,dy,dz,result', [
        (15, 1, 2, -1, 0, 0, True),
        (-5, -1, 4, 1, 0, 0, True),
        (7, 6, 5, 0, -1, 0, True),
        (9, -5, 6, 0, 1, 0, True),
        (8, 2, 12, 0, 0, -1, True),
        (6, 0, -5, 0, 0, 1, True),
        (8, 1, 3.5, 0, 0, 1, True),
        (9, -1, -8, 2, 4, 6, False),
        (8, 3, -4, 6, 2, 4, False),
        (9, -1, -2, 4, 6, 2, False),
        (4, 0, 9, 0, 0, -1, False),
        (8, 6, -1, 0, -1, 0, False),
        (12, 5, 4, -1, 0, 0, False)])
def test_intersecting_a_ray_with_a_non_cubic_bounding_box(
        px, py, pz, dx, dy, dz, result):    
    box = BoundingBox(Point(5, -2, 0), Point(11, 4, 7))
    direction = Vector(dx, dy, dz).normalize()
    r = Ray(Point(px, py, pz), direction)
    assert result == box.intersects(r)

def test_splitting_a_perfect_cube():
    box = BoundingBox(Point(-1, -4, -5), Point(9, 6, 5))
    left, right = box.split()
    assert Point(-1, -4, -5) == left.min
    assert Point(4, 6, 5) == left.max
    assert Point(4, -4, -5) == right.min
    assert Point(9, 6, 5) == right.max
        
def test_splitting_an_x_wide_box():
    box = BoundingBox(Point(-1, -2, -3), Point(9, 5.5, 3))
    left, right = box.split()
    assert Point(-1, -2, -3) == left.min
    assert Point(4, 5.5, 3) == left.max
    assert Point(4, -2, -3) == right.min
    assert Point(9, 5.5, 3) == right.max
        
def test_splitting_a_y_wide_box() :
    box = BoundingBox(Point(-1, -2, -3), Point(5, 8, 3))
    left, right = box.split()
    assert Point(-1, -2, -3) == left.min
    assert Point(5, 3, 3) == left.max
    assert Point(-1, 3, -3) == right.min
    assert Point(5, 8, 3) == right.max
        
def test_splitting_a_z_wide_box():
    box = BoundingBox(Point(-1, -2, -3), Point(5, 3, 7))
    left, right = box.split()
    
    assert Point(-1, -2, -3) == left.min
    assert Point(5, 3, 2) == left.max
    assert Point(-1, -2, 2) == right.min
    assert Point(5, 3, 7) == right.max