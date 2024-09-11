import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

# Constants for the simulation
e1 = 0.9  # Coefficient of restitution for ball-ball collisions
e2 = 0.95  # Coefficient of restitution for ball-wall collisions
r = 1.0  # Radius of each ball
l = 10.0  # Side length of the cubic box
a1, a2, a3 = 0.0, 0.0, -9.81  # Acceleration field components (gravity in z-direction)
NUM_BALLS = 10
# Time after which to display the collision points
simulation_time = 100.0

# Data structure to store collision points
collision_points = []

# Function to update positions and velocities of balls, and detect collisions
def update_positions_and_velocities(balls, dt):
    global collision_points
    for ball in balls:
        # Update velocity with acceleration
        ball.vx += a1 * dt
        ball.vy += a2 * dt
        ball.vz += a3 * dt
        
        # Update position
        ball.x += ball.vx * dt
        ball.y += ball.vy * dt
        ball.z += ball.vz * dt
        
        # Check for collisions with walls
        if ball.x - r <= 0 or ball.x + r >= l:
            ball.vx *= -e2
            ball.x = max(min(ball.x, l - r), r)
            if ball.x == r or ball.x == l - r:  # Record only if there's an actual collision
                collision_points.append((ball.x, ball.y, ball.z, 'wall'))
        
        if ball.y - r <= 0 or ball.y + r >= l:
            ball.vy *= -e2
            ball.y = max(min(ball.y, l - r), r)
            if ball.y == r or ball.y == l - r:  # Record only if there's an actual collision
                collision_points.append((ball.x, ball.y, ball.z, 'wall'))
        
        if ball.z - r <= 0 or ball.z + r >= l:
            ball.vz *= -e2
            ball.z = max(min(ball.z, l - r), r)
            if ball.z == r or ball.z == l - r:  # Record only if there's an actual collision
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
                    separation_dist = 2 * r - distance + 0.01  # Small buffer to ensure separation
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
def simulate_balls(balls, total_time):
    dt = 0.01  # Time step
    current_time = 0
    while current_time < total_time:
        update_positions_and_velocities(balls, dt)
        current_time += dt

# Example usage
class Ball:
    def __init__(self, x, y, z, vx, vy, vz):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

import random

balls = [Ball(random.uniform(r, l-r), random.uniform(r, l-r), random.uniform(r, l-r), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(NUM_BALLS)]
simulate_balls(balls, simulation_time)

# Create a DataFrame and plot the data
df = pd.DataFrame(collision_points, columns=['x', 'y', 'z', 'type', 'speed'])
wall_collisions = df[df['type'] == 'wall']
ball_collisions = df[df['type'] == 'ball']

# Plotting with color gradient based on relative speed
cmap = cm.get_cmap('viridis')
norm = plt.Normalize(df['speed'].min(), df['speed'].max())
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(wall_collisions['x'], wall_collisions['y'], wall_collisions['z'], color='red', label='Wall Collisions')
sc = ax.scatter(ball_collisions['x'], ball_collisions['y'], ball_collisions['z'], c=ball_collisions['speed'], cmap=cmap, norm=norm, label='Ball Collisions')
cbar = fig.colorbar(sc, ax=ax)
cbar.set_label('Relative Speed')
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_zlabel('Z Position')
ax.set_title('Collision Points')
ax.legend()
plt.show()

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
