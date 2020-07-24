from ..rt import Canvas, Color

from io import StringIO

def test_creating_a_canvas():
	c = Canvas(10, 20)
	assert 10 == c.width
	assert 20 == c.height

	for pixel in c.pixels:
		assert Color(0.0, 0.0, 0.0) == pixel
	

def test_write_pixel_to_canvas():
	red = Color(1.0, 0.0, 0.0)
	canvas = Canvas(10, 20)

	canvas[(2, 3)] = red
	assert red == canvas[(2, 3)]

def test_constructing_ppm_header():
    canvas = Canvas(5, 3)
    buf = StringIO()
    canvas.to_ppm(buf)
    
    buf.seek(0)
    lines = [line.strip() for line in buf.readlines()]
    
    assert "P3" == lines[0]
    assert "5 3" == lines[1]
    assert "255" == lines[2]

def test_constructing_the_ppm_pixel_data():
    canvas = Canvas(5, 3)
    c1 = Color(1.5, 0.0, 0.0)
    c2 = Color(0.0, 0.5, 0.0)
    c3 = Color(-0.5, 0.0, 1.0)

    canvas[(0, 0)] = c1
    canvas[(2, 1)] = c2
    canvas[(4, 2)] = c3

    buf = StringIO()
    canvas.to_ppm(buf)
    buf.seek(0)
    lines = [line.strip() for line in buf.readlines()]

    assert "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0" == lines[3]
    assert "0 0 0 0 0 0 0 128 0 0 0 0 0 0 0" == lines[4]
    assert "0 0 0 0 0 0 0 0 0 0 0 0 0 0 255" == lines[5]

def test_ppm_ends_with_new_line():
    canvas = Canvas(5, 3)
    buf = StringIO()
    canvas.to_ppm(buf)
    
    buf.seek(0)
    lines = buf.readlines()
    assert "\n" == lines[-1][-1]
