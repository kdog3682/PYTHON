from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm

from reportlab.platypus import Flowable
from reportlab.lib.styles import getSampleStyleSheet

class InlineFractionFlowable(Flowable):
    def __init__(self, numerator, denominator, font_size=12):
        Flowable.__init__(self)
        self.numerator = numerator
        self.denominator = denominator
        self.font_size = font_size

    def draw(self):
        # Set font for measurements
        font_name = "Helvetica"
        self.canv.setFont(font_name, self.font_size)

        # Calculate widths
        num_width = self.canv.stringWidth(self.numerator, font_name, self.font_size)
        den_width = self.canv.stringWidth(self.denominator, font_name, self.font_size)
        max_width = max(num_width, den_width)

        # Calculate positions
        num_x = (max_width - num_width) / 2
        den_x = (max_width - den_width) / 2
        line_y = self.height / 2
        num_y = line_y + 3
        den_y = line_y - self.font_size - 3

        # Draw numerator, line, and denominator
        self.canv.drawString(num_x, num_y, self.numerator)
        self.canv.line(0, line_y, max_width, line_y)
        self.canv.drawString(den_x, den_y, self.denominator)

        # Set width to the maximum width of numerator or denominator
        self.width = max_width


# Setup Canvas
canvas = Canvas('/home/kdog3682/2024/test.pdf', pagesize=letter)

# Create a Text Object
text_object = canvas.beginText(40 * mm, 200 * mm)  # Starting position
text_object.setFont("Helvetica", 12)

# Add text before the fraction
text_object.textOut("This is a fraction: ")

# Current position
current_x = text_object.getX()
current_y = text_object.getY()

# Draw the fraction at the current position
fraction_flowable = InlineFractionFlowable("1", "2", 12)
fraction_flowable.drawOn(canvas, current_x, current_y - 12)  # Adjust Y-offset for vertical alignment
print(fraction_flowable.width)

# Move the text position past the fraction
text_object.moveCursor(fraction_flowable.width + 2, 0)  # 2 is a small buffer space

# text_object.textOut(" in the text.")
# canvas.drawText(text_object)
# canvas.save()

# from utils import openpdf
# openpdf()
