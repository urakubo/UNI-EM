from PyQt5.QtWidgets import QAbstractItemView, QMenu, QAction, QListView, QSizePolicy
from PyQt5.QtCore import Qt, QEvent, QSize
from PyQt5.QtGui import QStandardItemModel

from .Widget import Widget

class TargetWidget(Widget):
    def __init__(self,parent=None):
        super(TargetWidget, self).__init__(parent)
    
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def sizeHint(self):
        s = QSize()
        s.setHeight(200)
        s.setWidth(150)
        return s

    def contextMenu(self, point):
        menu = QMenu(self)
        menu.setStyleSheet("background-color:white;")
        menu.setStyleSheet("color:black;")

        action = QAction('Delete', self)
        action.triggered.connect(self.onDeleteItem)
        menu.addAction(action)

        menu.exec_(self.mapToGlobal(point))

    def onDeleteItem(self):
        self.model().removeRow(self.selected.row())

        if self.onDeleteCallback is not None:
            self.onDeleteCallback()

