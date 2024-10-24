import sympy as sp

# 定义变量
a, b = sp.symbols('a b')
c = sp.symbols('c')

# 定义方程
lhs = (12 + 2 * sp.cos(a) - 2.5 * sp.cos(b))**2 + (1 + sp.sin(a) - 2.5 * sp.sin(b))**2
rhs = 11.2**2
equation = sp.Eq(lhs, rhs)

# 解方程
solutions = sp.solve(equation, b)

# 输出结果
for sol in solutions:
    print(f"b = {sol}")
