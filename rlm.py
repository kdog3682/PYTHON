from rl_setup_fonts import register_fonts
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

register_fonts(key = "chinese")

# Your JSON structure
expression_json = {
  "type": "operation",
  "operator": "+",
  "operands": [
    {
      "type": "operation",
      "operator": "^",
      "operands": [
        { "type": "number", "value": 2 },
        { "type": "number", "value": 3 }
      ]
    },
    {
      "type": "operation",
      "operator": "/",
      "operands": [
        { "type": "number", "value": 1 },
        { "type": "number", "value": 3 }
      ]
    }
  ]
}

def get(expr):
    type = expr.get("type")
    value = expr.get("value")
    args = expr.get("args")
    operands = expr.get("operands")
    operator = expr.get("operator")
    return [type, value, args, operands, operator]

def draw(canvas, x, y, value, move = 0, font = 0, font_size = 0):
    
    if font or font_size or bold:
        canvas.saveState()
        if font:
            canvas.setFont(font)
        canvas.drawString(x, y, str(value))
        canvas.restoreState()
    else:
        canvas.drawString(x, y, str(value))
    if move:
        return x + move
def render(expr, x, y, canvas):
    canvas.setFont("Minion")
    type, value, operator = get(expr)
    if type == 'number':
        return draw(canvas, x, y, value, move = 10)
    if type == 'operation':
        if operator == '+':
            x = render(expr['operands'][0], x, y, canvas)
            canvas.drawString(x, y, '+')
            x = render(expr['operands'][1], x + 20, y, canvas)  # Space for operator
        elif operator == '^':
            x = render(expr['operands'][0], x, y, canvas)
            x = render(expr['operands'][1], x, y + 10, canvas)  # Shift for exponent
        elif operator == '/':
            canvas.line(x, y, x + 40, y)  # Fraction line
            x = render(expr['operands'][0], x, y + 15, canvas)  # Above line
            x = render(expr['operands'][1], x, y - 15, canvas)  # Below line
        return x

# Create a PDF with ReportLab
c = canvas.Canvas("/home/kdog3682/2024/test.pdf", pagesize=letter)
x_start, y_start = inch, 10 * inch  # Starting position
render(expression_json, x_start, y_start, c)
c.save()

from utils import openpdf
openpdf()
