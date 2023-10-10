import marching_cubes
import numpy
import pytest


@pytest.fixture
def data():
    """Test volume with non-zero voxels parallel to axes"""
    data = numpy.zeros((17, 19, 23)).astype("uint32")
    data[1:7, 1:2, 1:2] = 1  # z-axis
    data[1:2, 1:9, 1:2] = 1  # y-axis
    data[1:2, 1:2, 1:11] = 1  # x-axis
    return data


def test_marching_orientation(data):
    v, _, _ = marching_cubes.march(data, 0)
    max_v = v.max(axis=0)
    numpy.testing.assert_array_almost_equal(max_v, [10.5, 8.5, 6.5])
