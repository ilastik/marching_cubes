import marching_cubes
import numpy as np
import pytest
import os

from laplacian_smooth import laplacian_smooth

@pytest.fixture
def volume():
    vol_path = os.path.join(os.path.split(__file__)[0], "data/input/sample.npy")
    return np.load(vol_path)


@pytest.fixture
def mesh_loader():
    """Load mesh data from npz file"""

    def _loader(mesh_file_name):
        data = np.load(mesh_file_name)
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

    np.testing.assert_array_almost_equal(vertices, ref_vertices)
    np.testing.assert_array_almost_equal(normals, ref_normals)
    assert (faces == ref_faces).all()


def test_smoothing(volume):
    ROUNDS = 3
    vertices, normals, faces = marching_cubes.march(volume, 0)
    smoothed_vertices, smoothed_normals, smoothed_faces = marching_cubes.march(volume, ROUNDS)

    # Compare with our reference implementation of laplacian smoothing.
    ref_smoothed_vertices = laplacian_smooth(vertices, faces, ROUNDS)
    np.allclose(smoothed_vertices, ref_smoothed_vertices, rtol=0.001)

    assert (faces == smoothed_faces).all(), \
        "Smoothing should not affect face definitions."

    assert not (normals == smoothed_normals).all(), \
        "Normals should not be the same after smoothing."


def test_reference_smoothing_trivial():
    """
    This is a simple test of our laplacian_smoothing reference function.
    """
    vertices = np.array([[0.0, 0.0, 0.0],
                         [0.0, 0.0, 1.0],
                         [0.0, 0.0, 2.0]])

    # This "face" is actually straight line,
    # which makes it easy to see what's going on
    faces = np.array([[0,1,2]])
    average_vertex = vertices.sum(axis=0) / 3
    vertices = laplacian_smooth(vertices, faces, 1)
    assert (vertices == average_vertex).all()


def test_reference_smoothing_hexagon():
    """
    This is a simple test of our laplacian_smoothing reference function.
    Try 'smoothing' a simple 2D hexagon, which is an easy case to understand.
    """
    # This map is correctly labeled with the vertex indices
    _ = -1
    hexagon = [[[_,_,_,_,_,_,_],
                [_,_,0,_,1,_,_],
                [_,_,_,_,_,_,_],
                [_,2,_,3,_,4,_],
                [_,_,_,_,_,_,_],
                [_,_,5,_,6,_,_],
                [_,_,_,_,_,_,_]]]

    hexagon = 1 + np.array(hexagon)
    original_vertices = np.transpose(hexagon.nonzero())
    faces = [[3,1,4],
             [3,4,6],
             [3,6,5],
             [3,5,2],
             [3,2,0],
             [3,0,1]]

    vertices = laplacian_smooth(original_vertices, faces, 1)

    # Since vertex 3 is exactly centered between the rest,
    # its location never changes.
    assert  (vertices[3] == original_vertices[3]).all()
