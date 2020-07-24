from ..rt import Matrix, Identity

def test_construct_and_inspect_a_4_x_4_matrix():
	m = Matrix (
		1.0, 2.0, 3.0, 4.0,
		5.5, 6.5, 7.5, 8.5,
		9.0, 10.0, 11.0, 12.0,
		13.5, 14.5, 15.5, 16.5,
	)

	assert 1.0 == m[(0, 0)]
	assert 4.0 == m[(0, 3)]
	assert 5.5 == m[(1, 0)]
	assert 7.5 == m[(1, 2)]
	assert 13.5 == m[(3, 0)]
	assert 15.5 == m[(3, 2)]

def test_a_2_x_2_matrix_should_be_representable():
	m = Matrix(
		-3.0, 5.0,
		1.0, -2.0,
	)

	assert -3.0 == m[(0, 0)]
	assert 5.0 == m[(0, 1)]
	assert 1.0 == m[(1, 0)]
	assert -2.0 == m[(1, 1)]

def test_a_3_x_3_matrix_should_be_representable():
	m = Matrix(
		-3.0, 5.0, 0.0,
		1.0, -2.0, -7.0,
		0.0, 1.0, 1.0,
	)

	assert -3.0 == m[(0, 0)]
	assert -2.0 == m[(1, 1)]
	assert 1.0 == m[(2, 2)]

def test_matrix_equality_with_identical_matrices():
	matA = Matrix(
		1, 2, 3, 4,
		5, 6, 7, 8,
		9, 10, 11, 12,
		13, 14, 15, 16,
	)
	matB = Matrix(
		1, 2, 3, 4,
		5, 6, 7, 8,
		9, 10, 11, 12,
		13, 14, 15, 16,
	)
	assert matA == matB

def test_matrix_equality_with_different_matrices():
	matA = Matrix(
		1, 2, 3, 4,
		5, 6, 7, 8,
		8, 7, 6, 5,
		4, 3, 2, 1,
	)
	matB = Matrix(
		2, 3, 4, 5,
		6, 7, 8, 9,
		9, 8, 7, 6,
		5, 4, 3, 2,
	)
	assert matA != matB

def test_multiplying_two_matrices():
	matA = Matrix(
		1, 2, 3, 4,
		5, 6, 7, 8,
		9, 8, 7, 6,
		5, 4, 3, 2,
	)
	matB = Matrix(
		-2, 1, 2, 3,
		3, 2, 1, -1,
		4, 3, 6, 5,
		1, 2, 7, 8,
	)

	exp = Matrix(
		20, 22, 50, 48,
		44, 54, 114, 108,
		40, 58, 110, 102,
		16, 26, 46, 42,
	)
	matC = matA * matB
	assert exp == matC

def test_multiply_by_a_tuple():
	matrix = Matrix(
		1, 2, 3, 4,
		2, 4, 4, 2,
		8, 6, 4, 1,
		0, 0, 0, 1,
	)
	t = (1, 2, 3, 1)
	assert (18, 24, 33, 1) == matrix * t

def test_multiply_by_identity_matrix():
	matrix = Matrix(
		0, 1, 2, 4,
		1, 2, 4, 8,
		2, 4, 8, 16,
		4, 8, 16, 32,
	)

	assert matrix == matrix * Identity(4)

def test_multiply_identity_matrix_by_tuple():
	t = (1, 2, 3, 4)
	assert t == Identity(4) * t

def test_transpose_a_matrix():
	a = Matrix(
		0, 9, 3, 0,
		9, 8, 0, 8,
		1, 8, 5, 3,
		0, 0, 5, 8,
	)
	b = Matrix(
		0, 9, 1, 0,
		9, 8, 8, 0,
		3, 0, 5, 5,
		0, 8, 3, 8,
	)
	assert b == a.transpose()

def test_determinant_of_2_x_2():
	m = Matrix(
		1, 5,
		-3, 2,
	)
	assert 17.0 == m.determinant()

