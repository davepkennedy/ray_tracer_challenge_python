import rt as rt
import math

RADIAN = math.pi / 180.0
def radians(deg):
    return deg * RADIAN

# world = rt.default_world()
camera = rt.Camera (320,240, math.radians(100))
camera.transform = rt.view(
    rt.Point(0, 1.5, -5),
    rt.Point(0, 1, 0), 
    rt.Vector(0, 1, 0))

world = rt.World()
world.light = rt.PointLight(rt.Point(0, 5, -10), rt.Color(1, 1, 1))

floor = rt.Plane()
floor.material = rt.Material()
floor.material.color = rt.Color(1, 0.9, 0.9)
floor.material.specular = 0
floor.material.reflective = 0.5
world.add(floor)

cube = rt.Cube()
cube.transform = rt.rotation_y(radians(30)) * rt.translation(0, 1, 0)
cube.material = rt.Material()
cube.material.color = rt.Color(0.3, 0.1, 0.2)
cube.material.pattern = rt.PerlinPattern(rt.Color(0.1, 1, 0.5), rt.Color(0.45, 0.55, 0.45))
cube.material.pattern.transform = rt.scaling (0.2,0.2,0.2) * rt.rotation_z(math.pi/2)
cube.material.reflective = 1
cube.material.diffuse = 0.7
cube.material.specular = 0.7
world.add(cube)

cone = rt.Cone()
cone.transform = rt.translation(0,0,5)
cone.material = rt.Material()
cone.material.color = rt.Color(0.1, 0.1, 0.3)
cone.material.reflective=1
cone.material.diffuse=0.9
cone.material.specular=0.9
world.add(cone)

canvas = camera.render(world)

with open("raycast.ppm", "w") as f:
    canvas.to_ppm(f)