import marching_cubes
import numpy
import pytest
import os


@pytest.fixture
def volume():
    vol_path = os.path.join(os.path.split(__file__)[0], 'sample.npy')
    return numpy.load(vol_path)


@pytest.fixture
def mesh_loader():
    """Load mesh data from npz file"""
    def _loader(mesh_file_name):
        data = numpy.load(mesh_file_name)
        vertices = data['vertices']
        normals = data['normals']
        faces = data['faces']
        return vertices, normals, faces

    return _loader


@pytest.fixture
def ref_mesh(mesh_loader):
    mesh_file = os.path.join(os.path.split(__file__)[0], 'sample_mesh.npz')
    return mesh_loader(mesh_file)


@pytest.fixture
def ref_mesh_smoothed(mesh_loader):
    mesh_file = os.path.join(os.path.split(__file__)[0], 'sample_mesh_smoothed4.npz')
    return mesh_loader(mesh_file)


def test_regression(volume, ref_mesh):
    vertices, normals, faces = marching_cubes.march(volume, 0)

    ref_vertices, ref_normals, ref_faces = ref_mesh

    numpy.testing.assert_array_almost_equal(vertices, ref_vertices)
    numpy.testing.assert_array_almost_equal(normals, ref_normals)
    numpy.testing.assert_array_almost_equal(faces, ref_faces)


def test_regression_smoothed(volume, ref_mesh_smoothed):
    vertices, normals, faces = marching_cubes.march(volume, 4)
    ref_vertices, ref_normals, ref_faces = ref_mesh_smoothed

    numpy.testing.assert_array_almost_equal(vertices, ref_vertices)
    numpy.testing.assert_array_almost_equal(normals, ref_normals)
    numpy.testing.assert_array_almost_equal(faces, ref_faces)
