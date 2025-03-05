import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import math
import matplotlib.colors as mcolors

mesh_path = "/path/to/mesh.obj"


def plot_mesh(vertices, triangles, colors):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Compute centroids of all triangles
    centroids = [vertices[triangle].mean(axis=0) for triangle in triangles]

    # Compute angles between the x-axis and the line connecting the origin with each centroid
    angles = [np.arctan2(centroid[1], centroid[0]) for centroid in centroids]

    # Sort indices of triangles based on their angles (this gives us a clockwise order)
    sorted_indices = np.argsort(angles)

    for i in sorted_indices:
        triangle = triangles[i]
        triangle_vertices = vertices[triangle]
        x = triangle_vertices[:, 0] + np.random.uniform(-1e-5, 1e-5, size=triangle_vertices.shape[0])  # Increase the noise
        y = triangle_vertices[:, 1] + np.random.uniform(-1e-5, 1e-5, size=triangle_vertices.shape[0])  # Increase the noise
        z = triangle_vertices[:, 2] + np.random.uniform(-1e-5, 1e-5, size=triangle_vertices.shape[0])  # Increase the noise
        ax.plot_trisurf(x, y, z, color=mcolors.to_hex(colors[i+1]/255))  # Convert RGB to hex color
        centroid = triangle_vertices.mean(axis=0)
        ax.text(*centroid, str(i+1), zdir=(0,0,1))  # Move the label slightly along the z-axis
    plt.show()


# Define the RGB colors for each triangle
colors = {
    1: np.array([143, 135, 109]),
    2: np.array([139, 131, 105]),
    3: np.array([77, 72, 63]),
    4: np.array([139, 131, 105]),
    5: np.array([106, 100,  83]),
    6: np.array([143, 135, 109]),
    7: np.array([77, 72, 63]),
    8: np.array([106, 100,  83])
}

# Load mesh
LoD2 = o3d.io.read_triangle_mesh(mesh_path, 
                enable_post_processing=False, print_progress=True)
mesh = o3d.t.geometry.TriangleMesh.from_legacy(LoD2)
   
# Subdivide the mesh
for _ in range(1):  # Number of subdivision iterations
    LoD2 = LoD2.subdivide_midpoint() 

# Convert to numpy array
vertices = np.asarray(LoD2.vertices)
triangles = np.asarray(LoD2.triangles)

# Plot mesh
plot_mesh(vertices, triangles, colors)

#coloring
def assign_colors_to_mesh(mesh, colors):
    # Initialize an array to store the colors of the vertices
    vertex_colors = np.zeros((len(mesh.vertices), 3))

    # Assign colors to the vertices of each triangle
    for i, triangle in enumerate(mesh.triangles):
        for vertex_index in triangle:
            vertex_colors[vertex_index] = colors[i+1] / 255  # Normalize the color values to [0, 1]

    # Assign the vertex colors to the mesh
    mesh.vertex_colors = o3d.utility.Vector3dVector(vertex_colors)

# Assign colors to the mesh
assign_colors_to_mesh(LoD2, colors)

# Save the colored mesh as a new .obj file
o3d.io.write_triangle_mesh("/path/to/mesh.obj", LoD2)

print("The colored mesh was successfully saved as colored_mesh.obj")