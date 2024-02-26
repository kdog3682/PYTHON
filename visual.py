from utils import *
# from sympy import Rational
# 

def splice(items, start, delete_count=None):
    """
    Removes elements from a list and returns the removed elements.

    :param items: The list from which elements will be removed.
    :param start: The zero-based location in the list from which to start removing elements.
    :param delete_count: The number of elements to remove.
    :return: A list containing the removed elements.
    """
    # Adjust negative start index
    if start < 0:
        start = max(0, start + len(items))

    # Determine the end index for removal
    if delete_count is not None:
        end = start + delete_count
    else:
        end = len(items)

    # Extract the elements to be removed
    removed_elements = items[start:end]

    # Remove the elements from the original list
    items[start:end] = []

    return removed_elements

class Calculator:
    def __init__(self):
        self.results = []
        pass
    
    def _calc(self, operation, percentage, number):
        percentage = float(percentage.strip('%'))
        pv = Rational(percentage, 100)

        if operation == 'more_than':
            return float((1 + pv) * number)
        elif operation == 'less_than':
            return float((1 - pv) * number)
        elif operation == 'of':
            return float(pv * number)
        else:
            raise ValueError(f"Operation {operation} is not supported")

    def more_than(self, percentage, number):
        return self._calc('more_than', percentage, number)

    def less_than(self, percentage, number):
        return self._calc('less_than', percentage, number)

    def of(self, percentage, number):
        return self._calc('of', percentage, number)

    def calculate(self, percentage, operation, number):
        number = float(number)
        method_name = dash_case(operation)
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            value = method(percentage, number)
            value = fix_floating_point(value)

            before = number
            after = value
            payload = {
                "final": after,
                "initial": before,
                "delta": after - before,
            }

            self.results.append(payload)
            return value
        else:
            raise ValueError(f"Operation {method_name} is not supported")


def dash_case(s):
    return s.lower().replace(' ', '_')

def parse(s):
    calculator = Calculator() 
    keys = ["of", "more than", "less than"]
    r = re_wrap(keys, "bc")
    items = map(split(s, r), trim)
    store = []
    
    while len(items) > 1:
        breaker(10)
        args = splice(items, -3)
        value = calculator.calculate(*args)
        items.append(str(value))

    return calculator.results

def fix_floating_point(value, max_precision=10):
    """
    Corrects floating point precision issues by intelligently rounding the value.

    :param value: The floating point number to round.
    :param max_precision: The maximum number of decimal places to consider.
    :return: The rounded floating point number, with insignificant trailing digits removed.
    """
    if not isinstance(value, float):
        raise ValueError("The provided value must be a float.")

    for precision in range(max_precision + 1):
        rounded_value = round(value, precision)
        if abs(value - rounded_value) < 10**-(precision + 1):
            return rounded_value

    return value  # Return the original value if no suitable rounding was found

def visual(s, **opts):
    return parse(s)
