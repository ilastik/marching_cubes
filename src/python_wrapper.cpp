#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "marching_cubes.h"
#include "laplacian_smoothing.h"

#include <tuple>
#include <set>

namespace py = pybind11;


const int ISO_LEVEL = 1;


namespace marching_cubes
{

    std::tuple<py::array, py::array, py::array> 
    marching_cubes_glue(
        py::array_t<int, py::array::f_style | py::array::forcecast > volume,
        int smooth_rounds
    )
    {
        auto buffer = volume.request();

        if (buffer.ndim != 3)
        {
            throw py::value_error("Volume ndim must be 3, not " + buffer.ndim);
        }

        size_t x_shape = buffer.shape[0];
        size_t y_shape = buffer.shape[1];
        size_t z_shape = buffer.shape[2];

        int* volume_ptr = (int*)buffer.ptr;


        Mesh mesh;
        const auto shape = volume.shape();
        {
            py::gil_scoped_release release;
            mesh = march( volume_ptr, x_shape, y_shape, z_shape, ISO_LEVEL);
        }

        if (smooth_rounds > 0)
        {
            py::gil_scoped_release release;
            smooth(mesh, smooth_rounds);
        }   

        const auto vc = int(mesh.vertexCount);
        const auto fc = int(mesh.faceCount);

        if(vc == 0 || fc == 0){
            throw py::value_error("vertex or face count are zero: terminating marching cubes");
        }
    
        std::string vert_format = py::format_descriptor<float>::value;
        auto vert_info = py::buffer_info(mesh.vertices, sizeof(float), vert_format, 2, { vc, 3 }, { sizeof(float) * 3, sizeof(float) });
        auto vert_array = py::array(vert_info);

        std::string norm_format = py::format_descriptor<float>::value;
        auto norm_info = py::buffer_info(mesh.normals, sizeof(float), norm_format, 2, { vc, 3 }, { sizeof(float) * 3, sizeof(float) });
        auto norm_array = py::array(norm_info);

        std::string face_format = py::format_descriptor<unsigned int>::value;
        auto face_info = py::buffer_info(mesh.faces, sizeof(size_t), face_format, 2, { fc, 3 }, { sizeof(size_t) * 3, sizeof(size_t) });
        auto face_array = py::array(face_info);

        return std::make_tuple(vert_array, norm_array, face_array);

    }

}

PYBIND11_MODULE(marching_cubes,m) {
	m.def("march", &marching_cubes::marching_cubes_glue, "Marching cubes implementation");
}
