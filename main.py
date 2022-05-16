from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(exposure=10)
scene.set_floor(-0.05, (1.0, 1.0, 1.0))

@ti.func
def moon(center, size, color):
    for i, j, k in ti.ndrange((-size, size + 1), (-size, size + 1), (-size, size + 1)):
        point = ivec3(i, j, k)
        if point.dot(point) < size * size:
            scene.set_voxel(vec3(center[0] + i, center[1] + j, center[2] + k), 2,vec3(color))

@ti.kernel
def initialize_voxels():
    color1 = (0.2, 0.2, 0.2);
    center = (1, 39, -39)

    moon((center[0], center[1] + 6, center[2]), 3, color1)

    n = 50
    randomPre = 0
    color = vec3(ti.random(), ti.random(), ti.random())

    for i, j in ti.ndrange(n, n):
        # if ti.random()>0.7:
        #     continue

        if randomPre == 0:
            color = vec3(ti.random(), ti.random(), ti.random())

        if min(i, j) == 0 or max(i, j) == n - 1:
            scene.set_voxel(vec3(i, 0, j), 2, vec3(ti.random(), ti.random(), ti.random()))
        else:
            scene.set_voxel(vec3(i, 0, j), 1, vec3(ti.random(), ti.random(), ti.random()))

            random = ti.random()

            if randomPre > 0 or random < 0.5:
                heightMax = 20
                if ti.random() > 0.96:
                    heightMax = 50

                height = int(ti.random() * heightMax)
                randomPre = 1
                if ti.random() < 0.95:
                    randomPre = 0
                    # colorNext = vec3(ti.random(), ti.random(), ti.random())

                for k in range(1, height):
                    scene.set_voxel(vec3(i, k, j), 1, color)
                for z in range(1, height):
                    if ti.random() > 0.8:
                        scene.set_voxel(vec3(i, z, j), 2, color)

initialize_voxels()

scene.finish()
