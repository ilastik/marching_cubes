import numpy as np
import pandas as pd

def laplacian_smooth(vertices, faces, rounds=1):
    """
    Pure-python reference implementation of laplacian smoothing.

    This is simplest mesh smoothing technique, known as Laplacian Smoothing.
    Relocates each vertex by averaging its position with those of its adjacent neighbors.
    Repeat for N iterations.

    One disadvantage of this technique is that it results in overall shrinkage
    of the mesh, especially for many iterations. (But nearly all smoothing techniques
    cause at least some shrinkage.)

    (Obviously, any normals you have for this mesh will be out-of-date after smoothing.)

    Args:
        vertices:
            Vertex coordinates shape=(N,3)
        faces
            Face definitions.  shape=(N,3)
            Each row lists 3 vertices (indexes into the vertices array)
        rounds:
            How many passes to take over the data.
            More iterations results in a smoother mesh, but more shrinkage (and more CPU time).

    Returns:
        new vertices

    Note:
        Smoothing can cause degenerate faces, particularly in some
        small special cases like this:

          1        1
         / \       |
        2---3 ==>  X (where X is occupied by both 2 and 3)
         \ /       |
          4        4

        (Such meshes are not usually produced by marching cubes, though.)
    """
    vertices = np.array(vertices, dtype=np.float32)
    faces = np.asarray(faces)

    # Compute the list of all unique vertex adjacencies
    all_edges = np.concatenate( [faces[:,(0,1)],
                                 faces[:,(1,2)],
                                 faces[:,(2,0)]] )
    all_edges.sort(axis=1)
    edges_df = pd.DataFrame( all_edges, columns=['v1_id', 'v2_id'] )
    edges_df.drop_duplicates(inplace=True)
    del all_edges

    # (This sort isn't technically necessary, but it might give
    # better cache locality for the vertex lookups below.)
    edges_df.sort_values(['v1_id', 'v2_id'], inplace=True)

    # How many neighbors for each vertex == how many times it is mentioned in the edge list
    neighbor_counts = np.bincount(edges_df.values.reshape(-1), minlength=len(vertices))

    new_vertices = np.empty_like(vertices)
    for _ in range(rounds):
        new_vertices[:] = vertices

        # For the complete edge index list, accumulate (sum) the vertexes on
        # the right side of the list into the left side's address and vice-versa.
        #
        ## We want something like this:
        # v1_indexes, v2_indexes = df['v1_id'], df['v2_id']
        # new_vertices[v1_indexes] += vertices[v2_indexes]
        # new_vertices[v2_indexes] += vertices[v1_indexes]
        #
        # ...but that doesn't work because v1_indexes will contain repeats,
        #    and "fancy indexing" behavior is undefined in that case.
        #
        # Instead, it turns out that np.ufunc.at() works (it's an "unbuffered" operation)
        np.add.at(new_vertices, edges_df['v1_id'], vertices[edges_df['v2_id'], :])
        np.add.at(new_vertices, edges_df['v2_id'], vertices[edges_df['v1_id'], :])

        # (plus one here because each point itself is also included in the sum)
        new_vertices[:] /= (neighbor_counts[:,None] + 1)

        # Swap (save RAM allocation overhead by reusing the new_vertices array between iterations)
        vertices, new_vertices = new_vertices, vertices

    return vertices
