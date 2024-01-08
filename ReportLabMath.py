from utils import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


BaseFonts = [
    "symbola.otf",
    "minion.ttf",
    "minion-bold.ttf",
]

def register_fonts(fonts = BaseFonts):
    for font in fonts:
        name = match(font, "[\w-]+")
        path = "/home/kdog3682/2023/fonts/" + font
        pdfmetrics.registerFont(TTFont(name, path))

from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing, Rect, Circle
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

register_fonts()

def draw_bar_graph(drawing, data, width, height):
    bar = VerticalBarChart()
    bar.x = 0
    bar.y = 0
    bar.height = height
    bar.width = width
    bar.data = data
    bar.fillColor = colors.lightblue
    bar.strokeColor = colors.black
    drawing.add(bar)

def draw_scatter_plot(drawing, data, width, height):
    for (x, y) in data:
        # Scale or adjust x and y as per your coordinate system
        drawing.add(Circle(x, y, 2, fillColor=colors.red, strokeColor=colors.red))

def draw_data_table(doc, data):
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'minion'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    doc.append(table)

def create_pdf(path):
    doc = SimpleDocTemplate(path, pagesize=letter)
    story = []
    drawing = Drawing(400, 200)

    # Sample Data
    bar_data = [[1, 2, 3, 4, 5]]
    scatter_data = [(10, 20), (30, 40), (50, 60), (70, 80)]
    table_data = [['X', 'Y']] + scatter_data

    # Draw Components
    draw_bar_graph(drawing, bar_data, 400, 200)
    draw_scatter_plot(drawing, scatter_data, 400, 200)
    draw_data_table(story, table_data)

    # Add to Story
    story.append(drawing)
    doc.build(story)

create_pdf("/home/kdog3682/2024/sample_graphs.pdf")

from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.scatterplots import ScatterPlot
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

class BarGraph(Drawing):
    def __init__(self, width, height, data):
        Drawing.__init__(self, width, height)
        self.add(VerticalBarChart(), name='chart')
        self.chart.data = data
        self.chart.x = 50
        self.chart.y = 50
        self.chart.width = width - 100
        self.chart.height = height - 100
        self.chart.fillColor = colors.lightblue
        self.add(String(200, height - 30, 'Bar Graph', fontName='minion', fontSize=14))

class ScatterGraph(Drawing):
    def __init__(self, width, height, data):
        Drawing.__init__(self, width, height)
        self.add(ScatterPlot(), name='plot')
        self.plot.data = [data]
        self.plot.x = 50
        self.plot.y = 50
        self.plot.width = width - 100
        self.plot.height = height - 100
        self.plot.fillColor = colors.lightblue
        self.add(String(200, height - 30, 'Scatter Plot 123', fontName='symbola', fontSize=14))

def draw_data_table(doc, data):
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'minion-bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    doc.append(table)

def create_pdf(path):
    doc = SimpleDocTemplate(path, pagesize=letter)
    story = []

    # Sample Data
    bar_data = [[1, 2, 3, 4, 5]]
    scatter_data = [(10, 20), (30, 40), (50, 60), (70, 80)]
    table_data = [['X', 'Y']] + scatter_data

    # Create Graphs
    bar_graph = BarGraph(400, 200, bar_data)
    scatter_graph = ScatterGraph(400, 200, scatter_data)

    # Draw Components
    draw_data_table(story, table_data)

    # Add to Story
    story.append(bar_graph)
    story.append(scatter_graph)
    doc.build(story)


create_pdf("/home/kdog3682/2024/sample_graphs.pdf")
