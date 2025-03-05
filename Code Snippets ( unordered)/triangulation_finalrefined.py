import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def calculate_average_color(image, vertices):
    # Get the coordinates of the vertices
    x, y = zip(*vertices)
    
    # Calculate the bounding box of the triangle
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)
    
    # Extract the pixels within the bounding box
    region = image.crop((x_min, y_min, x_max, y_max))
    pixels = np.array(region)
    
    # Calculate the average RGB value
    average_color = np.mean(pixels, axis=(0, 1))
    return average_color.astype(int)

def label_triangle(ax, vertices, label):
    # Calculate centroid of the triangle
    centroid = np.mean(vertices, axis=0)
    
    # Add label at the centroid
    ax.text(centroid[0], centroid[1], label, ha='center', va='center', fontsize=4, color='white')

def uniform_triangulation(image_path_a, image_path_b, iterations, num_divisions):
    # Load images
    image_a = Image.open(image_path_a) # actual image
    image_b = Image.open(image_path_b) # raycasted image 
    
    image_b = image_b.resize(image_a.size) #resize

    # Extract image sizes
    width_a, height_a = image_a.size
    width_b, height_b = image_b.size
    
    # Calculate grid parameters
    step_x_a = width_a // num_divisions
    step_y_a = height_a // num_divisions
    step_x_b = width_b // num_divisions
    step_y_b = height_b // num_divisions
    
    # Create vertices of the triangles
    vertices_a = []
    vertices_b = []
    for i in range(num_divisions):
        for j in range(num_divisions):
            x0_a, y0_a = i * step_x_a, j * step_y_a
            x1_a, y1_a = (i + 1) * step_x_a, j * step_y_a
            x2_a, y2_a = i * step_x_a, (j + 1) * step_y_a
            x3_a, y3_a = (i + 1) * step_x_a, (j + 1) * step_y_a
            vertices_a.append([(x0_a, y0_a), (x1_a, y1_a), (x3_a, y3_a)])
            vertices_a.append([(x0_a, y0_a), (x2_a, y2_a), (x3_a, y3_a)])
            
            x0_b, y0_b = i * step_x_b, j * step_y_b
            x1_b, y1_b = (i + 1) * step_x_b, j * step_y_b
            x2_b, y2_b = i * step_x_b, (j + 1) * step_y_b
            x3_b, y3_b = (i + 1) * step_x_b, (j + 1) * step_y_b
            vertices_b.append([(x0_b, y0_b), (x1_b, y1_b), (x3_b, y3_b)])
            vertices_b.append([(x0_b, y0_b), (x2_b, y2_b), (x3_b, y3_b)])
    
    # Define the indices of the triangles to copy RGB values from A to B
    indices_to_copy = [
        list(range(0, 33)),     # Column 1
        list(range(60, 93)),    # Column 2
        list(range(120, 153)),    # Column 3
        list(range(180, 213)),    # Column 4
        list(range(242, 273)),    # Column 5
        list(range(304, 333)),  # Column 6
        list(range(366, 393)),  # Column 7
        list(range(428, 453)),     # Column 8
        list(range(490, 513)),     # Column 9
        list(range(552, 573)),     # Column 10
        list(range(614, 633)),    # Column 11
        # list(range(676, 705)),    # Column 12
        # list(range(738, 765)),    # Column 13
        # list(range(800, 825)),    # Column 14
        # list(range(862, 885)),  # Column 15
        # list(range(924, 945)),  # Column 16
        # list(range(986, 1005)),     # Column 17
        # list(range(1048, 1065)),     # Column 18
        # list(range(1110, 1125))      # Column 19
    ]
    
    # Copy RGB values for the specified triangles from image A to B
    for indices in indices_to_copy:
        for i in indices:
            v_a = vertices_a[i]
            v_b = vertices_b[i]
            vertices_b[i] = v_a  # Just copy vertices without modification
    
    # Plot the triangulation for image A
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].imshow(image_a)
    for i, v in enumerate(vertices_a):
        avg_color = calculate_average_color(image_a, v)
        ax[0].fill([p[0] for p in v], [p[1] for p in v], color=avg_color / 255, edgecolor='black')
        # label_triangle(ax[0], v, str(i))
    ax[0].set_title('Image A')
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    
    # Plot the triangulation for image B
    ax[1].imshow(image_b)
    for i, v in enumerate(vertices_b):
        if i in [item for sublist in indices_to_copy for item in sublist]:
            avg_color = calculate_average_color(image_a, v)  # Use image A for color calculation
        else:
            avg_color = calculate_average_color(image_b, v)  # Use image B for color calculation
        ax[1].fill([p[0] for p in v], [p[1] for p in v], color=avg_color / 255, edgecolor='black')
        # label_triangle(ax[1], v, str(i))
    ax[1].set_title('Image B')
    ax[1].set_xticks([])
    ax[1].set_yticks([])
    
    plt.show()
