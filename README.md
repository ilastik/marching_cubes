Marching cubes implementation for the volumina 3D viewer
========================================================

[![Build status](https://ci.appveyor.com/api/projects/status/xqo5wl6d1bgxygli/branch/master?svg=true)](https://ci.appveyor.com/project/k-dominik/marching-cubes/branch/master)
[![Build Status](https://travis-ci.org/ilastik/marching_cubes.svg?branch=master)](https://travis-ci.org/ilastik/marching_cubes)

Creates a 3D iso surface from a 3D volume.

Why not these?
--------------

- `skimage`
    1. too slow (factor 10 - 20)
    2. incorrect normals (shading looks ugly)
- `vtk`
    1. huge dependency
    2. does not support python3.x


This library is work in progress
--------------------------------

__Todo:__

* repair workaround for volumes with different shapes


Example usage
-------------

__Mesh generation:__

```python
from marching_cubes import march
from numpy import load

volume = load("test/data/input/sample.npy")  # 128x128x128 uint8 volume

# extract the mesh where the values are larger than or equal to 1
# everything else is ignored
vertices, normals, faces = march(volume, 0)  # zero smoothing rounds
smooth_vertices, smooth_normals, faces = march(volume, 4)  # 4 smoothing rounds

# mesh statistics:
# 82464  vertices
# 82464  normals
# 165048 faces(triangles)
# duration:  0.158s
# smoothing: +0.254s
# [CPU: AMD A8-4500M 1.9 GHz]
```

__Displaying:__

```python
from pyqtgraph.opengl import GLViewWidget, MeshData
from pyqtgraph.opengl.items.GLMeshItem import GLMeshItem

from PyQt4.QtGui import QApplication

app = QApplication([])
view = GLViewWidget()

mesh = MeshData(vertices / 100, faces)  # scale down - because camera is at a fixed position 
# or mesh = MeshData(smooth_vertices / 100, faces)
mesh._vertexNormals = normals
# or mesh._vertexNormals = smooth_normals

item = GLMeshItem(meshdata=mesh, color=[1, 0, 0, 1], shader="normalColor")

view.addItem(item)
view.show()
app.exec_()
```

Example images
--------------

__No smoothing__

![no smoothing](https://raw.githubusercontent.com/ilastik/marching_cubes/master/test/image.png)

__4 smoothing rounds__

![4 smoothing rounds](https://raw.githubusercontent.com/ilastik/marching_cubes/master/test/image_smooth.png)