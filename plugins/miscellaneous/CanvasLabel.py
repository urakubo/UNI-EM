
from PyQt5.QtWidgets import QLabel


class CanvasLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(CanvasLabel, self).__init__(*args, **kwargs)
        self.mousePressEvent = self.onMousePress
        self.mouseMoveEvent = self.onMouseMove
        self.changePosCallback = None

        self.baseX = 0
        self.baseY = 0

    def onMousePress(self, e):
        x = e.pos().x()
        y = e.pos().y() 

        self.baseX = x
        self.baseY = y 

    def onMouseMove(self, e):
        x = e.pos().x()
        y = e.pos().y() 
        
        if self.changePosCallback is not None:
            relativeX = x - self.baseX
            relativeY = y - self.baseY
            self.changePosCallback(-1 * relativeX, -1 * relativeY)

        self.baseX = x
        self.baseY = y 

