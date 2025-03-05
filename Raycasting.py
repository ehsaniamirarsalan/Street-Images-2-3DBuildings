import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import math
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D

def initialize_cam():
    cam = {
        'x': 26.5220015504,
        'y': 24.214197471,
        'width': 4032,
        'height': 3024,
        'altitude': 1.9911950202659,
        'yaw': 1.5149143672449,
        'pitch': -0.30158202409702,
        'roll': 0.27474563334027,
        'cca': 21.173396500177 #74 21.173396500177
    }
    return cam

def project_image(mesh_path, image_path, cam):
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

    # Load image
    image = o3d.io.read_image(image_path)
    min_extents = np.array([3.490436, 6.703003, 0.93])
    max_extents = np.array([27.493946, 67.627477, 19.78])
    Center = (min_extents + max_extents)/1.6 

    # Create RaycastingScene
    scene = o3d.t.geometry.RaycastingScene()
    mesh_id = scene.add_triangles(mesh)

    # Generate rays
    fov = ((np.arctan(((cam['width']/2)/cam['cca']))*2)*180/math.pi)/1.75 #175.81 reviewed 
    rays = o3d.t.geometry.RaycastingScene.create_rays_pinhole(
        fov_deg=fov,
        center= Center, #[cam['x'], cam['y'], cam['cca']],
        eye=[cam['x'], cam['y'], cam['altitude']],# check the yaw pitch raw 
        up=[0, 0, -360], 
        width_px=cam['width'],
        height_px=cam['height'],
    )
    print(f"fov = {fov}")

    # Perform raycasting
    raycast_results = scene.cast_rays(rays)

    return raycast_results, rays
