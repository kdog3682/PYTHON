
from utils import *

class Polynomial:
    def __init__(self, s):
        self.expr = sympify(s)
        self.expr += 3
        self.expr += "x"
        print(self.expr)
    def __add__(self, p):
        symbol = getattr(sympy.abc, p, p) if is_string(p) else p
        print(symbol, "hi")
        return self.expr + symbol
    # def __subtract__(self, p):
    # def __mul__(self, p):
        
# a = Polynomial("x + 3")
# b = a + "x"
# print(b)


s = """
# from sympy import *
# from sympy.abc import x

a = x + 3
b = x + 2

d = ab.factor()
print(c)

"""

# exec(s)





def eat(s, pattern):
    regex = re.compile(pattern)
    while True:
        m = re.search(regex, s)
        print(m)
        return 

def parse(s):
    items = re.split()

class World:
    def __init__(self, s):
        self.s = s
        parse(s)

print(eat(s, "^\w+ *=.+"))

s = """
    # a = x + 2
    # b = x + 3

    what does ab / a equal?
    ab should naturally expand into the polynmial version
    (x^2 + 5x + 6) / (x + 2)
    // but this can happen later

    We can factor ab into ab.factor()

    box(ab.factored) ... be flexible ...

    $ab.first.coff
"""
