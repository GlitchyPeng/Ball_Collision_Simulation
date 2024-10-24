import numpy as np
import matplotlib.pyplot as plt

# Define the parameters of the simulation
d = 0.1  # Distance between the center axes of the gears
L = 0.1  # Length of each arm
m = 0.1  # Mass of each magnet
I = m * L**2 / 12  # Moment of inertia of each gear
mu = 1e-7  # Magnetic permeability of vacuum
B = 1  # Magnetic field strength of each magnet
dt = 0.01  # Timestep
t_max = 10  # Total simulation time

# Initialize the state of the simulation
theta1 = 0  # Angle of the first gear
theta2 = 0  # Angle of the second gear
omega1 = 1  # Initial angular velocity of the first gear
omega2 = 0  # Initial angular velocity of the second gear

# Create a time array for plotting
t = np.linspace(0, t_max, num=1000)

# Simulate the motion of the gears
for i in range(1000):
    # Calculate the torque on each gear
    torque1 = -mu * B**2 * L**2 * np.sin(2 * (theta1 - theta2)) / d**4
    torque2 = mu * B**2 * L**2 * np.sin(2 * (theta1 - theta2)) / d**4

    # Update the state of the gears
    omega1 += torque1 / I * dt
    omega2 += torque2 / I * dt
    theta1 += omega1 * dt
    theta2 += omega2 * dt  # Update the angle of the second gear

# Plot the results
plt.plot(t, theta1, label="Gear 1")
plt.plot(t, theta2, label="Gear 2")
plt.xlabel("Time (s)")  # Add label for the x-axis
plt.ylabel("Angle (radians)")  # Add label for the y-axis
plt.legend()
plt.show()

