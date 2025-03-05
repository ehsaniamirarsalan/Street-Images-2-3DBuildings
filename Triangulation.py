import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import math
import matplotlib.colors as mcolors

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

def assign_colors_to_mesh(mesh, colors):
    # Initialize an array to store the colors of the vertices
    vertex_colors = np.zeros((len(mesh.vertices), 3))

    # Assign colors to the vertices of each triangle
    for i, triangle in enumerate(mesh.triangles):
        for vertex_index in triangle:
            vertex_colors[vertex_index] = colors[i+1] / 255  # Normalize the color values to [0, 1]

    # Assign the vertex colors to the mesh
    mesh.vertex_colors = o3d.utility.Vector3dVector(vertex_colors)

def assign_colors_to_points(raycast_results, rays, colors):
    # Initialize an array to store the colors of the points
    point_colors = np.zeros((len(rays), 3))

    # Assign colors to the points based on the geometry_ids of the hit triangles
    for i, geometry_id in enumerate(raycast_results['geometry_ids']):
        if geometry_id >= 0:  # Check if the ray hit a triangle
            point_colors[i] = colors[geometry_id + 1] / 255  # Normalize the color values to [0, 1]

    # Create a point cloud from the hit points
    hit = raycast_results['t_hit'].isfinite()
    points = rays[hit][:,:3] + rays[hit][:,3:]*raycast_results['t_hit'][hit].reshape((-1,1))
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(point_colors[hit])

    return pcd
