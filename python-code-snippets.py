
"""
the power of sympy
"""
# from sympy import Symbol, sin
# from sympy.plotting import textplot
# t = Symbol('t')
# textplot(t * t - 1, -5, 5)
# absolutely amazing ... 

from sympy import *

# Calculate 60% * 3/4
result = Rational(60, 100) * Rational(3, 4)
print(result)


print(simplify("60/100 * 3/4"))
