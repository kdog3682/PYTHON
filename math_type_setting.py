from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import webbrowser

def draw_equation(c):
    # Set up font and size for the equation
    c.setFont("Helvetica", 12)

    # Starting position
    x = inch
    y = letter[1] - inch

    # Draw "x^2"
    c.drawString(x, y, "x")
    c.setFont("Helvetica", 8)  # smaller font size for superscript
    c.drawString(x + 10, y + 5, "2")
    c.setFont("Helvetica", 12)  # revert to original font size

    # Draw "+ 3 ="
    x += 20  # increment x position
    c.drawString(x, y, "+ 3 =")

    # Draw fraction "1/4"
    x += 50  # increment x position
    c.drawString(x, y + 5, "1")
    c.line(x - 5, y, x + 15, y)  # fraction line
    c.drawString(x, y - 10, "4")

    # Draw "+"
    x += 20  # increment x position
    c.drawString(x, y, "+")

    # Draw fraction "1/6"
    x += 20  # increment x position
    c.drawString(x, y + 5, "1")
    c.line(x - 5, y, x + 15, y)  # fraction line
    c.drawString(x, y - 10, "6")

file = "/home/kdog3682/2023/math_equation.pdf"
c = canvas.Canvas(file, pagesize=letter)
draw_equation(c)
c.save()

webbrowser.open(file)
