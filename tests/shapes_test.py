from ..rt.shape import Shape
from ..rt import Intersections
from ..rt import BoundingBox
from ..rt import Point, Vector
from ..rt import translation, scaling, rotation_z, rotation_y, rotation_z
from ..rt import Material
from ..rt import Ray
from ..rt import Identity
from ..rt import Group
from ..rt import Sphere

import math

class ShapeFixture(Shape):
    __slots__ = ['saved_ray']

    def __init__(self):
        super().__init__()
        self.saved_ray = None

    def local_normal_at(self, pt, i):
        return pt

    def intersects_int(self, r):
        self.saved_ray = r
        return Intersections()
        
    def bounds(self):
        return BoundingBox(
            Point(-1, -1, -1),
            Point(1, 1, 1))
            

def test_the_default_transformation():
    shape = ShapeFixture()
    assert Identity(4) == shape.transform
    
def test_assigning_a_transformation():
    shape = ShapeFixture()
    shape.transform = translation (2, 3, 4)
    assert translation(2, 3, 4) == shape.transform
    
def test_the_default_material():
    s = ShapeFixture()
    assert Material() == s.material
    
def test_assigning_a_material():
    m = Material()
    m.ambient = 1
    
    s = ShapeFixture()
    s.material = m
    
    assert m == s.material
    
def test_intersecting_a_scaled_shaped_with_a_ray():
    ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = ShapeFixture()
    shape.transform = scaling(2, 2, 2)
    
    xs = shape.intersects(ray)
    assert Point(0, 0, -2.5) == shape.saved_ray.origin
    assert Vector(0, 0, 0.5) == shape.saved_ray.direction
    
def test_intersecting_a_translated_shape_with_a_ray():
    ray = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = ShapeFixture()
    shape.transform = translation(5, 0, 0)
    xs = shape.intersects(ray)
    
    assert Point(-5, 0, -5) == shape.saved_ray.origin
    assert Vector(0, 0, 1) == shape.saved_ray.direction

def test_computing_the_normal_on_a_translated_shape():
    shape = ShapeFixture()
    shape.transform = translation(0, 1, 0)
    
    n = shape.normal_at(Point(0, 1.70711, -0.70711), None)
    assert Vector(0, 0.70711, -0.70711) == n
    
def test_computing_the_normal_on_a_transformed_shape():
    matrix = scaling(1, 0.5, 1) * rotation_z(math.pi / 5)
    shape = ShapeFixture()
    shape.transform = matrix
    
    n = shape.normal_at(Point(0, math.sqrt(2) / 2, -math.sqrt(2) / 2), None)
    assert Vector(0, 0.97014, -0.24254) == n

def test_a_shape_has_a_parent_attribute():
    s = ShapeFixture()
    assert None == s.parent
    
def test_converting_a_point_from_world_to_object_space():
    g1 = Group()
    g1.transform = rotation_y(math.pi / 2)
    
    g2 = Group()
    g2.transform = scaling(2, 2, 2)
    
    g1.add(g2)
    s = Sphere()
    s.transform = translation(5, 0, 0)
    
    g2.add(s)
    
    p = s.world_to_object(Point(-2, 0, -10))
    assert Point(0, 0, -1) == p
        
def test_converting_a_normal_from_object_to_world_space():
    rtot = math.sqrt(3) / 3.0
    g1 = Group()
    g1.transform = rotation_y(math.pi / 2)
    
    g2 = Group()
    g2.transform = scaling(1, 2, 3)
    g1.add(g2)
    
    s = Sphere()
    s.transform = translation(5,0,0)
    g2.add(s)
    
    n = s.normal_to_world(Vector(rtot, rtot, rtot))
    assert Vector(0.2857, 0.4286, -0.8571) == n
    
def test_finding_the_normal_on_a_child_object():
    g1 = Group()
    g1.transform = rotation_y(math.pi / 2)
    
    g2 = Group()
    g2.transform = scaling(1, 2, 3)
    g1.add(g2)
    
    s = Sphere()
    s.transform = translation(5, 0, 0)
    g2.add(s)
    
    n = s.normal_at(Point(1.7321, 1.1547, -5.5774), None)
    assert Vector(0.2857, 0.4286, -0.8571) == n

def test_querying_a_shapes_bounding_box_in_its_parents_space():
    shape = Sphere()
    shape.transform = translation(1, -3, 5) * scaling(0.5, 2, 4)
    
    box = shape.parent_space_bounds()
    assert Point(0.5, -5, 1) == box.min
    assert Point(1.5, -1, 9) == box.max

def test_subdividing_a_primitive_does_nothing():
    shape = Sphere()
    shape.divide(1)
    assert isinstance(shape, Sphere)