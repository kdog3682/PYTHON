from latex2sympy2 import latex2sympy as sympify

def pre(expr):
    print(expr)
    for arg in expr.args:
        pre(arg)


def sympy_tree_to_json(expr):
    """
    Recursively walk through a sympy expression tree to construct a JSON object.
    """
    if expr.is_Symbol or expr.is_Number or expr.is_constant():
        # Base case for symbols, numbers, and constants
        print_object_attribute_values(expr)
        return str(expr)
    elif expr.is_Function or expr.is_Pow or expr.is_Mul or expr.is_Add:
        # Recursive case for functions and operations
        return {
            "type": type(expr).__name__,
            "args": [sympy_tree_to_json(arg) for arg in expr.args]
        }
    else:
        return str(expr)

# Example usage
# latex_expression = "x^2 + y^2"
# latex_expression = "x^2 + y^2 + \\frac{1}{3}"
# latex_expression = "\\frac{1}{3}"
# expr = sympify(latex_expression)
# json_tree = sympy_tree_to_json(expr)
# print(json_tree)

# PDF Documents ...


from sympy import symbols, Eq, solve

x = symbols('x')
expr = sympify("x^2 - 5x + 6")
equation = Eq(expr, 0)

solutions = solve(equation, x)
print("Solutions:", solutions)
