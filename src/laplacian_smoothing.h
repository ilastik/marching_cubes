#ifndef LAPLACIAN_SMOOTHING_H
#define LAPLACIAN_SMOOTHING_H

#include "marching_cubes.h"

/**
* smoothes the mesh by setting each vertex to the average of its neighbours
* mesh:   the mesh to smooth (modified in-place)
* rounds: the number of repetitions
*/
void smooth(Mesh& mesh, unsigned int rounds);

#endif