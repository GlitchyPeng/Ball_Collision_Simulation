import os
import math
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# Constants for the simulation
e1 = 0.9  # Coefficient of restitution for ball-ball collisions
e2 = 0.95  # Coefficient of restitution for ball-wall collisions
r = 1.0  # Radius of each ball
l = 10.0  # Side length of the cubic box
simulation_time = 100.0

# Data structure to store collision points
collision_points = []

# Function to update positions and velocities of balls, and detect collisions
def update_positions_and_velocities(balls, dt, current_time):
    global collision_points
    # Calculate acceleration components dynamically based on current_time
    a1 = 10 * math.sin(4 * math.pi * current_time)
    a3 = 0.5 + 3 * math.sin(4 * math.pi * current_time)

    for ball in balls:
        # Update velocity with acceleration
        ball.vx += a1 * dt
        ball.vy += 0.0 * dt  # a2 is zero as per your setup
        ball.vz += a3 * dt
        
        # Update position
        ball.x += ball.vx * dt
        ball.y += ball.vy * dt
        ball.z += ball.vz * dt
        
        # Check for collisions with walls
        if ball.x - r <= 0 or ball.x + r >= l:
            ball.vx *= -e2
            ball.x = max(min(ball.x, l - r), r)
            if ball.x == r or ball.x == l - r:
                collision_points.append((ball.x, ball.y, ball.z, 'wall'))
        
        if ball.y - r <= 0 or ball.y + r >= l:
            ball.vy *= -e2
            ball.y = max(min(ball.y, l - r), r)
            if ball.y == r or ball.y == l - r:
                collision_points.append((ball.x, ball.y, ball.z, 'wall'))
        
        if ball.z - r <= 0 or ball.z + r >= l:
            ball.vz *= -e2
            ball.z = max(min(ball.z, l - r), r)
            if ball.z == r or ball.z == l - r:
                collision_points.append((ball.x, ball.y, ball.z, 'wall'))
        
        # Check for collisions with other balls
        for other in balls:
            if other != ball:
                dx = other.x - ball.x
                dy = other.y - ball.y
                dz = other.z - ball.z
                distance = math.sqrt(dx**2 + dy**2 + dz**2)
                if distance <= 2 * r:
                    # Simple elastic collision response
                    normal = (dx / distance, dy / distance, dz / distance)
                    v1n = ball.vx * normal[0] + ball.vy * normal[1] + ball.vz * normal[2]
                    v2n = other.vx * normal[0] + other.vy * normal[1] + other.vz * normal[2]
                    
                    # Update velocities
                    ball.vx += (v2n - v1n) * normal[0] * e1
                    ball.vy += (v2n - v1n) * normal[1] * e1
                    ball.vz += (v2n - v1n) * normal[2] * e1
                    other.vx += (v1n - v2n) * normal[0] * e1
                    other.vy += (v1n - v2n) * normal[1] * e1
                    other.vz += (v1n - v2n) * normal[2] * e1

                    # Slightly separate the balls to prevent sticking
                    separation_dist = 2 * r - distance + 0.01
                    ball.x -= normal[0] * separation_dist / 2
                    ball.y -= normal[1] * separation_dist / 2
                    ball.z -= normal[2] * separation_dist / 2
                    other.x += normal[0] * separation_dist / 2
                    other.y += normal[1] * separation_dist / 2
                    other.z += normal[2] * separation_dist / 2

                    # Record collision point at the moment of contact with relative speed
                    relative_speed = abs(v2n - v1n)
                    collision_points.append((ball.x, ball.y, ball.z, 'ball', relative_speed))

