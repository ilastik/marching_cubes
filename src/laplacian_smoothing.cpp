#include "laplacian_smoothing.h"
#include <vector>
// #include <set>
// #include <unordered_set>
#include <iostream>


#include <boost/container/flat_set.hpp>

typedef std::vector<boost::container::flat_set<size_t>> Adjacency;
//typedef std::vector<std::set<size_t> > Adjacency;
//typedef std::vector<std::unordered_set<size_t> > Adjacency;
/**
 * maps each vertex to all its neighbours
 */


template<typename T>
void swap(T& a, T&b)
{
	T tmp = a;
	a = b;
	b = tmp;
}


/**
 * generates the adjacency list for the vertices in the mesh
 * returns the adjacency list
 */
Adjacency adjacencyList(Mesh& mesh)
{
	Adjacency adjacency(mesh.vertexCount);

	size_t faceCount = mesh.faceCount;
	size_t* faces = mesh.faces;


	//#pragma omp parallel for
	for (size_t i = 0; i < faceCount * 3; i += 3)
	{
		//#pragma omp critical
		{
			size_t a, b, c;
			a = mesh.faces[i];
			b = faces[i + 1];
			c = faces[i + 2];
			//std::cout<<"i"<<i<<" ("<<a<<","<<b<<","<<c<<")\n";

			adjacency[a].insert(b);
			adjacency[a].insert(c);
			adjacency[b].insert(a);
			adjacency[b].insert(c);
			adjacency[c].insert(a);
			adjacency[c].insert(b);
		}
	}
	//std::cout<<"adjacency done\n";
	return adjacency;
}


void smooth(Mesh& mesh, unsigned int rounds)
{
	auto adjacency = adjacencyList(mesh);

	Point* vertices = mesh.vertices;
	Point* normals = mesh.normals;
	size_t vertexCount = mesh.vertexCount;

	Point* new_verts = new Point[vertexCount];
	Point* new_norms = new Point[vertexCount];

	for (unsigned int i = 0; i < rounds; ++i)
	{
		#pragma omp parallel for
		for (size_t vert = 0; vert < vertexCount; ++vert)
		{
			for (unsigned int off = 0; off < 3; ++off)
			{
				float new_vert = vertices[vert][off];
				float new_norm = normals[vert][off];
				auto& neis = adjacency[vert];
				for (auto nei : neis)
				{
					new_vert += vertices[nei][off];
					new_norm += normals[nei][off];
				}
				new_verts[vert][off] = new_vert / (neis.size() + 1);
				new_norms[vert][off] = new_norm / (neis.size() + 1);
			}

		}
		swap(normals, new_norms);
		swap(vertices, new_verts);
	}
	delete[] new_norms;
	delete[] new_verts;
	mesh.normals = normals;
	mesh.vertices = vertices;
}