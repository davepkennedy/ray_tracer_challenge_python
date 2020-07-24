from .tuple import Point
from .group import Group
from .triangle import Triangle
from .smooth_triangle import SmoothTriangle

def parse_file(path):
    with open(path) as f:
        return ObjFileParser(f)

def _to_float(s):
    try:
        return float(s)
    except ValueError:
        return 0

def _to_int(s):
    try:
        return int(s)-1
    except ValueError:
        return 0

class ObjFileParser:
    __slots__ = [
        'vertices','normals','ignored','default_group','groups', 'group'
    ]

    def __getitem__(self, key):
        return self.groups[key]

    def __init__ (self, reader):
        self.ignored = 0
        self.vertices = []
        self.normals = []
        self.default_group = Group()
        self.groups = {}
        self.group = self.default_group

        switcher = {
            'v': self.add_point_from_string,
            'f': self.add_faces_from_string,
            'g': self.add_group_from_string,
            'vn': self.add_vector_from_string
        }

        for line in reader:
            line = line.strip()
            parts = line.split()
            if len(line):
                if line[0] in switcher:
                    switcher[parts[0]](line)
                # switch (parts[0])
                # case "v":
                # vertices.Add(PointFromString(line.Substring(1).Trim()))
                #            break
                #        case "vn":
                #            normals.Add(PointFromString(line.Substring(2).Trim()).ToVector())
                #            break
                #        case "f":
                #            FacesFromString(line.Substring(1).Trim()).ForEach(s => group.Add(s))
                #            break
                #        case "g":
                #            String groupName = line.Substring(1).Trim()
                #            group = Group()
                #            groups[groupName] = group
                #            break
                #        default:
                else:
                    self.ignored += 1

    def add_group_from_string(self, line):
        group_name = line[1:].strip()
        self.group = Group()
        self.groups[group_name] = self.group

    def tuple_from_string(self, v):
        return Point(*map(_to_float, v.split()))

    def add_point_from_string(self, v):
        self.vertices.append(self.tuple_from_string(v[1:]).to_point())

    def add_vector_from_string(self, v):
        self.normals.append(self.tuple_from_string(v[2:]).to_vector())

    def parse_face_entry(self, v):
        return list(map(_to_int,v.split('/')))

    def parse_face (self, v):
        return list(map(self.parse_face_entry, v.split()))

    def faces_from_string(self, v):
        parts = self.parse_face(v[1:].strip())
        faces = []
        for i in range(1, len(parts)-1):
            if len(parts[0]) > 1 and parts[0][2] >= 0 and \
                    len(parts[i]) and parts[i][2] >= 0 and \
                    len(parts[i + 1]) and parts[i + 1][2] >= 0:
                faces.append(SmoothTriangle(
                        self.vertices[parts[0][0]],
                        self.vertices[parts[i][0]],
                        self.vertices[parts[i + 1][0]],
                        self.normals[parts[0][2]],
                        self.normals[parts[i][2]],
                        self.normals[parts[i + 1][2]]))
            else:
                faces.append(Triangle(
                        self.vertices[parts[0][0]],
                        self.vertices[parts[i][0]],
                        self.vertices[parts[i + 1][0]]))
        return faces

    def add_faces_from_string(self, v):
        for face in self.faces_from_string(v):
            self.group.add(face)
            
    def to_group(self):
        g = Group()
        g.add(self.default_group)
        for value in self.groups.values():
            g.add(value)
        return g