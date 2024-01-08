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

register_fonts()

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib.units import inch

class BarChartComponent:
    def __init__(self, width, height, data, title, x_axis_label, y_axis_label, font_name):
        self.width = width
        self.height = height
        self.data = data
        self.title = title
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.font_name = font_name

    def create_bar_chart(self):
        drawing = Drawing(self.width, self.height)
        bar_chart = VerticalBarChart()
        bar_chart.x = 50
        bar_chart.y = 85
        bar_chart.height = self.height - 100
        bar_chart.width = self.width - 100
        bar_chart.data = self.data
        bar_chart.valueAxis.valueMin = 0
        bar_chart.categoryAxis.labels.fontName = self.font_name
        bar_chart.categoryAxis.labels.angle = 30
        bar_chart.categoryAxis.labels.dx = -10
        bar_chart.categoryAxis.labels.dy = -10
        drawing.add(bar_chart)
        return drawing

class BasicGraphComponent:
    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self.data = data

    def create_basic_graph(self):
        drawing = Drawing(self.width, self.height)
        graph = LinePlot()
        graph.x = 50
        graph.y = 85
        graph.height = self.height - 100
        graph.width = self.width - 100
        graph.data = self.data
        graph.joinedLines = False
        for i in range(len(self.data)):
            graph.lines[i].symbol = makeMarker('Circle')
        drawing.add(graph)
        return drawing

class DocumentGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=letter)

    def generate_pdf(self, components):
        story = []
        for component in components:
            story.append(component)
            story.append(Spacer(1, 12))

        self.doc.build(story)

# Sample data for the charts
bar_data = [
    [10, 20, 30, 40],
    [50, 60, 70, 80]
]

# Data for basic graph
graph_data = [[(1, 10), (2, 20), (3, 30), (4, 40)]]

# Create chart components
bar_chart_component = BarChartComponent(400, 200, bar_data, "Bar Chart", "X-Axis", "Y-Axis", "minion-bold")
basic_graph_component = BasicGraphComponent(400, 200, graph_data)

# Create bar chart and basic graph
bar_chart = bar_chart_component.create_bar_chart()
basic_graph = basic_graph_component.create_basic_graph()

# Generate PDF
doc_generator = DocumentGenerator("/home/kdog3682/2024/test.pdf")
doc_generator.generate_pdf([bar_chart, basic_graph])
