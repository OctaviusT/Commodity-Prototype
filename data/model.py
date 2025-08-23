# Let's create a basic CAD model for a miniature Hellfire-inspired missile using Matplotlib's 3D plotting library.
# The model will include the missile body, nose cone, tail fins, and the attachment point.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Function to generate the cylindrical body
def create_cylinder(radius, height, segments=50):
    theta = np.linspace(0, 2 * np.pi, segments)
    z = np.linspace(0, height, 2)
    theta, z = np.meshgrid(theta, z)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return x, y, z

# Function to generate the conical nose
def create_cone(radius, height, segments=50):
    theta = np.linspace(0, 2 * np.pi, segments)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.zeros_like(x)
    vertices = [[0, 0, height]] + [[x[i], y[i], z[i]] for i in range(len(x))]
    faces = [[0] + list(range(1, len(x) + 1))]
    return vertices, faces

# Function to create fins
def create_fins(length, height, width, num_fins=4):
    fins = []
    angles = np.linspace(0, 2 * np.pi, num_fins, endpoint=False)
    for angle in angles:
        # Define a simple fin shape
        x = [0, length, length, 0]
        y = [0, width / 2, -width / 2, 0]
        z = [0, 0, 0, height]
        # Rotate the fin into position
        rotation = np.array([[np.cos(angle), -np.sin(angle), 0],
                              [np.sin(angle), np.cos(angle), 0],
                              [0, 0, 1]])
        fin = np.dot(rotation, np.array([x, y, z]))
        fins.append(fin.T)
    return fins

# Create the missile body
radius = 1  # 1-inch radius
body_height = 10  # 10 inches long
x, y, z = create_cylinder(radius, body_height)

# Create the nose cone
nose_radius = radius
nose_height = 3  # 3-inch tall cone
vertices, faces = create_cone(nose_radius, nose_height)

# Create tail fins
fin_length = 2  # 2-inch fin length
fin_height = 0.5  # 0.5-inch fin height
fin_width = 0.2  # 0.2-inch fin width
fins = create_fins(fin_length, fin_height, fin_width)

# Plot the model
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d', proj_type='ortho')
ax.set_box_aspect([2, 2, 3])  # Aspect ratio

# Plot the cylindrical body
ax.plot_surface(x, y, z, color="gray", alpha=0.8, edgecolor='none')

# Plot the nose cone
for face in faces:
    poly3d = [[vertices[vert] for vert in face]]
    ax.add_collection3d(Poly3DCollection(poly3d, color="lightgray", alpha=0.8))

# Plot the fins
for fin in fins:
    ax.add_collection3d(Poly3DCollection([fin], color="darkgray", alpha=0.9))

# Adjust the viewing angle
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])
ax.set_zlim([0, 15])
ax.view_init(elev=20, azim=30)
ax.set_title("Miniature Hellfire Missile CAD Model", fontsize=14)

plt.show()
