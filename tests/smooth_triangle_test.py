from ..rt import Point, Vector
from ..rt import SmoothTriangle
from ..rt import Intersection, Intersections
from ..rt import Ray

from ..rt.linmath import approx_eq

class TestSmoothTriangle:
    __slots__ = ['p1','p2','p3','n1','n2','n3','tri']
    
    def setup_method(self, method):
        self.p1 = Point(0, 1, 0)
        self.p2 = Point(-1, 0, 0)
        self.p3 = Point(1, 0, 0)

        self.n1 = Vector(0, 1, 0)
        self.n2 = Vector(-1, 0, 0)
        self.n3 = Vector(1, 0, 0)

        self.tri = SmoothTriangle(
            self.p1, self.p2, self.p3, 
            self.n1, self.n2, self.n3)
        
    def test_constructing_a_smooth_triangle(self):
        assert self.p1 == self.tri.p1
        assert self.p2 == self.tri.p2
        assert self.p3 == self.tri.p3

        assert self.n1 == self.tri.n1
        assert self.n2 == self.tri.n2
        assert self.n3 == self.tri.n3
        
    def test_an_intersection_with_a_smooth_triangle(self):
        r = Ray(Point(-0.2, 0.3, -2), Vector(0, 0, 1))
        xs = self.tri.intersects(r)

        assert approx_eq(0.45, xs[0].u)
        assert approx_eq(0.25, xs[0].v)
        
    def test_a_smooth_triangle_uses_u_v_to_interpolate_the_normal(self):
        i = Intersection(1, self.tri, 0.45, 0.25)
        n = self.tri.normal_at(Point(0, 0, 0), i)
        assert Vector(-0.5547, 0.83205, 0) == n
        
    def test_preparing_the_normal_on_a_smooth_triangle(self):
        i = Intersection(1, self.tri, 0.45, 0.25)
        r = Ray(Point(-0.2, 0.3, -2), Vector(0, 0, 1))
        xs = Intersections(i)
        comps = i.prepare_computations(r, xs)
        assert Vector(-0.5547, 0.83205, 0) == comps.normalv 