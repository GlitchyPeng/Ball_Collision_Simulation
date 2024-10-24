import numpy as np
import matplotlib.pyplot as plt

# Constants
mag_moment = 1.0  
d = 2.0  # Distance between gear centers
arm_length = 1.0
initial_omega = 1.0  # rad/s
inertia = 0.5  
dt = 0.01
total_time = 10.0

# Functions
def magnetic_force(pos1, pos2):
    r = np.linalg.norm(pos1 - pos2)
    force_magnitude = mag_moment / r**4
    force_direction = (pos2 - pos1) / r
    return force_magnitude * force_direction

def calculate_torque(gear, other_gear):
    torque = np.array([0.0, 0.0, 0.0])
    for i in range(3):
        magnet_pos = gear[0] + arm_length * np.array([np.cos(gear[1] + 2*i*np.pi/3), 
                                                      np.sin(gear[1] + 2*i*np.pi/3), 0])
        for j in range(3):
            other_pos = other_gear[0] + arm_length * np.array([np.cos(other_gear[1] + 2*j*np.pi/3), 
                                                               np.sin(other_gear[1] + 2*j*np.pi/3), 0])
            force = magnetic_force(magnet_pos, other_pos)
            r = magnet_pos - gear[0]
            torque += np.cross(r, force)
    return torque

def update_state(gears, dt):
    for gear in gears:
        gear[2] += gear[3] * dt  # Update angle
        torque = calculate_torque(gear, gears[1-gears.index(gear)])
        angular_acc = torque[2] / inertia 
        gear[3] += angular_acc * dt  # Update angular velocity 

# ... (Rest of the code is in the next response) 
# Simulation Setup
gears = [
    [np.array([0.0, 0.0, 0.0]), 0.0, 0.0, initial_omega],  # Gear 1
    [np.array([d, 0.0, 0.0]), 0.0, 0.0, 0.0]              # Gear 2
]

time_steps = int(total_time / dt)
angles1 = np.zeros(time_steps)
angles2 = np.zeros(time_steps)

# Simulation Loop
for t in range(time_steps):
    # Calculate magnet positions, torques, update state (See previous response)
    update_state(gears, dt) 

    # Store angles
    angles1[t] = gears[0][1]
    angles2[t] = gears[1][1]

# Plotting
plt.plot(np.arange(0, total_time, dt), angles1, label='Gear 1')
plt.plot(np.arange(0, total_time, dt), angles2, label='Gear 2')
plt.xlabel('Time (s)')
plt.ylabel('Rotation Angle (rad)')
plt.legend()
plt.title('Magnetic Gear Simulation')
plt.grid(True)
plt.show()

