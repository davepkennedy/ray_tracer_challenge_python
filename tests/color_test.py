from ..rt import Color

def test_colors_are_red_green_blue_tuples():
	c = Color(0.5, 0.4, 1.7)
	assert 0.5 == c.red
	assert 0.4 == c.green
	assert 1.7 == c.blue

def test_adding_colors():
	a = Color(0.9, 0.6, 0.75)
	b = Color(0.7, 0.1, 0.25)

	assert Color(1.6, 0.7, 1.0) == (a + b)

def test_subtracting_colors():
	a = Color(0.9, 0.6, 0.75)
	b = Color(0.7, 0.1, 0.25)

	assert Color(0.2, 0.5, 0.5) == (a - b)

def test_multiplying_colors_by_a_scalar():
	a = Color(0.2, 0.3, 0.4)
	assert Color (0.4, 0.6, 0.8) == a * 2

def test_multiply_color_by_color():
	a = Color(1.0, 0.2, 0.4)
	b = Color(0.9, 1.0, 0.1)
	assert Color(0.9, 0.2, 0.04) == a * b