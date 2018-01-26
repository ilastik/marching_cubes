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

    auto marching_cubes_glue(
        xt::pytensor<int, 3> volume,
        int smooth_rounds
    )
    {
        
        Mesh mesh;

        const auto shape = volume.shape();
        {
            py::gil_scoped_release release;
            mesh = march( &volume(0), shape[0], shape[1], shape[2], ISO_LEVEL);
        }

        if (smooth_rounds > 0)
        {
            py::gil_scoped_release release;
            smooth(mesh, smooth_rounds);
        }


        const auto zerosVert = xt::zeros<float >({ int(mesh.vertexCount), int(3) });
        xt::pytensor<float,  2> vertices = xt::zeros<float >({ int(mesh.vertexCount), int(3) });
        xt::pytensor<float,  2> normals  = xt::zeros<float >({ int(mesh.vertexCount), int(3) });
        xt::pytensor<size_t, 2> faces    = xt::zeros<size_t>({ int(mesh.faceCount),   int(3) });

        std::copy(&(mesh.vertices[0][0]), (&(mesh.vertices[0][0]))+mesh.vertexCount*3,&vertices(0));
        std::copy(&(mesh.normals[0][0]),  (&(mesh.normals[0][0]))+mesh.vertexCount*3, &normals(0));
        std::copy(&mesh.faces[0],  (&mesh.faces[0])+mesh.faceCount,       &faces(0));


        return std::make_tuple(vertices, normals, faces);
    }

}

PYBIND11_MODULE(marching_cubes,m) {
	//py::module m("marching_cubes");

	m.def("march", &marching_cubes::marching_cubes_glue, "Marching cubes implementation");

	//return m.ptr();
}
