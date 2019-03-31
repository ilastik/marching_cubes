import marching_cubes
import numpy
import pytest
import os


@pytest.fixture
def volume():
    vol_path = os.path.join(os.path.split(__file__)[0], "data/input/sample.npy")
    return numpy.load(vol_path)


@pytest.fixture
def mesh_loader():
    """Load mesh data from npz file"""

    def _loader(mesh_file_name):
        data = numpy.load(mesh_file_name)
        vertices = data["vertices"]
        normals = data["normals"]
        faces = data["faces"]
        return vertices, normals, faces

    return _loader


@pytest.mark.parametrize(
    "smoothing, reference_mesh_file",
    [
        (0, os.path.join(os.path.split(__file__)[0], "data/reference/sample_mesh.npz")),
        (4, os.path.join(os.path.split(__file__)[0], "data/reference/sample_mesh_smoothed4.npz")),
    ],
)
def test_regression(volume, mesh_loader, smoothing, reference_mesh_file):
    vertices, normals, faces = marching_cubes.march(volume, smoothing)

    ref_vertices, ref_normals, ref_faces = mesh_loader(reference_mesh_file)

    numpy.testing.assert_array_almost_equal(vertices, ref_vertices)
    numpy.testing.assert_array_almost_equal(normals, ref_normals)
    numpy.testing.assert_array_almost_equal(faces, ref_faces)
