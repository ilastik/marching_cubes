from marching_cubes import march
from numpy import load
import os
import time

from pyqtgraph.opengl import GLViewWidget, MeshData
from pyqtgraph.opengl.items.GLMeshItem import GLMeshItem

from PyQt5.QtGui import QApplication


volume = load(os.path.join(os.path.split(__file__)[0], 'data/input/sample.npy'))


t0 = time.time()
vertices, normals, faces = march(volume, 0)  # zero smoothing rounds
smooth_vertices, smooth_normals, faces = march(volume, 4)  # 4 smoothing rounds
t1 = time.time()
print("took", t1 - t0, "sec")

app = QApplication([])
view = GLViewWidget()

mesh = MeshData(vertices / 100.0, faces)  # scale down - otherwise camera is misplaced
# or mesh = MeshData(smooth_vertices / 100, faces)
mesh._vertexNormals = normals
# or mesh._vertexNormals = smooth_normals

item = GLMeshItem(meshdata=mesh, color=[1, 0, 0, 1], shader="normalColor")

view.addItem(item)
view.show()
app.exec_()
