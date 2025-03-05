from .Raycasting import project_image, initialize_cam
from .Triangulation import assign_colors_to_points
import numpy as np
import open3d as o3d

# Define the paths to your mesh and image
mesh_path = "/path/to/your/mesh.obj"
image_path = "/path/to/your/Locallytranslated_images/JPEG.jpg"

# Initialize the camera
cam = initialize_cam()

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

# Perform raycasting and get the results
raycast_results, rays = project_image(mesh_path, image_path, cam)

# Assign colors to the points in the point cloud based on the raycasting results
pcd = assign_colors_to_points(raycast_results, rays, colors)

# Visualize the colored point cloud
o3d.visualization.draw_geometries([pcd])
