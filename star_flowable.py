from reportlab.lib import styles
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.flowables import Flowable
from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing, Polygon

# Step 1: Create a custom Flowable for the star
class StarFlowable(Flowable):
    def __init__(self, size):
        Flowable.__init__(self)
        self.size = size
        self.width = self.height = size

    def draw(self):
        # Draw a star
        d = Drawing(self.width, self.height)
        star = Polygon(points=[
            (0.5*self.size, 0),
            (0.6*self.size, 0.35*self.size),
            (self.size, 0.35*self.size),
            (0.7*self.size, 0.57*self.size),
            (0.8*self.size, self.size),
            (0.5*self.size, 0.75*self.size),
            (0.2*self.size, self.size),
            (0.3*self.size, 0.57*self.size),
            (0, 0.35*self.size),
            (0.4*self.size, 0.35*self.size)
        ], isClosed=True, strokeColor=None)
        d.add(star)
        renderPDF.draw(d, self.canv, 0, 0)

# Step 2: Handler function to use in Paragraph
def star_handler(canvas, doc, flowable):
    flowable.drawOn(canvas, 0, 0)
    return flowable.width

# Step 3: Create a document and a stylesheet
doc = SimpleDocTemplate('/home/kdog3682/2024/test.pdf', pagesize=letter)
style = styles.getSampleStyleSheet()['Normal']

# Register the handler
style.add('star', star_handler)

# Create a Paragraph that uses the custom flowable
text = '<star size="20"/> This is a paragraph with stars <star size="20"/>'
para = Paragraph(text, style)

# Build the document
doc.build([para])

from utils import openpdf
openpdf()
