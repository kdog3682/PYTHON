from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

# Import Minion Pro font (you should provide the path to the font file)
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register the Minion Pro font
pdfmetrics.registerFont(TTFont('MinionPro', 'path_to_minion_pro_font_file.ttf'))
addMapping('MinionPro', 0, 0, 'MinionPro')

# Create a sample PDF
doc = SimpleDocTemplate("example.pdf", pagesize=letter)

# Create a story to hold the content
story = []

# Create a custom style with Minion Pro font
custom_style = ParagraphStyle('CustomStyle')
custom_style.fontName = 'MinionPro'  # Use the registered font
custom_style.fontSize = 12
custom_style.textColor = colors.black

# Create a paragraph with custom style
text = "This is a simple ReportLab example with Minion Pro font."
paragraph = Paragraph(text, custom_style)

story.append(paragraph)

# Build the PDF
doc.build(story)


/home/kdog3682/2023/fonts/minion.ttf
