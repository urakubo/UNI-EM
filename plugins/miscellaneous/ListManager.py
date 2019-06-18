from PyQt5.QtWidgets import QLabel, QLineEdit, QCheckBox, QListWidgetItem, QSpinBox
from PyQt5.QtCore import Qt

from Filter2D3D.FiltersInfo import FilterInfo

from .SourceWidget import SourceWidget
from .TargetWidget import TargetWidget
from .ParameterWidget import ParameterWidget

class ListManager:
    def __init__(self, parent):
        self.parent = parent
        self.widgets = []
        self.fi = FilterInfo()
        self.__width = 150

    def getFilterInstance(self, name):
        cls = self.fi.get_class(name)
        return cls()

    def addSource(self, layout, filters=[]):
        w = SourceWidget()
        layout.addWidget(w)

        for name in filters:
            item = QListWidgetItem(name)
            instance = self.getFilterInstance(name)
            item.setData(Qt.UserRole, instance)
            w.addItem(item)

        self.widgets.append(w)

    def addTarget(self, layout):
        w = TargetWidget()
        w.onClickedCallback = self.onClickedTarget
        w.onDeleteCallback = self.onDeleteTarget
        w.onDropCallback = self.onDropTarget
        layout.addWidget(w, alignment=Qt.AlignTop)

        self.widgets.append(w)

    def addParameter(self, layout):
        w = ParameterWidget()
        layout.addLayout(w)

        self.widgets.append(w)

    def leaveDragging(self):
        for w in self.widgets:
            w.dragging = False

    def onDropTarget(self):
        sourceWidget = self.widgets[0]
        sourceWidget2 = self.widgets[1]
        targetWidget = self.widgets[2]

        if not (sourceWidget.dragging or sourceWidget2.dragging):
            targetWidget.model().removeRow(targetWidget.selected.row())

        self.leaveDragging()

    def onDeleteTarget(self):
        parameterWidget = self.widgets[3]
        parameterWidget.setTitle('')
        parameterWidget.remove()

    def onClickedTarget(self, selected):
        text = selected.data()
        instance = selected.data(Qt.UserRole)

        parameterWidget = self.widgets[3]
        parameterWidget.remove()
        parameterWidget.setTitle(text)

        for idx, a in enumerate(instance.args):
            if a[1] == 'SpinBox':
                l = QLabel(a[0])
                l.setToolTip(instance.tips[idx])
                e = QSpinBox()
                e.setStyleSheet("color:black;")
                e.setRange(int(a[2][0]), int(a[2][2]))
                parameterWidget.addWidget(l)
                parameterWidget.addWidget(e)
                e.setValue(int(a[2][1]))
            elif a[1] == 'CheckBox':
                l = QLabel(a[0])
                l.setToolTip(instance.tips[idx])
                e = QCheckBox()
                parameterWidget.addWidget(l)
                parameterWidget.addWidget(e)
                e.setChecked(a[2])
            else:
                print('Not found {}'.format(a[1]))

            def handlerText(key):
                return lambda text: self.changedText(selected, key, text)

            def handlerState(key):
                return lambda: self.changedState(selected, key)

            if isinstance(e, QSpinBox):
                e.valueChanged[int].connect(handlerText(a[0]))
            elif isinstance(e, QCheckBox):
                e.stateChanged.connect(handlerState(a[0]))

    def changedText(self, selected, key, value):
        row = selected.row()
        targetWidget = self.widgets[2]
        item = targetWidget.item(row)
        instance = item.data(Qt.UserRole)
        for idx, a in enumerate(instance.args):
            if a[0] == key:
                a[2][1] = value
        item.setData(Qt.UserRole, instance)

    def changedState(self, selected, key):
        row = selected.row()
        targetWidget = self.widgets[2]
        item = targetWidget.item(row)
        instance = item.data(Qt.UserRole)
        for idx, a in enumerate(instance.args):
            if a[0] == key:
                a[2] = not a[2]
        item.setData(Qt.UserRole, instance)

