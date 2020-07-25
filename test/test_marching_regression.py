import marching_cubes
import numpy as np
import pytest
import os

from laplacian_smooth import laplacian_smooth


@pytest.fixture
def volume():
    vol_path = os.path.join(os.path.split(__file__)[0], "data/input/sample.npy")
    data_c_order = np.load(vol_path)
    # a little history lesson:
    # in the past, march would just "expect" the data to be in F-order
    # test data is in C-order, reference-data was generated with the data as is.
    # Effectively the data was seen transposed.
    # When the F-ordering issue was fixed, this data was suddenly "correctly"
    # picked up as C-order -> result was slightly different. In order to
    # emulate the old test, the data has to be transposed.
    return data_c_order.T


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


def test_c_and_f_order_agnostic(volume):
    # take a assymetric volume
    shape_z, shape_y, shape_x = volume.shape
    vol_c = np.ascontiguousarray(volume[0:shape_z // 2, 0:shape_y // 3, 0:shape_x // 5])
    assert len(np.unique(vol_c.shape)) == len(vol_c.shape)
    assert vol_c.flags['C_CONTIGUOUS']
    vol_f = np.copy(vol_c, order="f")
    assert vol_f.flags['F_CONTIGUOUS']

    mesh_data_c = marching_cubes.march(vol_c, 0)
    mesh_data_h = marching_cubes.march(vol_f, 0)

    for a, b in zip(mesh_data_c, mesh_data_h):
        assert (a == b).all()


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
