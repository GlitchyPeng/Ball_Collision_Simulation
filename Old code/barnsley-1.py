import matplotlib.pyplot as plt
import numpy as np

# Define the Barnsley fern transformation matrices and probabilities
transformations = [
    [[0, 0], [0, 0.16], 0.01],
    [[0.85, 0.04], [-0.04, 0.85], 0.85],
    [[0.2, -0.26], [0.23, 0.22], 0.07],
    [[-0.15, 0.28], [0.26, 0.24], 0.07]
]

# Initialize starting point
x, y = 0, 0

# Number of iterations (points to plot)
iterations = 100000

# Generate the points for the fern
points = []
for _ in range(iterations):
    indices = np.arange(len(transformations))
    index = np.random.choice(indices, p=[t[2] for t in transformations])
    transformation = transformations[index]
    x, y = transformation[0][0] * x + transformation[0][1] * y + transformation[1][0], transformation[0][0] * y + transformation[0][1] * x + transformation[1][1]
    points.append([x, y])

# Plot the fern
points = np.array(points)
plt.scatter(points[:, 0], points[:, 1], s=0.1, color='green')
plt.axis('off')
plt.show()