# Function to simulate the motion of balls
def simulate_balls(num_balls):
    balls = [Ball(random.uniform(r, l-r), random.uniform(r, l-r), random.uniform(r, l-r), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(num_balls)]
    dt = 0.01  # Time step
    current_time = 0
    while current_time < simulation_time:
        update_positions_and_velocities(balls, dt, current_time)
        current_time += dt
    return balls

# Example usage
class Ball:
    def __init__(self, x, y, z, vx, vy, vz):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

# Plotting function
def plot_and_save(balls, num_balls):
    # Create a DataFrame and plot the data
    df = pd.DataFrame(collision_points, columns=['x', 'y', 'z', 'type', 'speed'])
    wall_collisions = df[df['type'] == 'wall']
    ball_collisions = df[df['type'] == 'ball']

# Plotting with color gradient based on relative speed
    cmap = cm.get_cmap('viridis')
    norm = plt.Normalize(df['speed'].min(), df['speed'].max())
    plt.rcParams['font.family'] = 'Times New Roman'
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(wall_collisions['x'], wall_collisions['y'], wall_collisions['z'], color='red', label='Wall Collisions')
    sc = ax.scatter(ball_collisions['x'], ball_collisions['y'], ball_collisions['z'], c=ball_collisions['speed'], cmap=cmap, norm=norm, label='Ball Collisions')
    cbar = fig.colorbar(sc, ax=ax, pad=0.15)
    cbar.set_label('Relative Speed', fontsize=12)
    ax.set_xlabel('X Position', fontsize=12)
    ax.set_ylabel('Y Position', fontsize=12)
    ax.set_zlabel('Z Position', fontsize=12)
    ax.set_title('Collision Points', fontsize=18)
    ax.legend()
    ax.set_xlim([0, l])
    ax.set_ylim([0, l])
    ax.set_zlim([0, l])
    ax.set_xticks(np.linspace(0, l, num=5))
    ax.set_yticks(np.linspace(0, l, num=5))
    ax.set_zticks(np.linspace(0, l, num=5))
    ax.tick_params(axis='both', which='major', labelsize=12)
    plt.savefig(f'/Users/stanleypeng/Downloads/CollisionGraphs/collision_{num_balls}_balls.png')
    plt.close()

# Run simulations for different numbers of balls
for num_balls in [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30]:
    balls = simulate_balls(num_balls)
    plot_and_save(balls, num_balls)

# Save collision points to a text file
with open('collision_points.txt', 'w') as file:
    for index, row in df.iterrows():
        file.write(f"{row['x']}, {row['y']}, {row['z']}, {row['type']}\n")

# Constants for the simulation
speed_threshold = 0.1  # Minimum speed to register a collision

# Function to check and handle wall collisions
def check_wall_collision(ball, axis, size, restitution):
    position = getattr(ball, axis)
    velocity = getattr(ball, f'v{axis}')
    if position - r <= 0 or position + r >= size:
        if position - r <= 0:
            corrected_position = r
        else:
            corrected_position = size - r

        # Calculate the relative speed at the point of collision
        relative_speed = abs(velocity)

        # Only record if the relative speed is above the threshold and there's a significant position correction
        if relative_speed > speed_threshold and abs(corrected_position - position) > 0.01:
            setattr(ball, axis, corrected_position)
            setattr(ball, f'v{axis}', -velocity * restitution)
            collision_points.append((ball.x, ball.y, ball.z, 'wall'))
            print(f"Collision at {axis.upper()}: Pos={position}, Vel={velocity}, CorrPos={corrected_position}, Speed={relative_speed}")

for ball in balls:
    check_wall_collision(ball, 'x', l, e2)
    check_wall_collision(ball, 'y', l, e2)
    check_wall_collision(ball, 'z', l, e2)

plt.rcParams['font.size'] = 20  # Sets the default font size to 12
plt.rcParams['axes.labelsize'] = 20  # Specific for axis labels
plt.rcParams['axes.titlesize'] = 20  # Specific for titles
plt.rcParams['xtick.labelsize'] = 16  # Specific for x-tick labels
plt.rcParams['ytick.labelsize'] = 16  # Specific for y-tick labels
