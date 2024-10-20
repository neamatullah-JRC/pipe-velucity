import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters for the bent pipe
pipe_length = 30  # Total length of the pipe
pipe_radius = 2  # Radius of the pipe
n_points_length = 300  # Number of points along the pipe's length
n_points_radius = 20   # Number of points along the pipe's radius
pressure_inlet = 100  # High pressure at the inlet
pressure_outlet = 10  # Low pressure at the outlet
bend_angle = np.pi / 1.33  # Bending angle (45 degrees in radians)

# Create grid for cylindrical coordinates
t = np.linspace(0, 1, n_points_length)  # Parametric variable along the pipe's length
theta = np.linspace(0, 2 * np.pi, n_points_radius)  # Angle around the pipe's circumference
T, Theta = np.meshgrid(t, theta)

# Create a straight pipe first
X = pipe_radius * np.cos(Theta)
Y = pipe_radius * np.sin(Theta)
Z = pipe_length * T

# Apply smooth bending transformation along the entire length
bend_fraction = T  # Creates a gradual bending effect over the length
X_bend = X * np.cos(bend_fraction * bend_angle) + Z * np.sin(bend_fraction * bend_angle)
Z_bend = -X * np.sin(bend_fraction * bend_angle) + Z * np.cos(bend_fraction * bend_angle)
X, Z = X_bend, Z_bend

# Pressure distribution
pressure = np.linspace(pressure_inlet, pressure_outlet, n_points_length)
Pressure = np.tile(pressure, (n_points_radius, 1))

# Velocity distribution (parabolic profile for laminar flow)
r = np.linspace(0, pipe_radius, n_points_radius)
velocity_profile = 1 - (r / pipe_radius)**2  # Parabolic velocity profile
Velocity = np.tile(velocity_profile, (n_points_length, 1)).T  # Extend along the length

# Create a figure with two subplots for pressure flow and velocity field
fig = plt.figure(figsize=(18, 8))

# Subplot 1: Pressure Flow Visualization
ax1 = fig.add_subplot(121, projection='3d')
surface = ax1.plot_surface(X, Y, Z, facecolors=plt.cm.jet(Pressure / np.max(Pressure)), 
                           rstride=1, cstride=1, shade=False)

ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('Pipe with Pressure Flow')

# Add color bar to indicate pressure levels
mappable1 = plt.cm.ScalarMappable(cmap='jet')
mappable1.set_array(Pressure)
fig.colorbar(mappable1, ax=ax1, label='Pressure')

# Subplot 2: Velocity Field Visualization
ax2 = fig.add_subplot(122, projection='3d')
ax2.quiver(X, Y, Z, 
           np.zeros_like(X), np.zeros_like(Y), Velocity, 
           length=0.1, color='black', normalize=True)

ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Pipe with Velocity Field')

# Set aspect ratio to equal in both subplots to ensure the pipe appears round
ax1.set_box_aspect((np.ptp(X), np.ptp(Y), np.ptp(Z)))
ax2.set_box_aspect((np.ptp(X), np.ptp(Y), np.ptp(Z)))

plt.tight_layout()
plt.show()
