from .triangle import Triangle

class SmoothTriangle(Triangle):
    __slots__ = ['n1', 'n2', 'n3']
    # public Point P1 { get; internal set; }
    # public Point P2 { get; internal set; }
    # public Point P3 { get; internal set; }

    def __init__(self, p1,p2,p3,n1,n2,n3):
        super().__init__(p1,p2,p3)
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        
    def local_normal_at(self, pt, i):
        return self.n2 * i.u + \
                self.n3 * i.v + \
                self.n1 * (1 - i.u - i.v)