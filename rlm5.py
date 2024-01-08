"Scatter plot with legend"

from reportlab.lib.colors import (
    black,
    rgb2cmyk,
    toColor,
    red,
    green,
    blue,
    fade,
    PCMYKColor,
    CMYKColor,
)
from reportlab.graphics.charts.lineplots import ScatterPlot
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.lib.validators import Auto
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.pdfbase.pdfmetrics import (
    stringWidth,
    EmbeddedType1Face,
    registerTypeFace,
    Font,
    registerFont,
)
from reportlab.graphics.charts.textlabels import Label


class ScatterChart01(_DrawingEditorMixin, Drawing):
    """
    Chart Features
    --------------

    - The maximum number of rows in the legend is ONE, 
    which forces the legend to grow horizontally.

    - There is some dynamic bit of code there that decides 
    through the data where the crosshair should go.
    """

    def __init__(self, width=144, height=85, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)
        # common values
        strokeDashArray = 1, 1
        main_color = PCMYKColor(32, 0, 18, 44)
        fontName = "Helvetica"
        fontSize = 6

        self._add(
            self,
            ScatterPlot(),
            name="chart",
            validate=None,
            desc=None,
        )

        self.chart.leftPadding = 0
        self.chart.rightPadding = 0
        self.chart.topPadding = 0
        self.chart.bottomPadding = 0
        self.chart.lineLabelFormat = None
        self.chart.outerBorderColor = black
        # chart x axis
        self.chart.xValueAxis.labels.fontName = fontName
        self.chart.xValueAxis.labels.fontSize = fontSize
        # self.chart.xValueAxis.valueStep             = 2
        self.chart.xValueAxis.visibleGrid = 1
        self.chart.xValueAxis.gridStrokeDashArray = strokeDashArray
        self.chart.xValueAxis.minimumTickSpacing = 10
        self.chart.xValueAxis.maximumTicks = 8
        self.chart.xValueAxis.forceZero = 1
        self.chart.xValueAxis.avoidBoundFrac = 1  # 0.5
        self.chart.xValueAxis.visibleTicks = False
        # chart y axis
        self.chart.yValueAxis.labels.fontName = fontName
        self.chart.yValueAxis.labels.fontSize = fontSize
        self.chart.yValueAxis.labelTextFormat = None
        self.chart.yValueAxis.visibleGrid = 1
        self.chart.yValueAxis.gridStrokeDashArray = strokeDashArray
        self.chart.yValueAxis.drawGridLast = False
        self.chart.yValueAxis.minimumTickSpacing = 10
        self.chart.yValueAxis.maximumTicks = 8
        self.chart.yValueAxis.forceZero = 1
        self.chart.yValueAxis.avoidBoundFrac = 1  # 0.5
        self.chart.yValueAxis.visibleTicks = False
        # chart labels
        self.chart.xLabel = ""
        self.chart.yLabel = ""
        # chart legend
        self._add(
            self, Legend(), name="legend", validate=None, desc=None
        )
        self.legend.fontName = fontName
        self.legend.strokeWidth = 0
        self.legend.strokeColor = None
        self.legend.boxAnchor = "w"
        self.legend.alignment = "right"
        self.legend.dx = self.legend.dy = 6
        self.legend.deltax = 30
        self.legend.deltay = 0
        self.legend.dxTextSpace = 2
        self.legend.columnMaximum = 1
        self.legend.variColumn = 1
        # xal
        self._add(self, Label(), name="xal", validate=None, desc=None)
        self.xal.fontName = fontName
        # yal
        self._add(self, Label(), name="yal", validate=None, desc=None)
        self.yal.fontName = fontName
        self.yal.angle = 90
        # self.yal.boxAnchor='s'
        self.yal.textAnchor = "middle"
        # symbol styles
        self.chart.lines.symbol = makeMarker("FilledSquare")
        # sample data
        self._data = [
            (u"Portfolio", 2.25, 4.4800000000000004),
            (u"Index", 3.5899999999999999, 4.4199999999999999),
            (u"Universe Mean", 3.52, 3.48),
        ]
        self._primary = 2
        self._crossHairStrokeWidth = 2
        self._colorsList = [
            PCMYKColor(0, 59, 100, 18, alpha=100),
            PCMYKColor(0, 44.25, 75, 13.5, alpha=100),
            PCMYKColor(0, 29.5, 50, 9, alpha=100),
            PCMYKColor(0, 14.75, 25, 4.5, alpha=100),
        ]
        # self._crossHairStrokeColor = black
        self.xal._text = "5-year annualized standard deviation"
        self.yal._text = "5-year average\nannual return (%)"
        for i, color in enumerate(
            fade(main_color, [100, 75, 50, 25])
        ):
            self.chart.lines[i].strokeColor = color
        # self.chart.lines[0].strokeColor = toColor(rgb2cmyk(*red.rgb()))
        # self.chart.lines[1].strokeColor = toColor(rgb2cmyk(*green.rgb()))
        # self.chart.lines[2].strokeColor = toColor(rgb2cmyk(*blue.rgb()))
        self.height = 200
        self.chart.y = 50
        self.chart.x = 50
        self.xal.boxAnchor = "w"
        self.xal.x = 50
        self.xal.y = 30
        self.legend.x = 50
        self.yal.boxAnchor = "c"
        self.yal.y = 100
        self.yal.x = 25
        self.yal.fontSize = 8
        self.xal.fontSize = 8
        self.legend.y = 15
        self.legend.fontSize = 8
        self.chart.lines.symbol.size = 6
        self.chart.lines[0].strokeColor = PCMYKColor(
            100, 0, 90, 50, alpha=100
        )
        self.chart.lines[2].strokeColor = PCMYKColor(
            100, 60, 0, 50, alpha=100
        )
        self.chart.lines.strokeWidth = 1
        self.chart.data = [
            [(2.25, 4.48)],
            [(3.59, 4.42)],
            [(3.52, 3.58)],
        ]
        self.chart.height = 125
        self.chart.lines[1].strokeColor = PCMYKColor(
            0, 100, 100, 40, alpha=100
        )
        self.width = 400
        self.chart.width = 250

    def getContents(self):
        chart = self.chart
        # get the data using a helper function. Put into the plot in the right way
        d = self._data
        sd = [tuple(x[1:]) for x in d]
        nd = len(sd)
        self.chart.data = [[x] for x in sd]
        for i in range(nd):
            chart.lines[i].symbol = chart.lines.symbol
        for i in range(nd):
            chart.lines[i].symbol.size = chart.lines.symbol.size
        # make up the legend text using the helper instance
        self.legend.colorNamePairs = [
            (Auto(obj=chart), d[i][0]) for i in range(nd)
        ]
        primary = self._primary
        # for valid primary add a cross
        if 0 < primary < nd:
            chart.addCrossHair(
                "pch",
                sd[primary][0],
                sd[primary][1],
                strokeColor=self.chart.lines[primary].strokeColor,
                strokeWidth=self._crossHairStrokeWidth,
            )
        return Drawing.getContents(self)


# ScatterChart01().save(formats=["pdf"], outDir="/home/kdog3682/2024/", fnRoot="test")
# /home/kdog3682/2024/test.pdf
