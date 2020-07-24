from ..rt import ObjFileParser
from ..rt import Point, Vector

from io import StringIO

def test_ignoring_unrecognized_lines():
    input = """
There was a young lady named Bright
Who travelled much faster than light
She set out one day
In a relative way
And returned home the previous night
            """
    reader = StringIO(input)
    parser = ObjFileParser(reader)
    
    assert 5 == parser.ignored
        
def test_vertex_data():
    input = """
v -1 1 0
v -1.000 0.5000 0.000
v 1 0 0
v 1 1 0
            """
    reader = StringIO(input)
    parser = ObjFileParser(reader)
    assert Point(-1, 1, 0) == parser.vertices[0]
    assert Point(-1, 0.5, 0) == parser.vertices[1]
    assert Point(1, 0, 0) == parser.vertices[2]
    assert Point(1, 1, 0) == parser.vertices[3]

def test_parsing_triangle_faces():
    input = """
v -1 1 0
v -1 0 0
v 1 0 0
v 1 1 0

f 1 2 3
f 1 3 4
            """
    reader = StringIO(input)
    parser = ObjFileParser(reader)
    
    g = parser.default_group
    t1 = g[0]
    t2 = g[1]

    assert t1.p1 == parser.vertices[0]
    assert t1.p2 == parser.vertices[1]
    assert t1.p3 == parser.vertices[2]
    assert t2.p1 == parser.vertices[0]
    assert t2.p2 == parser.vertices[2]
    assert t2.p3 == parser.vertices[3]
        
def test_triangulating_polygons():
    input = """
v -1 1 0
v -1 0 0
v 1 0 0
v 1 1 0
v 0 2 0

f 1 2 3 4 5
            """
    reader = StringIO(input)
    parser = ObjFileParser(reader)
    
    g = parser.default_group
    t1 = g[0]
    t2 = g[1]
    t3 = g[2]

    assert t1.p1 == parser.vertices[0]
    assert t1.p2 == parser.vertices[1]
    assert t1.p3 == parser.vertices[2]
    assert t2.p1 == parser.vertices[0]
    assert t2.p2 == parser.vertices[2]
    assert t2.p3 == parser.vertices[3]
    assert t3.p1 == parser.vertices[0]
    assert t3.p2 == parser.vertices[3]
    assert t3.p3 == parser.vertices[4]
        
def test_triangles_in_groups():
    input = """
v -1 1 0
v -1 0 0
v 1 0 0
v 1 1 0

g FirstGroup
f 1 2 3

g SecondGroup
f 1 3 4
"""
    reader = StringIO(input)
    parser = ObjFileParser(reader)
    
    g1 = parser["FirstGroup"]
    g2 = parser["SecondGroup"]
    
    t1 = g1[0]
    t2 = g2[0]
    
    assert t1.p1 == parser.vertices[0]
    assert t1.p2 == parser.vertices[1]
    assert t1.p3 == parser.vertices[2]
    assert t2.p1 == parser.vertices[0]
    assert t2.p2 == parser.vertices[2]
    assert t2.p3 == parser.vertices[3]
    
def test_converting_an_obj_file_to_a_group():
    input = """
v -1 1 0
v -1 0 0
v 1 0 0
v 1 1 0

g FirstGroup
f 1 2 3

g SecondGroup
f 1 3 4
"""
    reader = StringIO(input)
    parser = ObjFileParser(reader)
    
    g1 = parser["FirstGroup"]
    g2 = parser["SecondGroup"]
    
    g = parser.to_group()
    assert g1 in g
    assert g2 in g

def test_vertex_normal_records():
    input = """
vn 0 0 1
vn 0.707 0 -0.707
vn 1 2 3"
"""
    reader = StringIO(input)
    parser = ObjFileParser(reader)
    
    assert Vector(0, 0, 1) == parser.normals[0]
    assert Vector(0.707, 0, -0.707) == parser.normals[1]
    assert Vector(1, 2, 3) == parser.normals[2]
        
def test_faces_with_normals():
    input = """
v 0 1 0
v -1 0 0
v 1 0 0

vn -1 0 0
vn 1 0 0
vn 0 1 0

f 1//3 2//1 3//2
f 1/0/3 2/102/1 3/14/2"""

    reader = StringIO(input)
    parser = ObjFileParser(reader)
    
    g = parser.default_group
    t1 = g[0]
    t2 = g[1]

    assert parser.vertices[0] == t1.p1
    assert parser.vertices[1] == t1.p2
    assert parser.vertices[2] == t1.p3

    assert parser.normals[2] == t1.n1
    assert parser.normals[0] == t1.n2
    assert parser.normals[1] == t1.n3
    
    assert t1 == t2