def test_submatrix_of_3_x_3_matrix_is_2_x_2_matrix():
	a = Matrix(
		1, 5, 0,
		-3, 2, 7,
		0, 6, -3
	)

	assert Matrix(
        -3, 2, 
        0, 6) == a.submatrix(0, 2)

def test_submatrix_of_4_x_4_matrix_is_3_x_3_matri():
	a = Matrix(
		-6, 1, 1, 6,
		-8, 5, 8, 6,
		-1, 0, 8, 2,
		-7, 1, -1, 1,
	)

	assert Matrix(-6, 1, 6,
		-8, 8, 6,
		-7, -1, 1) == a.submatrix(2, 1)

def test_minor_of_a_3_x_3_matrix():
	a = Matrix(
		3, 5, 0,
		2, -1, -7,
		6, -1, 5,
	)
	b = a.submatrix(1, 0)
	assert 25.0 == b.determinant()
	assert 25.0 == a.minor(1, 0)

def test_cofactor_of_a_3_x_3_matrix():
	a = Matrix(
		3, 5, 0,
		2, -1, -7,
		6, -1, 5,
	)

	assert -12.0 == a.minor(0, 0)
	assert -12.0 == a.cofactor(0, 0)

	assert 25.0 == a.minor(1, 0)
	assert -25.0 == a.cofactor(1, 0)

def test_calculating_the_determinant_of_a_3_x_3_matrix():
    a = Matrix(
        1, 2, 6,
        -5, 8, -4,
        2, 6, 4
    )
    assert 56.0 == a.cofactor(0, 0)
    assert 12.0 == a.cofactor(0, 1)
    assert -46.0 == a.cofactor(0, 2)
    assert -196.0 == a.determinant()

def test_calculating_the_determinant_of_a_4_x_4_matrix():
	a = Matrix(
		-2, -8, 3, 5,
		-3, 1, 7, 3,
		1, 2, -9, 6,
		-6, 7, 7, -9,
	)
	assert 690.0 == a.cofactor(0, 0)
	assert 447.0 == a.cofactor(0, 1)
	assert 210.0 == a.cofactor(0, 2)
	assert 51.0 == a.cofactor(0, 3)
	assert -4071.0 == a.determinant()

def test_an_invertible_matrix_for_invertibility():
	a = Matrix(
		6, 4, 4, 4,
		5, 5, 7, 6,
		4, -9, 3, -7,
		9, 1, 7, -6,
	)
	assert -2120.0 == a.determinant()
	assert a.is_invertible

def test_a_non_invertible_matrix_for_invertibility():
	a = Matrix(
		-4, 2, -2, -3,
		9, 6, 2, 6,
		0, -5, 1, -5,
		0, 0, 0, 0,
	)
	assert 0.0 == a.determinant()
	assert not a.is_invertible

def test_calculating_the_inverse_of_a_matrix():
	a = Matrix(
		-5, 2, 6, -8,
		1, -5, 1, 8,
		7, 7, -6, -7,
		1, -3, 7, 4,
	)
	b = a.inverse()

	assert 532.0 == a.determinant()
	assert -160.0, a.cofactor(2, 3)
	assert -160.0/532, b[(3, 2)]
	assert 105.0, a.cofactor(3, 2)
	assert 105.0/532.0, b[(2, 3)]
	assert Matrix(
		0.21805, 0.45113, 0.24060, -0.04511,
		-0.80827, -1.45677, -0.44361, 0.52068,
		-0.07895, -0.22368, -0.05263, 0.19737,
		-0.52256, -0.81391, -0.30075, 0.30639,
	) == b

def test_multiply_a_product_by_its_inverse():
	a = Matrix(
		3, -9, 7, 3,
		3, -8, 2, -9,
		-4, 4, 4, 1,
		-6, 5, -1, 1,
	)

	b = Matrix(
		8, 2, 2, 2,
		3, -1, 7, 0,
		7, 0, 5, 4,
		6, -2, 0, 5,
	)

	c = a * b

	assert a == c * b.inverse()