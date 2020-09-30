Marching cubes implementation for the volumina 3D viewer
========================================================

[![Build status](https://ci.appveyor.com/api/projects/status/xqo5wl6d1bgxygli/branch/master?svg=true)](https://ci.appveyor.com/project/k-dominik/marching-cubes/branch/master)
[![Build Status](https://travis-ci.org/ilastik/marching_cubes.svg?branch=master)](https://travis-ci.org/ilastik/marching_cubes)

Creates a 3D iso surface from a 3D volume.


Release Notes:
--------------
__0.3__:
 * fixed fortran order expectation (#26)
   *Note:* previously data was expected in fortran order.
   A workaround was to supply `volume.T` with C-order data to `march`.
   This should not be done anymore.
   `march` works with C- and F-order data now.

__0.2__:
 * fixed number of smoothing rounds off by one error (#23)
   *Note:* in order to get consistent results with older versions, you'll have to decrement the number of smoothing rounds by `1`.
   So instead of e.g. `march(volume, 4)`, go for `march(volume, 3)`.


Why not these? (time of writing July 2016)
--------------

- `skimage`
    1. too slow (factor 10 - 20)
    2. incorrect normals (shading looks ugly)
- `vtk`
    1. huge dependency
    2. does not support python3.x

    _update: vtk started supporting Python 3.2-3.5 with version 7, Python 3.5-3.8 with version 9_


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
smooth_vertices, smooth_normals, faces = march(volume, 3)  # 3 smoothing rounds

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

__3 smoothing rounds__

![3 smoothing rounds](https://raw.githubusercontent.com/ilastik/marching_cubes/master/test/image_smooth.png)


This library is work in progress
--------------------------------

__Todo:__

* repair workaround for volumes with different shapes
