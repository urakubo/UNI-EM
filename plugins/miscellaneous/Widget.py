from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

class Widget(QListWidget):
    def __init__(self, parent=None):
        super(Widget,self).__init__(parent)

        self.width = 150

        self.dragging = False
        self.layout = None
        self.onClickedCallback = None
        self.onInsertedCallback = None
        self.onDeleteCallback = None
        self.onDropCallback = None

        self.itemClicked.connect(self.onClicked)
        self.model().rowsInserted.connect(self.onInserted)
        self.setStyleSheet("color:black;")
        self.setMinimumWidth(self.width)

        self.widgets = []
        self.title_label = None

    def remove(self):
        for w in self.widgets:
            w.deleteLater()
        self.widgets = []

    def addWidget(self, w):
       self.layout.addWidget(w)
       self.widgets.append(w)

    def onInserted(self, parent, start, end):
        if self.onInsertedCallback is not None:
            self.onInsertedCallback(parent, start, end)

    def onClicked(self, item):
        if self.onClickedCallback is not None:
            self.onClickedCallback(self.selected)

    @property
    def selected(self):
        selModel = self.selectionModel()
        indexes = selModel.selectedIndexes()
        selected = None
        if len(indexes) != 0:
            selected = indexes[0]

        return selected

    def dragEnterEvent(self, e):
        self.dragging = True

        super(Widget, self).dragEnterEvent(e)

    def dropEvent(self, e):
        if self.onDropCallback is not None:
            self.onDropCallback()

        self.dragging = False

        super(Widget, self).dropEvent(e)

    def dragLeaveEvent(self, e):
        super(Widget, self).dragLeaveEvent(e)

