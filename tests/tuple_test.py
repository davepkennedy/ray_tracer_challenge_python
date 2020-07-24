from ..rt import Tuple, Point, Vector
import math

def test_A_tuple_with_W_1_0_is_a_point():
	a = Tuple(4.3, -4.2, 3.1, 1.0)
	assert 4.3 == a.x
	assert -4.2 == a.y
	assert 3.1 == a.z
	assert 1.0 == a.w

	assert a.is_point
	assert not a.is_vector

def test_tuple_with_w_0_0_is_a_vector():
	a = Tuple(4.3, -4.2, 3.1, 0)
	assert 4.3 == a.x
	assert -4.2 == a.y
	assert 3.1 == a.z
	assert 0.0 == a.w

	assert not a.is_point
	assert a.is_vector

def test_Point_creates_a_tuple_with_w_1():
	a = Point(1.0, 2.0, 3.0)
	assert 1.0 == a.x
	assert 2.0 == a.y
	assert 3.0 == a.z
	assert 1.0 == a.w

def test_Vector_creates_a_tuple_with_w_0():
	a = Vector(1.0, 2.0, 3.0)
	assert 1.0 == a.x
	assert 2.0 == a.y
	assert 3.0 == a.z
	assert 0.0 == a.w

def test_adding_two_tuples():
	a = Tuple(3.0, -2.0, 5.0, 1.0)
	b = Tuple(-2.0, 3.0, 1.0, 0.0)
	assert Tuple(1.0, 1.0, 6.0, 1.0) == a + b

def test_subtracting_two_points():
	a = Point(3.0, 2.0, 1.0)
	b = Point(5.0, 6.0, 7.0)
	assert Vector(-2.0, -4.0, -6.0) == a - b

def test_subtracting_a_vector_from_a_point():
	a = Point(3.0, 2.0, 1.0)
	b = Vector(5.0, 6.0, 7.0)
	assert Point(-2.0, -4.0, -6.0) == a - b

def test_subtracting_two_vectors():
	a = Vector(3.0, 2.0, 1.0)
	b = Vector(5.0, 6.0, 7.0)
	assert Vector(-2.0, -4.0, -6.0) == a - b

def test_negating_a_tuple():
	a = Tuple(1.0, -2.0, 3.0, -4.0)
	assert Tuple(-1.0, 2.0, -3.0, 4.0) == -a

def test_multiply_tuple_by_scalar():
	a = Tuple(1.0, -2.0, 3.0, -4.0)
	assert Tuple(3.5, -7.0, 10.5, -14.0) == a * 3.5

def test_multiply_tuple_by_fraction():
	a = Tuple(1.0, -2.0, 3.0, -4.0)
	assert Tuple(0.5, -1.0, 1.5, -2.0) == a * 0.5

def test_dividing_tuple_by_scalar():
	a = Tuple(1.0, -2.0, 3.0, -4.0)
	assert Tuple(0.5, -1.0, 1.5, -2.0) == a / 2.0

def test_computing_the_magnitude_of_vector_1_0_0():
	a = Vector(1.0, 0.0, 0.0)
	assert 1.0 == a.magnitude()

def test_computing_the_magnitude_of_vector_0_1_0():
	a = Vector(0.0, 1.0, 0.0)
	assert 1.0 == a.magnitude()

def test_computing_the_magnitude_of_vector_0_0_1():
	a = Vector(0.0, 0.0, 1.0)
	assert 1.0 == a.magnitude()

def test_computing_the_magnitude_of_vector_1_2_3():
	a = Vector(1.0, 2.0, 3.0)
	assert math.sqrt(14.0), a.magnitude()

def test_computing_the_magnitude_of_vector_n1_n2_n3():
	a = Vector(-1.0, -2.0, -3.0)
	assert math.sqrt(14.0) == a.magnitude()

def test_normalizing_vector_4_0_0_is_vector_1_0_0():
	a = Vector(4.0, 0.0, 0.0)
	assert Vector(1.0, 0.0, 0.0) == a.normalize()

def test_normalizing_vector_1_2_3():
	a = Vector(1.0, 2.0, 3.0)
	assert Vector(
		1.0/math.sqrt(14.0),
		2.0/math.sqrt(14.0),
		3.0/math.sqrt(14.0)
	) == a.normalize()

def test_magnitude_of_normalized_vector():
	a = Vector(1.0, 2.0, 3.0)
	assert 1.0 == a.normalize().magnitude()

def test_dot_product_of_two_tuples():
	a = Vector(1.0, 2.0, 3.0)
	b = Vector(2.0, 3.0, 4.0)
	assert 20.0 == a.dot(b)

def test_cross_product_of_two_vectors():
	a = Vector(1.0, 2.0, 3.0)
	b = Vector(2.0, 3.0, 4.0)

	assert Vector(-1.0, 2.0, -1.0) == a.cross(b)
	assert Vector(1.0, -2.0, 1.0) == b.cross(a)

def test_tuple_equivalent_to_same_values():
	a = Tuple(1,2,3,4)
	b = (1,2,3,4)
	assert a == b

def test_tuple_not_equivalent_to_different_values():
	a = Tuple(1,2,3,4)
	b = (2,3,4,5)
	assert a != b

# Chapter 6
def test_reflecting_a_vector_approaching_at_45_deg():
	v = Vector(1, -1, 0)
	n = Vector(0, 1, 0)
	r = v.reflect_on(n)
	
	assert Vector(1, 1, 0) == r
	
# Chapter 6
def test_reflecting_a_vector_approaching_a_slanted_surface():
	rtot = math.sqrt(2) / 2.0
	v = Vector(0, -1, 0)
	n = Vector(rtot, rtot, 0)
	r = v.reflect_on(n)
	assert Vector(1, 0, 0) == r