import sympy as sp

# Define variables
t = sp.symbols('t')
r, R, L = sp.symbols('r R L')
x_A, y_A, x_B, y_B = sp.symbols('x_A y_A x_B y_B')
x_C = r * sp.cos(4 * sp.pi * t)
y_C = r * sp.sin(4 * sp.pi * t)

# Define x_D(t) and y_D(t) as unknown functions of t
x_D = sp.Function('x_D')(t)
y_D = sp.Function('y_D')(t)

# Define the system of equations
eq1 = (x_C - x_B)**2 + (y_C - y_B)**2 - r**2
eq2 = (x_D - x_A)**2 + (y_D - y_A)**2 - R**2
eq3 = (x_D - x_C)**2 + (y_D - y_C)**2 - L**2

# Solve eq3 implicitly for x_D(t) and y_D(t)
solutions = sp.solve([eq1, eq2, eq3], [x_D, y_D], dict=True)

# Extract the solutions
x_D_sol = solutions[0][x_D]
y_D_sol = solutions[0][y_D]

# First and second derivatives of x_D and y_D with respect to x_C
x_D_diff_1st = sp.diff(x_D_sol, x_C)
x_D_diff_2nd = sp.diff(x_D_diff_1st, x_C)

y_D_diff_1st = sp.diff(y_D_sol, x_C)
y_D_diff_2nd = sp.diff(y_D_diff_1st, x_C)

# Display the results
x_D_diff_2nd, y_D_diff_2nd
