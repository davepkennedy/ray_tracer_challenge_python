from ..rt import translation, scaling, rotation_x, rotation_y, rotation_z, shearing, view
from ..rt import Matrix, Identity
from ..rt import Point, Vector

import math

def test_transform_is_as_expected():
    assert Matrix(
        1, 0, 0, 5,
        0, 1, 0, -3,
        0, 0, 1, 2,
        0, 0, 0, 1
        ) == translation(5, -3, 2)


def test_multiply_by_translation_matrix():
	transform = translation(5, -3, 2)
	point = Point(-3, 4, 5)
	assert Point(2, 1, 7) == transform * point

def test_multiply_by_the_inverse_of_translation_matrix():
	transform = translation(5, -3, 2)
	inv = transform.inverse()
	point = Point(-3, 4, 5)
	assert Point(-8, 7, 3) == inv * point


def test_translation_does_not_affect_vectors():
	transform = translation(5, -3, 2)
	vector = Vector(-3, 4, 5)
	assert vector == transform * vector
	
def test_ScalingMatrixAppliedToPoint():
	transform = scaling(2, 3, 4)
	point = Point(-4, 6, 8)
	assert Point(-8, 18, 32) == transform * point

def test_scaling_matrix_applied_to_Vector():
	transform = scaling(2, 3, 4)
	vector = Vector(-4, 6, 8)
	assert Vector(-8, 18, 32) == transform * vector

def test_inverse_scaling_matrix_applied_to_vector():
	transform = scaling(2, 3, 4).inverse()
	vector = Vector(-4, 6, 8)
	assert Vector(-2,2,2) == transform * vector

def test_reflection_is_scaling_by_negative_value():
	transform = scaling(-1,1,1)
	point = Point(2,3,4)
	assert Point(-2,3,4) == transform * point
	
def test_rotation_around_x_axis():
	point = Point(0, 1, 0)
	half_quarter = rotation_x(math.pi / 4)
	full_quarter = rotation_x(math.pi / 2)
	
	assert Point(0, math.sqrt(2) / 2, math.sqrt(2) / 2) == half_quarter * point
	assert Point(0, 0, 1) == full_quarter * point

def test_inverse_rotation_around_x_axis_is_opposite_direction():
	point = Point(0, 1, 0)
	half_quarter = rotation_x(math.pi / 4).inverse()
	
	assert Point(0, math.sqrt(2) / 2, -math.sqrt(2) / 2) == half_quarter * point

def test_rotation_around_y_axis():
	point = Point(0, 0, 1)
	half_quarter = rotation_y(math.pi / 4)
	full_quarter = rotation_y(math.pi / 2)
	
	assert Point(math.sqrt(2) / 2, 0, math.sqrt(2) / 2) == half_quarter * point
	assert Point(1, 0, 0) == full_quarter * point
		
def test_rotation_around_z_axis():
	point = Point(0, 1, 0)
	half_quarter = rotation_z(math.pi / 4)
	full_quarter = rotation_z(math.pi / 2)
	
	assert Point(-math.sqrt(2) / 2, math.sqrt(2) / 2, 0) == half_quarter * point
	assert Point(-1, 0, 0) == full_quarter * point
		
def test_shearing_moves_x_in_proportion_to_y():
	transform = shearing(1, 0, 0, 0, 0, 0)
	point = Point(2, 3, 4)
	assert Point(5, 3, 4) == transform * point
		
def test_shearing_moves_x_in_proportion_to_z():
	transform = shearing(0, 1, 0, 0, 0, 0)
	point = Point(2, 3, 4)
	assert Point(6, 3, 4), transform * point
		
def test_shearing_moves_y_in_proportion_to_x():
	transform = shearing(0, 0, 1, 0, 0, 0)
	point = Point(2, 3, 4)
	assert Point(2, 5, 4), transform * point
		
def test_shearing_moves_y_in_proportion_to_z():
	transform = shearing(0, 0, 0, 1, 0, 0)
	point = Point(2, 3, 4)
	assert Point(2, 7, 4), transform * point
		
def test_shearing_moves_z_in_proportion_to_x():
	transform = shearing(0, 0, 0, 0, 1, 0)
	point = Point(2, 3, 4)
	assert Point(2, 3, 6), transform * point
		
def test_shearing_moves_z_in_proportion_to_y():
	transform = shearing(0, 0, 0, 0, 0, 1)
	point = Point(2, 3, 4)
	assert Point(2, 3, 7), transform * point
	
def test_individual_transformations_are_applied_in_sequence():
	p = Point(1, 0, 1)
	A = rotation_x(math.pi / 2)
	B = scaling(5, 5, 5)
	C = translation(10, 5, 7)
	p2 = A * p
	assert Point(1, -1, 0) == p2
	p3 = B * p2
	assert Point(5, -5, 0) == p3
	p4 = C * p3
	assert Point(15, 0, 7) == p4
		
def test_chained_transformations_must_be_applied_in_reverse_order():
	p = Point(1, 0, 1)
	A = rotation_x(math.pi / 2)
	B = scaling(5, 5, 5)
	C = translation(10, 5, 7)
	T = C * B * A
	assert Point(15, 0, 7) == T * p
	
def test_transformation_matrix_for_the_default_orientation():
	source = Point(0, 0, 0)
	to = Point(0, 0, -1)
	up = Vector(0, 1, 0)
	t = view(source, to, up)
	assert Identity(4) == t
	
def test_a_view_transformation_matrix_looking_in_positive_z_direction():
	source = Point(0, 0, 0)
	to = Point(0, 0, 1)
	up = Vector(0, 1, 0)
	t = view(source, to, up)
	assert scaling(-1, 1, -1) == t

def test_the_view_transform_moves_the_world():
	source = Point(0, 0, 8)
	to = Point(0, 0, 0)
	up = Vector(0, 1, 0)
	t = view(source, to, up)
	assert translation(0, 0, -8) == t
	
def test_an_arbitrary_view_transformation():
	source = Point(1, 3, 2)
	to = Point(4, -2, 8)
	up = Vector(1, 1, 0)
	t = view(source, to, up)
	m = Matrix(
		-0.50709, 0.50709, 0.67612, -2.36643,
		0.76772, 0.60609, 0.12122, -2.82843,
		-0.35857, 0.59761, -0.71714, 0.0000,
		0.00000, 0.00000, 0.00000, 1.00000)