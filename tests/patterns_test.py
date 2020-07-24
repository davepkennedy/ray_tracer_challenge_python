from ..rt import Color
from ..rt import Pattern, GradientPattern, StripePattern, RingPattern, CheckersPattern
from ..rt import Point
from ..rt import Identity
from ..rt import translation, scaling
from ..rt import Sphere

class PatternForTest (Pattern):
    def pattern_at(self, pt):
        return Color(pt.x, pt.y, pt.z)

def test_the_default_pattern_transformation():
    pattern = PatternForTest()
    assert Identity(4) == pattern.transform
    
def test_applying_a_pattern_transformation():
    transformation = translation(1, 2, 3)
    pattern = PatternForTest()
    pattern.transform = transformation
    assert transformation == pattern.transform
    
def test_a_pattern_with_an_object_transformation():
    shape = Sphere()
    shape.transform = scaling(2, 2, 2)
    pattern = PatternForTest()
    c = pattern.pattern_at_object(shape, Point(2, 3, 4))
    assert Color(1, 1.5, 2) == c
    
def test_a_pattern_with_a_pattern_transformation():
    shape = Sphere()
    pattern = PatternForTest()
    pattern.transform = scaling(2, 2, 2)
    c = pattern.pattern_at_object(shape, Point(2, 3, 4))
    assert Color(1, 1.5, 2) == c
    
def test_a_pattern_with_both_an_object_and_pattern_transformation():
    shape = Sphere()
    shape.transform = scaling(2, 2, 2)
    pattern = PatternForTest()
    pattern.transform = translation(0.5, 1, 1.5)
    c = pattern.pattern_at_object(shape, Point(2.5, 3, 3.5))
    assert Color(0.75, 0.5, 0.25) == c


def test_creating_a_stripe_pattern():
    pattern = StripePattern(Color.WHITE, Color.BLACK)
    assert Color.WHITE == pattern.a
    assert Color.BLACK, pattern.b

def test_a_stripe_pattern_is_constant_in_y():
    shape = Sphere()
    pattern = StripePattern(Color.WHITE, Color.BLACK)
    assert Color.WHITE == pattern.pattern_at_object(shape, Point(0, 0, 0))
    assert Color.WHITE == pattern.pattern_at_object(shape, Point(0, 1, 0))
    assert Color.WHITE == pattern.pattern_at_object(shape, Point(0, 2, 0))

def test_a_stripe_pattern_is_constant_in_z():
    shape = Sphere()
    pattern = StripePattern(Color.WHITE, Color.BLACK)
    assert Color.WHITE == pattern.pattern_at_object(shape, Point(0, 0, 0))
    assert Color.WHITE == pattern.pattern_at_object(shape, Point(0, 0, 1))
    assert Color.WHITE == pattern.pattern_at_object(shape, Point(0, 0, 2))

def test_a_stripe_pattern_is_alternate_in_x():
    shape = Sphere()
    pattern = StripePattern(Color.WHITE, Color.BLACK)
    assert Color.WHITE == pattern.pattern_at_object(shape, Point(0, 0, 0))
    assert Color.WHITE == pattern.pattern_at_object(shape, Point(0.9, 0, 0))
    assert Color.BLACK == pattern.pattern_at_object(shape, Point(1, 0, 0))
    assert Color.BLACK == pattern.pattern_at_object(shape, Point(-0.1, 0, 0))
    assert Color.BLACK == pattern.pattern_at_object(shape, Point(-1, 0, 0))
    assert Color.WHITE == pattern.pattern_at_object(shape, Point(-1.1, 0, 0))

def test_stripes_with_an_object_transformation():
    shape = Sphere()
    shape.transform = scaling(2, 2, 2)
    
    pattern = StripePattern(Color.WHITE, Color.BLACK)
    c = pattern.pattern_at_object(shape, Point(1.5, 0, 0))
    assert Color.WHITE == c

def test_stripes_with_a_pattern_transformation():
    shape = Sphere()
    pattern = StripePattern(Color.WHITE, Color.BLACK)
    pattern.transform = scaling(2, 2, 2)
    
    c = pattern.pattern_at_object(shape, Point(1.5, 0, 0))
    assert Color.WHITE == c

def test_stripes_with_both_object_and_pattern_transformation():
    shape = Sphere()
    shape.transform = scaling(2, 2, 2)
    
    pattern = StripePattern(Color.WHITE, Color.BLACK)
    pattern.transform = scaling(2, 2, 2)
    
    c = pattern.pattern_at_object(shape, Point(1.5, 0, 0))
    assert Color.WHITE == c
        
def test_a_gradient_linearly_interpolates_between_two_colors():
    pattern = GradientPattern(Color.WHITE, Color.BLACK)
    assert Color.WHITE == pattern.pattern_at(Point(0, 0, 0))
    assert Color(0.75,0.75,0.75) == pattern.pattern_at(Point(0.25, 0, 0))
    assert Color(0.5, 0.5, 0.5) == pattern.pattern_at(Point(0.5, 0, 0))
    assert Color(0.25, 0.25, 0.25) == pattern.pattern_at(Point(0.75, 0, 0))
        
def test_a_ring_should_extend_in_both_x_and_z():
    pattern = RingPattern(Color.WHITE, Color.BLACK)
    assert Color.WHITE == pattern.pattern_at(Point(0, 0, 0))
    assert Color.BLACK == pattern.pattern_at(Point(1, 0, 0))
    assert Color.BLACK == pattern.pattern_at(Point(0, 0, 1))
    assert Color.BLACK == pattern.pattern_at(Point(0.708, 0, 0.708))
        
def test_checkers_should_extend_in_x():
    pattern = CheckersPattern(Color.WHITE, Color.BLACK)
    assert Color.WHITE == pattern.pattern_at(Point(0, 0, 0))
    assert Color.WHITE == pattern.pattern_at(Point(0.99, 0, 0))
    assert Color.BLACK == pattern.pattern_at(Point(1.01, 0, 0))
        
def test_checkers_should_extend_in_y():
    pattern = CheckersPattern(Color.WHITE, Color.BLACK)
    assert Color.WHITE == pattern.pattern_at(Point(0, 0, 0))
    assert Color.WHITE == pattern.pattern_at(Point(0, 0.99, 0))
    assert Color.BLACK == pattern.pattern_at(Point(0, 1.01, 0))
        
def test_checkers_should_extend_in_z():
    pattern = CheckersPattern(Color.WHITE, Color.BLACK)
    assert Color.WHITE == pattern.pattern_at(Point(0, 0, 0))
    assert Color.WHITE == pattern.pattern_at(Point(0, 0, 0.99))
    assert Color.BLACK == pattern.pattern_at(Point(0, 0, 1.01))