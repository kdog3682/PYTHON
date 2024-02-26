# from fractions import Fraction
from utils import *
# pprint(Fraction(4.25) + Fraction(3.75))

from sympy import *

x, t, z, nu, y = symbols('x t z nu y')
# pprint(solve(x**2 - 2, x))

# expr = cos(x) + 1
# print(expr)
# print(expr.subs(x, y))
# print(expr)

# str_expr = "x^2 + 3*x - 1/2"
# print(sympify(str_expr))

# print(factor(x**3 - x**2 + x - 1))
# print(factor(x**2*z + 4*x*y*z + 4*y**2*z))

# print(cancel((x**2 + 2*x + 1)/(x**2 + x)))


x, y = symbols('x y', positive=True)
a, b = symbols('a b', real=True)
z, t, c = symbols('z t c')

s = """
    
# powsimp("x^ax^b")
# powsimp(z**2*t**2)
# powsimp(sqrt(x)*sqrt(y))

# solve([x**2 + y - 2*z, y + 4*z], x, y, dict=True)

# solve("x^2 = 1")

# factor("x^2 + 5x + 6 // x + 2")

expand((x + 1) * (x + 2))
"""

# s = replace_quotes(remove_comments(s), sympify_wrapper)
# run_tests(s, locals())


