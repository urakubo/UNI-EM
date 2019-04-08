from PyQt5.QtWidgets import QAbstractItemView
from .Widget import Widget

class SourceWidget(Widget):
    def __init__(self, parent=None):
        super(SourceWidget,self).__init__(parent)
    
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

