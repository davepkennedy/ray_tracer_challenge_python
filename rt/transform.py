from .matrix import Matrix, Identity

import math

def translation(x,y,z):
    m = Identity(4)
    m[(0, 3)] = x
    m[(1, 3)] = y
    m[(2, 3)] = z
    return m

def scaling(x,y,z):
    m = Identity(4)
    m[(0, 0)] = x
    m[(1, 1)] = y
    m[(2, 2)] = z
    return m

def rotation_x(r):
    return Matrix(
			1,0,0,0,
			0,math.cos(r), -math.sin(r),0,
			0,math.sin(r), math.cos(r),0,
			0,0,0,1
		)

def rotation_y(r):
    return Matrix (
        math.cos(r), 0, math.sin(r), 0,
        0, 1, 0, 0,
        -math.sin(r), 0, math.cos(r), 0,
        0,0,0,1
        )

def rotation_z(r):
    return Matrix (
        math.cos(r), -math.sin(r), 0, 0,
        math.sin(r), math.cos(r), 0, 0,
        0, 0, 1, 0,
        0,0,0,1
        )

def shearing(
    xy, xz, 
    yx, yz,
    zx, zy):
    return Matrix (
        1, xy, xz, 0,
        yx, 1, yz, 0,
        zx, zy, 1, 0,
        0, 0, 0, 1
        )    

def view (source, to, up):
    forward = (to - source).normalize()
    left = forward.cross(up.normalize())
    true_up = left.cross(forward)
    
    orientation = Matrix(
        left.x, left.y, left.z, 0,
        true_up.x, true_up.y, true_up.z, 0,
        -forward.x, -forward.y, -forward.z, 0,
        0, 0, 0, 1)
    return orientation * translation(-source.x, -source.y, -source.z)