import numpy as np

def monte_carlo_sphere_cap(n, cap_height, num_trials=1000000):
    radius = 1  # We can assume a unit sphere
    successes = 0

    for _ in range(num_trials):
        points = np.random.rand(n, 3)  # Random points on the sphere
        points /= np.linalg.norm(points, axis=1)[:, np.newaxis]  # Normalize

        cap_center = np.random.rand(3)
        cap_center /= np.linalg.norm(cap_center)

        distances = np.dot(points, cap_center)  # Projection onto cap's axis
        if np.all(distances > radius * (1 - cap_height)): 
            successes += 1

    return successes / num_trials

# Get user input for n
n = int(input("Enter the number of points (n): ")) 
cap_height = 0.25  # You can change this if you'd like

probability = monte_carlo_sphere_cap(n, cap_height)
print("Approximate probability:", probability)

