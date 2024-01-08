from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib import colors
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class BarChartComponent:
    def __init__(self, width, height, data, title, x_axis_label, y_axis_label):
        self.width = width
        self.height = height
        self.data = data
        self.title = title
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label

    def create_chart(self):
        drawing = Drawing(self.width, self.height)
        bar_chart = VerticalBarChart()
        bar_chart.x = 50
        bar_chart.y = 85
        bar_chart.height = self.height - 150
        bar_chart.width = self.width - 100
        bar_chart.data = self.data

        bar_chart.valueAxis.valueMin = 0
        bar_chart.categoryAxis.labels.boxAnchor = 'ne'
        bar_chart.categoryAxis.labels.angle = 45

        # Title
        title = Label()
        title.setOrigin(self.width/2, self.height-20)
        title.boxAnchor = 'n'
        title.setText(self.title)
        drawing.add(title)

        # X-axis label
        x_label = Label()
        x_label.setOrigin(self.width/2, 30)
        x_label.boxAnchor = 'n'
        x_label.setText(self.x_axis_label)
        drawing.add(x_label)

        # Y-axis label
        y_label = Label()
        y_label.setOrigin(15, self.height/2)
        y_label.boxAnchor = 'e'
        y_label.angle = 90
        y_label.setText(self.y_axis_label)
        drawing.add(y_label)

        drawing.add(bar_chart)
        return drawing

def save_pdf(drawing, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    renderPDF.draw(drawing, c, 100, 400)
    c.save()

# Sample data and usage
data = [(50, 100, 150, 200, 250)]
bar_chart_component = BarChartComponent(400, 200, data, "Sales Over Time", "Year", "Sales ($)")
bar_chart_drawing = bar_chart_component.create_chart()

save_pdf(bar_chart_drawing, "/home/kdog3682/2024/test.pdf")
