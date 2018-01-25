#include <pybind11/pybind11.h>



#include "xtensor/xtensor.hpp"
#include "xtensor/xbuilder.hpp"
#include "xtensor/xmath.hpp"              // xtensor import for the C++ universal functions
#define FORCE_IMPORT_ARRAY
#include "xtensor-python/pyarray.hpp"     // Numpy bindings
#include "xtensor-python/pytensor.hpp"     // Numpy bindings


#include "marching_cubes.h"
#include "laplacian_smoothing.h"

#include <tuple>
#include <set>

namespace py = pybind11;


const int ISO_LEVEL = 1;


namespace marching_cubes
{

    auto
    marching_cubes_impl(
        xt::pytensor<int, 3> volume,
        int smooth_rounds
    )
    {
        const auto shape = volume.shape();
        const size_t x_shape = shape[0];
        const size_t y_shape = shape[1];
        const size_t z_shape = shape[2];

        int* volume_ptr = &volume(0);

        Mesh mesh;

        {
            py::gil_scoped_release release;
            mesh = march(volume_ptr, x_shape, y_shape, z_shape, ISO_LEVEL);
        }

        if (smooth_rounds > 0)
        {
            py::gil_scoped_release release;
            smooth(mesh, smooth_rounds);
        }


        // vertices



        const auto zerosVert = xt::zeros<float >({ int(mesh.vertexCount), int(3) });
        xt::pytensor<float,  2> vertices = xt::zeros<float >({ int(mesh.vertexCount), int(3) });
        xt::pytensor<float,  2> normals  = xt::zeros<float >({ int(mesh.vertexCount), int(3) });
        xt::pytensor<size_t, 2> faces    = xt::zeros<size_t>({ int(mesh.faceCount),   int(3) });

        // // todo, make this more efficient
        std::copy(&(mesh.vertices[0][0]), (&(mesh.vertices[0][0]))+mesh.vertexCount,&vertices(0));
        std::copy(&mesh.normals[0][0],  (&mesh.normals[0][0])+mesh.vertexCount, &normals(0));
        std::copy(&mesh.faces[0],  (&mesh.faces[0])+mesh.faceCount,       &faces(0));



        // // std::string vert_format = py::format_descriptor<float>::value;
        // // auto vert_info = py::buffer_info(mesh.vertices, sizeof(float), vert_format, 2, { mesh.vertexCount, 3 }, { sizeof(float) * 3, sizeof(float) });
        // // auto vert_array = py::array(vert_info);

        // // std::string norm_format = py::format_descriptor<float>::value;
        // // auto norm_info = py::buffer_info(mesh.normals, sizeof(float), norm_format, 2, { mesh.vertexCount, 3 }, { sizeof(float) * 3, sizeof(float) });
        // // auto norm_array = py::array(norm_info);

        // // std::string face_format = py::format_descriptor<unsigned int>::value;
        // // auto face_info = py::buffer_info(mesh.faces, sizeof(size_t), face_format, 2, { mesh.faceCount, 3 }, { sizeof(size_t) * 3, sizeof(size_t) });
        // // auto face_array = py::array(face_info);

        // return std::make_tuple(vertices, normals, faces);
    }

}

PYBIND11_MODULE(marching_cubes,m) {
	//py::module m("marching_cubes");

	m.def("march", &marching_cubes::marching_cubes_impl, "Marching cubes implementation");

	//return m.ptr();
}
