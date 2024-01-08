from rl_setup_fonts import register_fonts
register_fonts()

from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.pdfbase.pdfmetrics import stringWidth, EmbeddedType1Face, registerTypeFace, Font, registerFont
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, Rect
from reportlab.lib.colors import PCMYKColor

class PieChart04(_DrawingEditorMixin,Drawing):
    '''
        Chart Features
        --------------

        This Pie chart itself is a simple chart with exploded slices:

        - **self.pie.slices.popout = 5**
    '''
    def __init__(self,width=524,height=308,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)
        fontName = 'minion'
        fontSize = 10
        self._add(self,Pie(),name='pie',validate=None,desc=None)
        self._add(self,Legend(),name='legend',validate=None,desc=None)
        self.pie.height = 252
        self.pie.sameRadii          = 1
        self.pie.direction          = 'clockwise'
        self.pie.startAngle         = 90
        self.background = Rect(0, 0, self.width, self.height, strokeColor=PCMYKColor(100,0,0,0), fillColor=PCMYKColor(15,0,0,0))
        self.background.strokeWidth = 0.25
        #self.pie.slices[0].fillColor             = PCMYKColor(0,0,0,100)
        colors = [ PCMYKColor(100,0,0,0), PCMYKColor(100,67,0,23), PCMYKColor(0,95,100,0), PCMYKColor(0,0,0,40), PCMYKColor(10,0,100,11)]
        for i, color in enumerate(colors): self.pie.slices[i].fillColor =  color
        #self.pie.slices.strokeColor      = PCMYKColor(0,0,0,0)
        #self.pie.slices.strokeWidth      = 0.5
        self.legend.y               = 101
        self.legend.fontSize        = fontSize
        self.legend.fontName        = fontName
        self.legend.dx              = 8
        self.legend.dy              = 8
        self.legend.yGap            = 0
        self.legend.deltay          = 16
        self.legend.strokeColor     = PCMYKColor(0,0,0,0)
        self.legend.strokeWidth     = 0
        self.legend.columnMaximum   = 6
        self.legend.alignment       ='right'
        # sample data
        self.pie.data = [30.0, 21.0, 21.0, 14.0, 14.0]
        names = 'BP', 'Shell Transport & Trading', 'Liberty International', 'Persimmon', 'Royal Bank of Scotland',
        colorsList = PCMYKColor(100,0,0,0,alpha=100), PCMYKColor(100,67,0,23,alpha=100), PCMYKColor(0,95,100,0,alpha=100), PCMYKColor(0,0,0,40,alpha=100), PCMYKColor(10,0,100,11,alpha=100),
        self.pie.slices[0].fillColor             = PCMYKColor(100,0,90,50,alpha=85)
        self.pie.slices[1].fillColor             = PCMYKColor(0,100,100,40,alpha=85)
        self.pie.slices[2].fillColor             = PCMYKColor(100,60,0,50,alpha=85)
        self.pie.slices[3].fillColor             = PCMYKColor(23,51,0,4,alpha=85)
        self.pie.slices[4].fillColor             = PCMYKColor(66,13,0,22,alpha=85)
        self.background.fillColor        = None
        self.legend.colorNamePairs = [(PCMYKColor(100,0,90,50,alpha=100), ('BP', '30%')), (PCMYKColor(0,100,100,40,alpha=100), ('Shell Transport & Trading', '21%')), (PCMYKColor(100,60,0,50,alpha=100), ('Liberty International', '21%')), (PCMYKColor(23,51,0,4,alpha=100), ('Persimmon', '14%')), (PCMYKColor(66,13,0,22,alpha=100), ('Royal Bank of Scotland', '14%'))]
        self.width       = 400
        self.height      = 200
        self.pie.width            = 150
        self.pie.x                = 25
        self.pie.y                = -25
        self.legend.x              = 225
        self.legend.subCols.rpad      = 12
        self.pie.slices.popout                    = 5

PieChart04().save(formats=['pdf'],outDir='.',fnRoot=None)

/mnt/chromeos/MyFiles/Downloads/gfe.py
